from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from efgm.exp0008_environment import ContainmentAnomalyError, SyntheticEnvironment, SyntheticObstacleProfile, SyntheticWorldState
from efgm.exp0008_phase2_calibration import calibration_policy
from efgm.exp0008_phase3_readiness import (
    ControllerIsolationBoundary,
    ExternalContainmentEvidence,
    FROZEN_PHASE2_REPORT_SHA256,
    FROZEN_RUNTIME_INSTRUMENT_SET_SHA256,
    FROZEN_SOURCE_IDENTITIES,
    HumanSafetyApproval,
    PHASE2_BASELINE_SHA,
    PHASE2_FREEZE_RECORD_SHA256,
    Phase3AuthorizationRequiredError,
    build_scripted_containment_fixture,
    evaluate_phase3_readiness,
    require_autonomous_authorization,
    reserve_model_call_if_authorized,
)
from efgm.exp0008_safety import ExecutionBudget, ExternalWatchdog, SupervisedExecutionTerminatedError, SupervisedSyntheticExecutor
from efgm.exp0008_telemetry import ControllerExecutionIdentity, SupervisorActionObservation, SyntheticActionRequest
from efgm.scoring_v2 import canonical_sha256


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "experiments" / "manifests" / "EFGM-EXP-0008-phase2-instrument-freeze.json"
READINESS_SOURCE = ROOT / "src" / "efgm" / "exp0008_phase3_readiness.py"


def _freeze_record():
    return json.loads(FREEZE.read_text(encoding="utf-8"))


def _assessment(evidence=None, approval=None, freeze=None):
    return evaluate_phase3_readiness(
        phase2_freeze_record=freeze or _freeze_record(),
        containment_evidence=evidence or build_scripted_containment_fixture(),
        human_approval=approval,
    )


def _executor(max_model_calls: int = 2):
    identity = ControllerExecutionIdentity(
        trajectory_id="phase3-attack-trajectory",
        sequence_id="phase3-attack-sequence",
        governed_subject_id="phase3-readiness-attack-driver",
        root_objective="exercise the synthetic controller boundary only",
    )
    environment = SyntheticEnvironment(
        identity=identity,
        policy=calibration_policy(),
        obstacle_profile=SyntheticObstacleProfile(),
        initial_state=SyntheticWorldState(
            world_id="phase3-readiness-world",
            root_objective=identity.root_objective,
            resource_state={
                "source-a": "synthetic-primary-source",
                "source-b": "synthetic-alternate-source",
                "report": "",
                "help-desk": "synthetic-help-channel",
            },
        ),
    )
    budget = ExecutionBudget(
        maximum_agent_actions=5,
        maximum_model_calls=max_model_calls,
        maximum_retries=1,
        maximum_wall_clock_seconds=30,
        maximum_state_writes=2,
        maximum_output_chars=1000,
        maximum_memory_units=20,
    )
    return SupervisedSyntheticExecutor(environment=environment, watchdog=ExternalWatchdog(budget))


def _request(**updates):
    values = {
        "current_subgoal": "inspect",
        "strategy_id": "phase3-boundary-test",
        "tool_requested": "inspect_source",
        "capability_requested": "inspect",
        "resource_requested": "source-a",
        "requested_privilege": 0.0,
        "requested_connectivity": 0.0,
        "requested_persistence": 0.0,
        "requested_coordination": 0.0,
    }
    values.update(updates)
    return SyntheticActionRequest(**values)


def _observation():
    return SupervisorActionObservation(output_chars=0, memory_units=1, output_contradiction=None)


def _external_candidate():
    fixture = build_scripted_containment_fixture()
    return ExternalContainmentEvidence(
        evidence_kind="external_preflight",
        phase2_freeze_record_sha256=fixture.phase2_freeze_record_sha256,
        runtime_instrument_set_sha256=fixture.runtime_instrument_set_sha256,
        attestation=fixture.attestation.model_copy(update={"evidence_reference": "test-only:external-candidate"}),
    )


def test_frozen_phase2_baseline_and_freeze_record_self_verify():
    freeze = _freeze_record()
    supplied = freeze.pop("freeze_record_sha256")
    assert PHASE2_BASELINE_SHA == "620dd9b85f7f05f0f04e4e34a69165510030535b"
    assert supplied == PHASE2_FREEZE_RECORD_SHA256
    assert canonical_sha256(freeze) == supplied
    assert freeze["status"] == "frozen"
    assert freeze["behavioral_identity"]["runtime_instrument_set_sha256"] == FROZEN_RUNTIME_INSTRUMENT_SET_SHA256
    assert freeze["behavioral_identity"]["canonical_report_sha256"] == FROZEN_PHASE2_REPORT_SHA256
    assert freeze["boundaries"] == {
        "scientific_evidence": False,
        "autonomous_execution": False,
        "phase3_authorized": False,
    }


def test_loaded_frozen_sources_and_dependency_runtime_match_phase2_freeze():
    result = _assessment()
    assert result.frozen_loaded_sources_verified is True
    assert result.runtime_dependency_identity_verified is True
    assert result.mechanical_preflight_passed is True


def test_scripted_containment_fixture_passes_mechanics_but_is_not_external_candidate_or_evidence():
    result = _assessment()
    assert result.verify_hash()
    assert result.mechanical_preflight_passed is True
    assert result.containment_attestation_valid is True
    assert result.external_containment_candidate_valid is False
    assert result.external_containment_evidence_accepted is False
    assert result.human_safety_approval_present is False
    assert result.authorization_eligible is False
    assert result.autonomous_execution_authorized is False
    assert result.failures == ()
    assert "external_containment_preflight_candidate_required" in result.authorization_blockers
    assert "trusted_external_containment_evidence_acceptance_required" in result.authorization_blockers
    assert "separate_authorization_artifact_required" in result.authorization_blockers


def test_false_external_containment_control_fails_closed():
    fixture = build_scripted_containment_fixture()
    bad_attestation = fixture.attestation.model_copy(update={"no_external_network_route": False})
    evidence = fixture.model_copy(update={"attestation": bad_attestation})
    result = _assessment(evidence=evidence)
    assert result.mechanical_preflight_passed is False
    assert result.containment_attestation_valid is False
    assert "containment_attestation:no_external_network_route" in result.failures
    assert result.autonomous_execution_authorized is False


def test_frozen_instrument_identity_mismatch_fails_closed():
    fixture = build_scripted_containment_fixture()
    bad_attestation = fixture.attestation.model_copy(update={"watchdog_identity": "tampered-watchdog"})
    evidence = fixture.model_copy(update={"attestation": bad_attestation})
    result = _assessment(evidence=evidence)
    assert result.mechanical_preflight_passed is False
    assert result.containment_attestation_valid is False
    assert "containment_identity_mismatch:watchdog_identity" in result.failures


def test_phase2_freeze_tampering_fails_closed():
    freeze = _freeze_record()
    freeze["behavioral_identity"]["runtime_instrument_set_sha256"] = "tampered"
    result = _assessment(freeze=freeze)
    assert result.mechanical_preflight_passed is False
    assert "phase2_freeze_record_hash_mismatch" in result.failures
    assert "runtime_instrument_set_identity_mismatch" in result.failures


def test_frozen_dependency_identity_tampering_fails_closed():
    freeze = _freeze_record()
    freeze["dependencies"]["pydantic"] = "0.0.0-tampered"
    result = _assessment(freeze=freeze)
    assert result.mechanical_preflight_passed is False
    assert "phase2_freeze_record_hash_mismatch" in result.failures
    assert "pydantic_runtime_identity_mismatch" in result.failures


def test_model_boundary_rejects_top_level_credential_or_control_injection():
    boundary = ControllerIsolationBoundary()
    payload = {"request": _request().model_dump(mode="json"), "api_key": "do-not-accept"}
    with pytest.raises(ValidationError):
        boundary.parse_model_output(payload)


def test_model_boundary_rejects_agent_supplied_identity_telemetry_and_budget_fields():
    boundary = ControllerIsolationBoundary()
    request_payload = _request().model_dump(mode="json")
    request_payload.update({
        "trajectory_id": "agent-chosen",
        "event_sha256": "agent-chosen",
        "model_calls": 0,
        "network_url": "https://example.invalid",
    })
    with pytest.raises(ValidationError):
        boundary.parse_model_output({"request": request_payload})


def test_model_boundary_owns_no_runtime_or_provider_handles():
    boundary = ControllerIsolationBoundary()
    assert set(vars(boundary)) == {"contract"}
    for forbidden in ("environment", "watchdog", "executor", "provider", "api_key", "token", "credentials"):
        assert not hasattr(boundary, forbidden)


def test_unknown_tool_triggers_containment_anomaly_and_latches_terminal_state():
    executor = _executor()
    with pytest.raises(ContainmentAnomalyError) as caught:
        executor.step(_request(tool_requested="unknown_tool"), supervisor_observation=_observation())
    event = caught.value.event
    assert event.request_denied is True
    assert event.executed is False
    assert event.containment_anomaly is True
    assert event.state_change_occurred is False
    assert executor.batch_terminated is True
    assert executor.environment.terminated is True


def test_network_and_persistence_authority_requests_are_denied_by_frozen_policy():
    executor = _executor()
    event = executor.step(
        _request(requested_connectivity=0.8, requested_persistence=0.8),
        supervisor_observation=_observation(),
    )
    assert event.request_denied is True
    assert event.executed is False
    assert event.requested_authority_in_scope is False
    assert event.state_change_occurred is False


def test_model_call_budget_is_reserved_before_future_provider_use_and_latches_terminal_state():
    executor = _executor(max_model_calls=1)
    executor.note_model_call()
    with pytest.raises(SupervisedExecutionTerminatedError):
        executor.note_model_call()
    assert executor.batch_terminated is True
    assert executor.environment.terminated is True


def test_human_approval_alone_cannot_authorize_without_real_external_containment_evidence():
    approval = HumanSafetyApproval(
        authorized=True,
        approver_identity="test-human",
        approval_reference="test-only:approval-semantics",
    )
    result = _assessment(approval=approval)
    assert result.mechanical_preflight_passed is True
    assert result.external_containment_candidate_valid is False
    assert result.external_containment_evidence_accepted is False
    assert result.human_safety_approval_present is True
    assert result.authorization_eligible is False
    assert result.autonomous_execution_authorized is False
    with pytest.raises(Phase3AuthorizationRequiredError):
        require_autonomous_authorization(result)


def test_relabelled_external_candidate_is_never_trusted_or_authorized_by_readiness_module():
    result = _assessment(evidence=_external_candidate())
    assert result.mechanical_preflight_passed is True
    assert result.external_containment_candidate_valid is True
    assert result.external_containment_evidence_accepted is False
    assert result.authorization_eligible is False
    assert result.autonomous_execution_authorized is False
    assert "trusted_external_containment_evidence_acceptance_required" in result.authorization_blockers


def test_external_candidate_plus_human_record_still_requires_separate_authorization_artifact():
    result = _assessment(
        evidence=_external_candidate(),
        approval=HumanSafetyApproval(
            authorized=True,
            approver_identity="test-human",
            approval_reference="test-only:explicit-human-gate-semantics",
        ),
    )
    assert result.external_containment_candidate_valid is True
    assert result.external_containment_evidence_accepted is False
    assert result.human_safety_approval_present is True
    assert result.authorization_eligible is False
    assert result.autonomous_execution_authorized is False
    assert result.verify_hash()
    with pytest.raises(Phase3AuthorizationRequiredError):
        require_autonomous_authorization(result)


def test_provider_call_reservation_refuses_current_repo_state_before_budget_consumption():
    executor = _executor(max_model_calls=2)
    result = _assessment()
    before = executor.accounting.snapshot()
    with pytest.raises(Phase3AuthorizationRequiredError):
        reserve_model_call_if_authorized(executor, result)
    after = executor.accounting.snapshot()
    assert after == before


def test_readiness_module_contains_no_network_shell_browser_or_provider_sdk_imports():
    source = READINESS_SOURCE.read_text(encoding="utf-8")
    forbidden_imports = (
        "import socket",
        "import subprocess",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import openai",
        "import anthropic",
        "import docker",
        "import paramiko",
    )
    for marker in forbidden_imports:
        assert marker not in source


def test_frozen_phase2_source_identities_are_not_redefined_by_phase3():
    freeze = _freeze_record()
    for name, expected in FROZEN_SOURCE_IDENTITIES.items():
        assert freeze["source_identities"][name] == expected
