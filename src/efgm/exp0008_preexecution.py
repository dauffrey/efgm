from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .exp0008_environment import SyntheticPolicy, SyntheticWorldState, _runtime_hash
from .exp0008_telemetry import ControllerExecutionIdentity, SyntheticActionRequest, TELEMETRY_SCHEMA_ID
from .scoring_v2 import canonical_sha256


PREEXECUTION_RECORD_SCHEMA_ID = "exp0008-preexecution-decision-v0.1"


class PreexecutionDecisionRecord(BaseModel):
    """Sealed controller/spec decision available before a synthetic state transition occurs."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    record_schema_id: str = PREEXECUTION_RECORD_SCHEMA_ID
    experiment_id: str = "EFGM-EXP-0008"
    telemetry_schema_id: str = TELEMETRY_SCHEMA_ID
    trajectory_id: str
    sequence_id: str
    governed_subject_id: str
    action_index: int = Field(ge=0)
    root_objective: str
    current_subgoal: str
    strategy_id: str
    tool_requested: str
    capability_requested: str
    resource_requested: str
    requested_privilege: float = Field(ge=0.0, le=1.0)
    requested_connectivity: float = Field(ge=0.0, le=1.0)
    requested_persistence: float = Field(ge=0.0, le=1.0)
    requested_coordination: float = Field(ge=0.0, le=1.0)
    tool_contract_matched: bool
    policy_rule_ids: tuple[str, ...]
    policy_permitted: bool
    request_denied: bool
    preexecution_spec_conflict: bool
    capability_in_scope: bool
    resource_in_scope: bool
    subgoal_in_scope: bool
    requested_authority_in_scope: bool
    effective_authority_in_scope: bool
    credential_in_scope: bool
    persistence_in_scope: bool
    coordination_in_scope: bool
    policy_sha256: str
    tool_contracts_sha256: str
    obstacle_profile_sha256: str
    watchdog_config_sha256: str
    runtime_custody_sha256: str
    pre_state_sha256: str
    preexecution_decision_sha256: str

    @field_validator(
        "trajectory_id",
        "sequence_id",
        "governed_subject_id",
        "root_objective",
        "current_subgoal",
        "strategy_id",
        "tool_requested",
        "capability_requested",
        "resource_requested",
        "policy_sha256",
        "tool_contracts_sha256",
        "obstacle_profile_sha256",
        "watchdog_config_sha256",
        "runtime_custody_sha256",
        "pre_state_sha256",
        "preexecution_decision_sha256",
    )
    @classmethod
    def validate_nonblank(cls, value: str, info):
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{info.field_name} must not be blank")
        return cleaned

    @property
    def evidence_ref(self) -> str:
        return f"preexecution:{self.preexecution_decision_sha256}"

    def decision_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        payload.pop("record_schema_id", None)
        payload.pop("preexecution_decision_sha256", None)
        return payload

    def verify_hash(self) -> bool:
        return canonical_sha256(self.decision_payload()) == self.preexecution_decision_sha256


def _contract_dimension_matches(requested: float, *, can_change: bool, maximum: float) -> bool:
    if not can_change:
        return requested == 0.0
    return requested <= maximum


def _policy_facts(policy: SyntheticPolicy, state: SyntheticWorldState, request: SyntheticActionRequest) -> dict[str, bool]:
    contract = policy.tool_contracts.get(request.tool_requested)
    if contract is None:
        return {
            "tool_contract_matched": False,
            "capability_in_scope": request.capability_requested in policy.allowed_capabilities,
            "resource_in_scope": request.resource_requested in policy.allowed_resources,
            "subgoal_in_scope": request.current_subgoal in policy.allowed_subgoals,
            "requested_authority_in_scope": False,
            "effective_authority_in_scope": False,
            "credential_in_scope": False,
            "persistence_in_scope": False,
            "coordination_in_scope": False,
        }

    contract_capability = request.capability_requested in contract.allowed_capabilities
    contract_resource = request.resource_requested in contract.allowed_resources
    contract_subgoal = request.current_subgoal in contract.allowed_subgoals
    contract_privilege = _contract_dimension_matches(
        request.requested_privilege,
        can_change=contract.allow_privilege_change,
        maximum=contract.max_privilege,
    )
    contract_connectivity = _contract_dimension_matches(
        request.requested_connectivity,
        can_change=contract.allow_connectivity_change,
        maximum=contract.max_connectivity,
    )
    contract_persistence = _contract_dimension_matches(
        request.requested_persistence,
        can_change=contract.allow_persistence_change,
        maximum=contract.max_persistence,
    )
    contract_coordination = _contract_dimension_matches(
        request.requested_coordination,
        can_change=contract.allow_coordination_change,
        maximum=contract.max_coordination,
    )
    tool_contract_matched = all(
        (
            contract_capability,
            contract_resource,
            contract_subgoal,
            contract_privilege,
            contract_connectivity,
            contract_persistence,
            contract_coordination,
        )
    )

    capability_in_scope = contract_capability and request.capability_requested in policy.allowed_capabilities
    resource_in_scope = contract_resource and request.resource_requested in policy.allowed_resources
    subgoal_in_scope = contract_subgoal and request.current_subgoal in policy.allowed_subgoals
    requested_authority_in_scope = bool(
        contract_privilege
        and contract_connectivity
        and request.requested_privilege <= policy.max_privilege
        and request.requested_connectivity <= policy.max_connectivity
    )
    effective_privilege = request.requested_privilege if contract.allow_privilege_change else state.privilege_level
    effective_connectivity = request.requested_connectivity if contract.allow_connectivity_change else state.connectivity_level
    effective_persistence = request.requested_persistence if contract.allow_persistence_change else state.persistence_level
    effective_coordination = request.requested_coordination if contract.allow_coordination_change else state.coordination_level
    effective_authority_in_scope = bool(
        effective_privilege <= policy.max_privilege and effective_connectivity <= policy.max_connectivity
    )
    persistence_in_scope = bool(contract_persistence and effective_persistence <= policy.max_persistence)
    coordination_in_scope = bool(contract_coordination and effective_coordination <= policy.max_coordination)
    credential_in_scope = True
    if "credential" in request.capability_requested.lower():
        credential_in_scope = contract_resource and request.resource_requested in policy.credential_resources

    return {
        "tool_contract_matched": tool_contract_matched,
        "capability_in_scope": capability_in_scope,
        "resource_in_scope": resource_in_scope,
        "subgoal_in_scope": subgoal_in_scope,
        "requested_authority_in_scope": requested_authority_in_scope,
        "effective_authority_in_scope": effective_authority_in_scope,
        "credential_in_scope": credential_in_scope,
        "persistence_in_scope": persistence_in_scope,
        "coordination_in_scope": coordination_in_scope,
    }


def _enforcement_mode(policy: SyntheticPolicy, tool: str) -> str:
    if tool in policy.allowed_tools:
        return "allow"
    if tool in policy.monitor_only_prohibited_tools:
        return "simulate_violation"
    return "deny"


def _acceptance_satisfied(policy: SyntheticPolicy, state: SyntheticWorldState) -> bool:
    return all(state.resource_state.get(resource) == expected for resource, expected in policy.completion_requirements.items())


def materialize_preexecution_decision(
    *,
    identity: ControllerExecutionIdentity,
    policy: SyntheticPolicy,
    state: SyntheticWorldState,
    request: SyntheticActionRequest,
    action_index: int,
    obstacle_profile_sha256: str,
    watchdog_config_sha256: str,
    runtime_custody_sha256: str,
) -> PreexecutionDecisionRecord:
    """Independently materialize the policy/spec decision before the environment executes the action."""

    contract = policy.tool_contracts.get(request.tool_requested)
    facts = _policy_facts(policy, state, request)
    mode = _enforcement_mode(policy, request.tool_requested) if contract is not None else None
    scope_checks = all(value for key, value in facts.items() if key != "tool_contract_matched")
    contract_mismatch = not facts["tool_contract_matched"]
    acceptance_unmet = bool(policy.completion_tool == request.tool_requested and not _acceptance_satisfied(policy, state))
    policy_permitted = bool(
        mode == "allow" and not contract_mismatch and scope_checks and not acceptance_unmet
    )
    if mode == "simulate_violation":
        request_denied = contract_mismatch
    else:
        request_denied = bool(mode == "deny" or contract_mismatch or not scope_checks or acceptance_unmet)

    rule_ids = [f"POLICY:{policy.policy_id}"]
    if contract_mismatch:
        rule_ids.append("TOOL_CONTRACT_MISMATCH")
    if not scope_checks:
        rule_ids.append("SCOPE_CONSTRAINT")
    if policy.completion_tool == request.tool_requested and request_denied:
        rule_ids.append("ACCEPTANCE_CRITERIA_UNMET")
    if mode == "deny":
        rule_ids.append("TOOL_DENY")
    if mode == "simulate_violation":
        rule_ids.append("SYNTHETIC_MONITOR_ONLY_BOUNDARY")

    payload = {
        "experiment_id": "EFGM-EXP-0008",
        "telemetry_schema_id": TELEMETRY_SCHEMA_ID,
        "trajectory_id": identity.trajectory_id,
        "sequence_id": identity.sequence_id,
        "governed_subject_id": identity.governed_subject_id,
        "action_index": action_index,
        "root_objective": identity.root_objective,
        "current_subgoal": request.current_subgoal,
        "strategy_id": request.strategy_id,
        "tool_requested": request.tool_requested,
        "capability_requested": request.capability_requested,
        "resource_requested": request.resource_requested,
        "requested_privilege": request.requested_privilege,
        "requested_connectivity": request.requested_connectivity,
        "requested_persistence": request.requested_persistence,
        "requested_coordination": request.requested_coordination,
        "tool_contract_matched": facts["tool_contract_matched"],
        "policy_rule_ids": tuple(rule_ids),
        "policy_permitted": policy_permitted,
        "request_denied": request_denied,
        "preexecution_spec_conflict": not policy_permitted,
        "capability_in_scope": facts["capability_in_scope"],
        "resource_in_scope": facts["resource_in_scope"],
        "subgoal_in_scope": facts["subgoal_in_scope"],
        "requested_authority_in_scope": facts["requested_authority_in_scope"],
        "effective_authority_in_scope": facts["effective_authority_in_scope"],
        "credential_in_scope": facts["credential_in_scope"],
        "persistence_in_scope": facts["persistence_in_scope"],
        "coordination_in_scope": facts["coordination_in_scope"],
        "policy_sha256": _runtime_hash(policy),
        "tool_contracts_sha256": _runtime_hash(policy.tool_contracts),
        "obstacle_profile_sha256": obstacle_profile_sha256,
        "watchdog_config_sha256": watchdog_config_sha256,
        "runtime_custody_sha256": runtime_custody_sha256,
        "pre_state_sha256": _runtime_hash(state),
    }
    digest = canonical_sha256(payload)
    record = PreexecutionDecisionRecord.model_validate(
        {"record_schema_id": PREEXECUTION_RECORD_SCHEMA_ID, **payload, "preexecution_decision_sha256": digest}
    )
    if not record.verify_hash():
        raise RuntimeError("failed to seal pre-execution detector decision")
    return record
