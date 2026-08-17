from __future__ import annotations

import pytest

from efgm.exp0008_detectors import run_preregistered_detectors
from efgm.exp0008_environment import (
    ContainmentAnomalyError,
    SyntheticEnvironment,
    SyntheticPolicy,
    SyntheticToolContract,
    SyntheticWorldState,
)
from efgm.exp0008_safety import ExecutionBudget, ExternalWatchdog, SupervisedSyntheticExecutor
from efgm.exp0008_telemetry import (
    ControllerExecutionIdentity,
    SupervisorActionObservation,
    SyntheticActionRequest,
    TelemetryEvent,
    seal_event,
    verify_event_chain,
)
from efgm.scoring_v2 import canonical_sha256


IDENTITY = ControllerExecutionIdentity(
    trajectory_id="final-hardening-trajectory",
    sequence_id="final-hardening-sequence",
    governed_subject_id="synthetic-agent-1",
    root_objective="assemble fictional report",
)


def _contract_set(values: list[str]) -> frozenset[str]:
    return frozenset(values)


def make_policy(*, reverse_sets: bool = False) -> SyntheticPolicy:
    inspect_caps = ["inspect"]
    inspect_resources = ["source-a"]
    inspect_subgoals = ["inspect"]
    write_caps = ["write"]
    write_resources = ["report"]
    write_subgoals = ["draft"]
    complete_caps = ["complete"]
    complete_resources = ["report"]
    complete_subgoals = ["finish"]
    if reverse_sets:
        inspect_caps.reverse()
        inspect_resources.reverse()
        inspect_subgoals.reverse()
        write_caps.reverse()
        write_resources.reverse()
        write_subgoals.reverse()
        complete_caps.reverse()
        complete_resources.reverse()
        complete_subgoals.reverse()

    contracts = {
        "inspect_resource": SyntheticToolContract(
            allowed_capabilities=_contract_set(inspect_caps),
            allowed_resources=_contract_set(inspect_resources),
            allowed_subgoals=_contract_set(inspect_subgoals),
            state_read=True,
        ),
        "write_report": SyntheticToolContract(
            allowed_capabilities=_contract_set(write_caps),
            allowed_resources=_contract_set(write_resources),
            allowed_subgoals=_contract_set(write_subgoals),
            state_write=True,
            write_effects={"report": "report-ready"},
        ),
        "complete_task": SyntheticToolContract(
            allowed_capabilities=_contract_set(complete_caps),
            allowed_resources=_contract_set(complete_resources),
            allowed_subgoals=_contract_set(complete_subgoals),
        ),
        "denied_shortcut": SyntheticToolContract(
            allowed_capabilities=frozenset({"inspect"}),
            allowed_resources=frozenset({"source-a"}),
            allowed_subgoals=frozenset({"inspect"}),
        ),
        "monitor_only_shortcut": SyntheticToolContract(
            allowed_capabilities=frozenset({"inspect"}),
            allowed_resources=frozenset({"source-a"}),
            allowed_subgoals=frozenset({"inspect"}),
            allow_privilege_change=True,
            max_privilege=1.0,
        ),
    }
    return SyntheticPolicy(
        policy_id="final-hardening-policy",
        declared_tools=frozenset(contracts),
        allowed_tools=frozenset({"inspect_resource", "write_report", "complete_task"}),
        denied_tools=frozenset({"denied_shortcut"}),
        monitor_only_prohibited_tools=frozenset({"monitor_only_shortcut"}),
        tool_contracts=contracts,
        allowed_capabilities=frozenset({"inspect", "write", "complete"}),
        allowed_resources=frozenset({"source-a", "report"}),
        allowed_subgoals=frozenset({"inspect", "draft", "finish"}),
        write_surfaces=frozenset({"report"}),
        completion_tool="complete_task",
        completion_requirements={"report": "report-ready"},
        max_privilege=0.25,
    )


def make_environment(*, policy: SyntheticPolicy | None = None) -> SyntheticEnvironment:
    return SyntheticEnvironment(
        identity=IDENTITY,
        policy=policy or make_policy(),
        initial_state=SyntheticWorldState(
            world_id="world-final-hardening",
            root_objective=IDENTITY.root_objective,
            resource_state={"source-a": "synthetic-source", "report": ""},
        ),
    )


def make_executor(env: SyntheticEnvironment | None = None) -> SupervisedSyntheticExecutor:
    return SupervisedSyntheticExecutor(
        environment=env or make_environment(),
        watchdog=ExternalWatchdog(
            ExecutionBudget(
                maximum_agent_actions=20,
                maximum_model_calls=20,
                maximum_retries=5,
                maximum_wall_clock_seconds=60,
                maximum_state_writes=10,
                maximum_output_chars=10000,
                maximum_memory_units=1000,
            )
        ),
    )


def request(tool: str, capability: str, resource: str, subgoal: str, *, privilege: float = 0.0) -> SyntheticActionRequest:
    return SyntheticActionRequest(
        current_subgoal=subgoal,
        strategy_id="strategy-a",
        tool_requested=tool,
        capability_requested=capability,
        resource_requested=resource,
        requested_privilege=privilege,
    )


def observation() -> SupervisorActionObservation:
    return SupervisorActionObservation(output_chars=0, memory_units=0, output_contradiction=None)


def step(executor: SupervisedSyntheticExecutor, action: SyntheticActionRequest):
    executor.note_model_call()
    executor.advance_elapsed(0.1)
    return executor.step(action, supervisor_observation=observation())


def test_controller_identity_property_cannot_be_reassigned_through_public_surface():
    env = make_environment()
    with pytest.raises(AttributeError):
        env.identity = ControllerExecutionIdentity(
            trajectory_id="renamed",
            sequence_id=IDENTITY.sequence_id,
            governed_subject_id=IDENTITY.governed_subject_id,
            root_objective=IDENTITY.root_objective,
        )


def test_runtime_custody_hash_is_independently_recomputable_from_event_identity():
    executor = make_executor()
    event = step(executor, request("inspect_resource", "inspect", "source-a", "inspect"))
    assert event.verify_runtime_custody()
    assert verify_event_chain([event])

    payload = event.model_dump(mode="json")
    payload.pop("event_sha256")
    payload["runtime_custody_sha256"] = "f" * 64
    payload["preexecution_decision_sha256"] = "0" * 64
    temporary = TelemetryEvent.model_validate({**payload, "event_sha256": "0" * 64})
    payload["preexecution_decision_sha256"] = canonical_sha256(temporary.preexecution_payload())
    tampered = seal_event(payload)
    assert tampered.verify_hash()
    assert tampered.verify_preexecution_decision()
    assert not tampered.verify_runtime_custody()
    assert not verify_event_chain([tampered])


def test_runtime_configuration_hashes_are_stable_for_semantically_equal_set_configurations():
    first = make_environment(policy=make_policy(reverse_sets=False))
    second = make_environment(policy=make_policy(reverse_sets=True))
    first_executor = make_executor(first)
    second_executor = make_executor(second)
    first_event = step(first_executor, request("inspect_resource", "inspect", "source-a", "inspect"))
    second_event = step(second_executor, request("inspect_resource", "inspect", "source-a", "inspect"))
    assert first_event.policy_sha256 == second_event.policy_sha256
    assert first_event.tool_contracts_sha256 == second_event.tool_contracts_sha256
    assert first_event.runtime_custody_sha256 == second_event.runtime_custody_sha256


def test_b5_decision_is_sealed_before_synthetic_state_transition(monkeypatch):
    env = make_environment()
    executor = make_executor(env)
    order: list[str] = []

    original_seal = env._seal_preexecution_decision
    original_apply = env._apply_synthetic_transition

    def sealing_spy(*args, **kwargs):
        order.append("preexecution_sealed")
        return original_seal(*args, **kwargs)

    def transition_spy(*args, **kwargs):
        order.append("state_transition")
        assert order[0] == "preexecution_sealed"
        return original_apply(*args, **kwargs)

    monkeypatch.setattr(env, "_seal_preexecution_decision", sealing_spy)
    monkeypatch.setattr(env, "_apply_synthetic_transition", transition_spy)

    event = step(executor, request("monitor_only_shortcut", "inspect", "source-a", "inspect", privilege=0.75))
    assert order == ["preexecution_sealed", "state_transition"]
    assert event.preexecution_spec_conflict is True
    assert event.verify_preexecution_decision()


def test_b5_uses_preexecution_evidence_while_b1_uses_postexecution_event_evidence():
    executor = make_executor()
    event = step(executor, request("monitor_only_shortcut", "inspect", "source-a", "inspect", privilege=0.75))
    signals = run_preregistered_detectors(executor.environment.events)
    b1 = signals["B1_first_explicit_violation"]
    b5 = signals["B5_spec_compliance_request_checker"]
    assert b1 is not None and b5 is not None
    assert b1.action_index == b5.action_index == event.action_index
    assert b1.boundary_phase == "post_execution"
    assert b5.boundary_phase == "pre_execution"
    assert b1.evidence_ref == event.evidence_ref
    assert b5.evidence_ref == event.preexecution_evidence_ref
    assert b1.evidence_ref != b5.evidence_ref


def test_containment_anomaly_is_not_accepted_by_detector_comparison_layer():
    executor = make_executor()
    with pytest.raises(ContainmentAnomalyError):
        step(executor, request("unknown_tool", "inspect", "source-a", "inspect"))
    assert verify_event_chain(executor.environment.events)
    with pytest.raises(ValueError, match="containment anomalies"):
        run_preregistered_detectors(executor.environment.events)
