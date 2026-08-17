from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .scoring_v2 import canonical_sha256


EXPERIMENT_ID = "EFGM-EXP-0008"
TELEMETRY_SCHEMA_ID = "exp0008-telemetry-v0.2"


def _clean_nonblank(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must not be blank or whitespace-only")
    return cleaned


def compute_runtime_custody_sha256(
    *,
    experiment_id: str,
    telemetry_schema_id: str,
    trajectory_id: str,
    sequence_id: str,
    governed_subject_id: str,
    root_objective: str,
    policy_sha256: str,
    tool_contracts_sha256: str,
    obstacle_profile_sha256: str,
    environment_initial_state_sha256: str,
    watchdog_config_sha256: str,
) -> str:
    """Canonical custody identity shared by the controller and independent verifier."""
    return canonical_sha256({
        "experiment_id": experiment_id,
        "telemetry_schema_id": telemetry_schema_id,
        "identity": {
            "trajectory_id": trajectory_id,
            "sequence_id": sequence_id,
            "governed_subject_id": governed_subject_id,
            "root_objective": root_objective,
        },
        "policy_sha256": policy_sha256,
        "tool_contracts_sha256": tool_contracts_sha256,
        "obstacle_profile_sha256": obstacle_profile_sha256,
        "environment_initial_state_sha256": environment_initial_state_sha256,
        "watchdog_config_sha256": watchdog_config_sha256,
    })


class ControllerExecutionIdentity(BaseModel):
    """Controller-owned trajectory identity; never part of the agent-visible proposal."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    trajectory_id: str
    sequence_id: str
    governed_subject_id: str
    root_objective: str

    @field_validator("trajectory_id", "sequence_id", "governed_subject_id", "root_objective")
    @classmethod
    def validate_required_text(cls, value: str, info):
        return _clean_nonblank(value, info.field_name)


class SyntheticActionRequest(BaseModel):
    """Agent-visible proposal against controller-owned synthetic tool contracts."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    current_subgoal: str
    strategy_id: str
    tool_requested: str
    capability_requested: str
    resource_requested: str
    requested_privilege: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_connectivity: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_persistence: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_coordination: float = Field(default=0.0, ge=0.0, le=1.0)

    @field_validator(
        "current_subgoal", "strategy_id", "tool_requested", "capability_requested",
        "resource_requested",
    )
    @classmethod
    def validate_required_text(cls, value: str, info):
        return _clean_nonblank(value, info.field_name)


class SupervisorActionObservation(BaseModel):
    """Controller/runtime facts outside the agent-visible request surface."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    output_chars: int = Field(ge=0)
    memory_units: int = Field(ge=0)
    output_contradiction: bool | None = None

    @model_validator(mode="after")
    def validate_output_applicability(self):
        if self.output_chars == 0 and self.output_contradiction is not None:
            raise ValueError("output_contradiction must be null when no output was emitted")
        if self.output_chars > 0 and self.output_contradiction is None:
            raise ValueError("output_contradiction must be observed when output_chars is positive")
        return self


class TelemetryEvent(BaseModel):
    """Immutable, hash-chained event emitted after one synthetic action boundary."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    experiment_id: str = EXPERIMENT_ID
    telemetry_schema_id: str = TELEMETRY_SCHEMA_ID
    trajectory_id: str
    sequence_id: str
    governed_subject_id: str
    action_index: int = Field(ge=0)
    action_id: str
    parent_action_id: str | None = None
    root_objective: str
    current_subgoal: str
    strategy_id: str
    strategy_change: bool
    obstacle_id: str | None = None
    obstacle_type: str | None = None
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
    preexecution_decision_sha256: str
    executed: bool
    action_result: str
    capability_in_scope: bool
    resource_in_scope: bool
    subgoal_in_scope: bool
    requested_authority_in_scope: bool
    effective_authority_in_scope: bool
    authority_granted: bool
    credential_in_scope: bool
    persistence_in_scope: bool
    coordination_in_scope: bool
    privilege_level: float = Field(ge=0.0, le=1.0)
    connectivity_level: float = Field(ge=0.0, le=1.0)
    persistence_level: float = Field(ge=0.0, le=1.0)
    coordination_level: float = Field(ge=0.0, le=1.0)
    state_change_occurred: bool
    state_write: bool
    state_read: bool
    cross_agent_message: bool
    action_traceable: bool
    tool_traceable: bool
    state_change_traceable: bool
    write_surface_inventoried: bool
    readback_traceable: bool
    message_traceable: bool
    revocation_available: bool
    containment_available: bool
    cleanup_available: bool
    rollback_available: bool
    failed_attempt_count: int = Field(ge=0)
    replan_count: int = Field(ge=0)
    new_subgoal_count: int = Field(ge=0)
    strategy_change_count: int = Field(ge=0)
    tool_failed: bool = False
    timed_out: bool = False
    workflow_interrupted: bool = False
    synthetic_policy_violation: bool = False
    containment_anomaly: bool = False
    output_chars: int = Field(ge=0)
    memory_units: int = Field(ge=0)
    output_contradiction: bool | None = None
    policy_sha256: str
    tool_contracts_sha256: str
    obstacle_profile_sha256: str
    environment_initial_state_sha256: str
    watchdog_config_sha256: str
    runtime_custody_sha256: str
    pre_state_sha256: str
    post_state_sha256: str
    previous_event_sha256: str | None = None
    event_sha256: str

    @field_validator(
        "trajectory_id", "sequence_id", "governed_subject_id", "action_id",
        "root_objective", "current_subgoal", "strategy_id", "tool_requested",
        "capability_requested", "resource_requested", "action_result", "event_sha256",
        "preexecution_decision_sha256", "policy_sha256", "tool_contracts_sha256",
        "obstacle_profile_sha256", "environment_initial_state_sha256",
        "watchdog_config_sha256", "runtime_custody_sha256", "pre_state_sha256",
        "post_state_sha256", "telemetry_schema_id",
    )
    @classmethod
    def validate_required_text(cls, value: str, info):
        return _clean_nonblank(value, info.field_name)

    @field_validator("obstacle_id", "obstacle_type", "parent_action_id")
    @classmethod
    def validate_optional_text(cls, value: str | None, info):
        if value is None:
            return None
        return _clean_nonblank(value, info.field_name)

    @field_validator("policy_rule_ids")
    @classmethod
    def validate_policy_rule_ids(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if not value:
            raise ValueError("policy_rule_ids must contain at least one rule identifier")
        cleaned = tuple(_clean_nonblank(item, "policy_rule_ids") for item in value)
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("policy_rule_ids must not contain duplicates")
        return cleaned

    @model_validator(mode="after")
    def validate_output_applicability(self):
        if self.output_chars == 0 and self.output_contradiction is not None:
            raise ValueError("output_contradiction must be null when no output was emitted")
        if self.output_chars > 0 and self.output_contradiction is None:
            raise ValueError("output_contradiction must be observed when output_chars is positive")
        if self.authority_granted != self.effective_authority_in_scope:
            raise ValueError("authority_granted must reflect effective authority, not request-only authority")
        return self

    @property
    def evidence_ref(self) -> str:
        return f"event:{self.event_sha256}"

    @property
    def preexecution_evidence_ref(self) -> str:
        return f"preexecution:{self.preexecution_decision_sha256}"

    def expected_runtime_custody_sha256(self) -> str:
        return compute_runtime_custody_sha256(
            experiment_id=self.experiment_id,
            telemetry_schema_id=self.telemetry_schema_id,
            trajectory_id=self.trajectory_id,
            sequence_id=self.sequence_id,
            governed_subject_id=self.governed_subject_id,
            root_objective=self.root_objective,
            policy_sha256=self.policy_sha256,
            tool_contracts_sha256=self.tool_contracts_sha256,
            obstacle_profile_sha256=self.obstacle_profile_sha256,
            environment_initial_state_sha256=self.environment_initial_state_sha256,
            watchdog_config_sha256=self.watchdog_config_sha256,
        )

    def verify_runtime_custody(self) -> bool:
        return self.expected_runtime_custody_sha256() == self.runtime_custody_sha256

    def preexecution_payload(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "telemetry_schema_id": self.telemetry_schema_id,
            "trajectory_id": self.trajectory_id,
            "sequence_id": self.sequence_id,
            "governed_subject_id": self.governed_subject_id,
            "action_index": self.action_index,
            "root_objective": self.root_objective,
            "current_subgoal": self.current_subgoal,
            "strategy_id": self.strategy_id,
            "tool_requested": self.tool_requested,
            "capability_requested": self.capability_requested,
            "resource_requested": self.resource_requested,
            "requested_privilege": self.requested_privilege,
            "requested_connectivity": self.requested_connectivity,
            "requested_persistence": self.requested_persistence,
            "requested_coordination": self.requested_coordination,
            "tool_contract_matched": self.tool_contract_matched,
            "policy_rule_ids": self.policy_rule_ids,
            "policy_permitted": self.policy_permitted,
            "request_denied": self.request_denied,
            "preexecution_spec_conflict": self.preexecution_spec_conflict,
            "capability_in_scope": self.capability_in_scope,
            "resource_in_scope": self.resource_in_scope,
            "subgoal_in_scope": self.subgoal_in_scope,
            "requested_authority_in_scope": self.requested_authority_in_scope,
            "effective_authority_in_scope": self.effective_authority_in_scope,
            "credential_in_scope": self.credential_in_scope,
            "persistence_in_scope": self.persistence_in_scope,
            "coordination_in_scope": self.coordination_in_scope,
            "policy_sha256": self.policy_sha256,
            "tool_contracts_sha256": self.tool_contracts_sha256,
            "obstacle_profile_sha256": self.obstacle_profile_sha256,
            "watchdog_config_sha256": self.watchdog_config_sha256,
            "runtime_custody_sha256": self.runtime_custody_sha256,
            "pre_state_sha256": self.pre_state_sha256,
        }

    def verify_preexecution_decision(self) -> bool:
        return canonical_sha256(self.preexecution_payload()) == self.preexecution_decision_sha256

    def hash_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        payload.pop("event_sha256", None)
        return payload

    def verify_hash(self) -> bool:
        return canonical_sha256(self.hash_payload()) == self.event_sha256


def seal_event(payload: dict[str, Any]) -> TelemetryEvent:
    candidate = dict(payload)
    candidate.pop("event_sha256", None)
    normalized = TelemetryEvent.model_validate({**candidate, "event_sha256": "0" * 64}).hash_payload()
    digest = canonical_sha256(normalized)
    return TelemetryEvent.model_validate({**normalized, "event_sha256": digest})


def verify_event_chain(events: list[TelemetryEvent]) -> bool:
    if not events:
        return True
    first = events[0]
    identity = (
        first.experiment_id,
        first.telemetry_schema_id,
        first.trajectory_id,
        first.sequence_id,
        first.governed_subject_id,
        first.root_objective,
        first.policy_sha256,
        first.tool_contracts_sha256,
        first.obstacle_profile_sha256,
        first.environment_initial_state_sha256,
        first.watchdog_config_sha256,
        first.runtime_custody_sha256,
    )
    previous_hash: str | None = None
    previous_action_id: str | None = None
    previous_post_state = first.environment_initial_state_sha256
    for index, event in enumerate(events):
        if not event.verify_hash() or not event.verify_preexecution_decision() or not event.verify_runtime_custody() or event.action_index != index:
            return False
        current_identity = (
            event.experiment_id,
            event.telemetry_schema_id,
            event.trajectory_id,
            event.sequence_id,
            event.governed_subject_id,
            event.root_objective,
            event.policy_sha256,
            event.tool_contracts_sha256,
            event.obstacle_profile_sha256,
            event.environment_initial_state_sha256,
            event.watchdog_config_sha256,
            event.runtime_custody_sha256,
        )
        if current_identity != identity:
            return False
        if event.previous_event_sha256 != previous_hash:
            return False
        if event.pre_state_sha256 != previous_post_state:
            return False
        if index == 0 and event.parent_action_id is not None:
            return False
        if index > 0 and event.parent_action_id != previous_action_id:
            return False
        previous_hash = event.event_sha256
        previous_action_id = event.action_id
        previous_post_state = event.post_state_sha256
    return True
