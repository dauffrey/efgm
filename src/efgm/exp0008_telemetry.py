from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .scoring_v2 import canonical_sha256


EXPERIMENT_ID = "EFGM-EXP-0008"


def _clean_nonblank(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} must not be blank or whitespace-only")
    return cleaned


class SyntheticActionRequest(BaseModel):
    """A request against the fictional EXP-0008 state machine.

    This is data only. It cannot carry executable code, shell commands, URLs,
    credentials, host paths, or arbitrary tool payloads.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    trajectory_id: str
    sequence_id: str
    governed_subject_id: str
    root_objective: str
    current_subgoal: str
    strategy_id: str
    obstacle_id: str | None = None
    parent_action_id: str | None = None

    tool_requested: str
    capability_requested: str
    resource_requested: str
    requested_privilege: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_connectivity: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_persistence: float = Field(default=0.0, ge=0.0, le=1.0)
    requested_coordination: float = Field(default=0.0, ge=0.0, le=1.0)

    state_write: bool = False
    state_read: bool = False
    cross_agent_message: bool = False
    output_chars: int = Field(default=0, ge=0)
    memory_units: int = Field(default=0, ge=0)

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
    )
    @classmethod
    def validate_required_text(cls, value: str, info):
        return _clean_nonblank(value, info.field_name)

    @field_validator("obstacle_id", "parent_action_id")
    @classmethod
    def validate_optional_text(cls, value: str | None, info):
        if value is None:
            return None
        return _clean_nonblank(value, info.field_name)


class TelemetryEvent(BaseModel):
    """Immutable, hash-chained event emitted after one synthetic action boundary."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    experiment_id: str = EXPERIMENT_ID
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

    tool_requested: str
    capability_requested: str
    resource_requested: str
    policy_rule_ids: tuple[str, ...]
    policy_permitted: bool
    request_denied: bool
    executed: bool
    action_result: str

    capability_in_scope: bool
    resource_in_scope: bool
    subgoal_in_scope: bool
    authority_granted: bool
    credential_in_scope: bool
    persistence_in_scope: bool
    coordination_in_scope: bool

    privilege_level: float = Field(ge=0.0, le=1.0)
    connectivity_level: float = Field(ge=0.0, le=1.0)
    persistence_level: float = Field(ge=0.0, le=1.0)
    coordination_level: float = Field(ge=0.0, le=1.0)
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
    output_chars: int = Field(default=0, ge=0)
    memory_units: int = Field(default=0, ge=0)

    previous_event_sha256: str | None = None
    event_sha256: str

    @field_validator(
        "trajectory_id",
        "sequence_id",
        "governed_subject_id",
        "action_id",
        "root_objective",
        "current_subgoal",
        "strategy_id",
        "tool_requested",
        "capability_requested",
        "resource_requested",
        "action_result",
        "event_sha256",
    )
    @classmethod
    def validate_required_text(cls, value: str, info):
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

    @property
    def evidence_ref(self) -> str:
        return f"event:{self.event_sha256}"

    def hash_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        payload.pop("event_sha256", None)
        return payload

    def verify_hash(self) -> bool:
        return canonical_sha256(self.hash_payload()) == self.event_sha256


def seal_event(payload: dict[str, Any]) -> TelemetryEvent:
    """Create a sealed event by hashing every field except the hash itself."""
    candidate = dict(payload)
    candidate.pop("event_sha256", None)
    digest = canonical_sha256(candidate)
    return TelemetryEvent.model_validate({**candidate, "event_sha256": digest})


def verify_event_chain(events: list[TelemetryEvent]) -> bool:
    """Verify per-event hashes, indices, identity continuity, and hash chaining."""
    if not events:
        return True
    first = events[0]
    identity = (
        first.experiment_id,
        first.trajectory_id,
        first.sequence_id,
        first.governed_subject_id,
        first.root_objective,
    )
    previous_hash: str | None = None
    for index, event in enumerate(events):
        if not event.verify_hash():
            return False
        if event.action_index != index:
            return False
        if (
            event.experiment_id,
            event.trajectory_id,
            event.sequence_id,
            event.governed_subject_id,
            event.root_objective,
        ) != identity:
            return False
        if event.previous_event_sha256 != previous_hash:
            return False
        previous_hash = event.event_sha256
    return True
