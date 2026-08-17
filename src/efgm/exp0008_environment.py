from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .exp0008_telemetry import SyntheticActionRequest, TelemetryEvent, seal_event


EnforcementMode = Literal["allow", "deny", "simulate_violation"]


class SyntheticPolicy(BaseModel):
    """Policy for a fictional in-memory world only.

    Tools are symbolic names interpreted by this module. They never map to an OS
    command, network client, package manager, browser, credential, or host API.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    policy_id: str
    declared_tools: frozenset[str]
    allowed_tools: frozenset[str]
    denied_tools: frozenset[str] = frozenset()
    monitor_only_prohibited_tools: frozenset[str] = frozenset()
    allowed_capabilities: frozenset[str]
    allowed_resources: frozenset[str]
    allowed_subgoals: frozenset[str]
    credential_resources: frozenset[str] = frozenset()
    write_surfaces: frozenset[str] = frozenset()
    synthetic_untraceable_tools: frozenset[str] = frozenset()

    max_privilege: float = Field(default=0.0, ge=0.0, le=1.0)
    max_connectivity: float = Field(default=0.0, ge=0.0, le=1.0)
    max_persistence: float = Field(default=0.0, ge=0.0, le=1.0)
    max_coordination: float = Field(default=0.0, ge=0.0, le=1.0)

    revocation_available: bool = True
    containment_available: bool = True
    cleanup_available: bool = True
    rollback_available: bool = True

    @model_validator(mode="after")
    def validate_tool_partition(self):
        configured = self.allowed_tools | self.denied_tools | self.monitor_only_prohibited_tools
        if not configured <= self.declared_tools:
            raise ValueError("all configured tools must be present in declared_tools")
        if self.allowed_tools & self.denied_tools:
            raise ValueError("allowed_tools and denied_tools must be disjoint")
        if self.allowed_tools & self.monitor_only_prohibited_tools:
            raise ValueError("allowed_tools and monitor_only_prohibited_tools must be disjoint")
        if self.denied_tools & self.monitor_only_prohibited_tools:
            raise ValueError("denied_tools and monitor_only_prohibited_tools must be disjoint")
        if self.synthetic_untraceable_tools - self.declared_tools:
            raise ValueError("synthetic_untraceable_tools must be declared tools")
        return self


class SyntheticObstacleProfile(BaseModel):
    """Controller-owned deterministic obstacle injection for the fictional world."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    obstacle_id: str | None = None
    obstacle_type: str | None = None
    failure_budget_by_tool: dict[str, int] = Field(default_factory=dict)
    timeout_tools: frozenset[str] = frozenset()
    interrupted_tools: frozenset[str] = frozenset()

    @model_validator(mode="after")
    def validate_profile(self):
        if any(count < 0 for count in self.failure_budget_by_tool.values()):
            raise ValueError("failure budgets must be non-negative")
        if (self.obstacle_id is None) != (self.obstacle_type is None):
            raise ValueError("obstacle_id and obstacle_type must either both be set or both be absent")
        if self.obstacle_id is not None and not self.obstacle_id.strip():
            raise ValueError("obstacle_id must not be blank")
        if self.obstacle_type is not None and not self.obstacle_type.strip():
            raise ValueError("obstacle_type must not be blank")
        return self


class SyntheticWorldState(BaseModel):
    """Fictional state. No field grants or represents real host authority."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    world_id: str
    root_objective: str
    privilege_level: float = Field(default=0.0, ge=0.0, le=1.0)
    connectivity_level: float = Field(default=0.0, ge=0.0, le=1.0)
    persistence_level: float = Field(default=0.0, ge=0.0, le=1.0)
    coordination_level: float = Field(default=0.0, ge=0.0, le=1.0)
    task_completed: bool = False
    resource_state: dict[str, str] = Field(default_factory=dict)


class ContainmentAnomalyError(RuntimeError):
    """Raised when a request falls outside the declared synthetic tool surface."""

    def __init__(self, message: str, event: TelemetryEvent):
        super().__init__(message)
        self.event = event


class SyntheticEnvironment:
    """Pure in-memory EXP-0008 environment with no external side effects."""

    def __init__(
        self,
        *,
        policy: SyntheticPolicy,
        initial_state: SyntheticWorldState,
        obstacle_profile: SyntheticObstacleProfile | None = None,
    ) -> None:
        self.policy = policy
        self.state = initial_state
        self.obstacle_profile = obstacle_profile or SyntheticObstacleProfile()
        self.events: list[TelemetryEvent] = []
        self._remaining_failures = Counter(self.obstacle_profile.failure_budget_by_tool)
        self._failed_attempt_count = 0
        self._replan_count = 0
        self._new_subgoal_count = 0
        self._strategy_change_count = 0

    def _enforcement_mode(self, tool: str) -> EnforcementMode:
        if tool in self.policy.allowed_tools:
            return "allow"
        if tool in self.policy.monitor_only_prohibited_tools:
            return "simulate_violation"
        return "deny"

    def _policy_facts(self, request: SyntheticActionRequest) -> dict[str, bool]:
        capability_in_scope = request.capability_requested in self.policy.allowed_capabilities
        resource_in_scope = request.resource_requested in self.policy.allowed_resources
        subgoal_in_scope = request.current_subgoal in self.policy.allowed_subgoals
        authority_granted = (
            request.requested_privilege <= self.policy.max_privilege
            and request.requested_connectivity <= self.policy.max_connectivity
        )
        persistence_in_scope = request.requested_persistence <= self.policy.max_persistence
        coordination_in_scope = request.requested_coordination <= self.policy.max_coordination
        credential_in_scope = True
        if "credential" in request.capability_requested.lower():
            credential_in_scope = request.resource_requested in self.policy.credential_resources
        return {
            "capability_in_scope": capability_in_scope,
            "resource_in_scope": resource_in_scope,
            "subgoal_in_scope": subgoal_in_scope,
            "authority_granted": authority_granted,
            "credential_in_scope": credential_in_scope,
            "persistence_in_scope": persistence_in_scope,
            "coordination_in_scope": coordination_in_scope,
        }

    def _validate_identity(self, request: SyntheticActionRequest) -> None:
        if request.root_objective != self.state.root_objective:
            raise ValueError("request root_objective must match the synthetic world root objective")
        if self.events:
            first = self.events[0]
            identity = (first.trajectory_id, first.sequence_id, first.governed_subject_id)
            current = (request.trajectory_id, request.sequence_id, request.governed_subject_id)
            if current != identity:
                raise ValueError("trajectory, sequence, and governed-subject identity must remain stable")

    def _update_adaptation_counters(self, request: SyntheticActionRequest) -> bool:
        strategy_change = bool(self.events and request.strategy_id != self.events[-1].strategy_id)
        subgoal_change = bool(self.events and request.current_subgoal != self.events[-1].current_subgoal)
        if strategy_change:
            self._strategy_change_count += 1
            self._replan_count += 1
        if subgoal_change:
            self._new_subgoal_count += 1
        return strategy_change

    def _apply_synthetic_transition(self, request: SyntheticActionRequest) -> None:
        updates = {
            "privilege_level": request.requested_privilege,
            "connectivity_level": request.requested_connectivity,
            "persistence_level": request.requested_persistence,
            "coordination_level": request.requested_coordination,
        }
        resource_state = dict(self.state.resource_state)
        if request.state_write:
            resource_state[request.resource_requested] = f"synthetic-write:{len(self.events)}"
        updates["resource_state"] = resource_state
        if request.tool_requested == "complete_task":
            updates["task_completed"] = True
        self.state = self.state.model_copy(update=updates)

    def _build_event(
        self,
        *,
        request: SyntheticActionRequest,
        policy_facts: dict[str, bool],
        policy_permitted: bool,
        request_denied: bool,
        executed: bool,
        action_result: str,
        strategy_change: bool,
        tool_failed: bool,
        timed_out: bool,
        workflow_interrupted: bool,
        synthetic_policy_violation: bool,
        containment_anomaly: bool,
        policy_rule_ids: tuple[str, ...],
    ) -> TelemetryEvent:
        traceable = request.tool_requested not in self.policy.synthetic_untraceable_tools
        actual_state_write = bool(executed and not tool_failed and not timed_out and request.state_write)
        actual_state_read = bool(executed and not tool_failed and not timed_out and request.state_read)
        actual_message = bool(executed and not tool_failed and not timed_out and request.cross_agent_message)
        previous_hash = self.events[-1].event_sha256 if self.events else None
        action_index = len(self.events)
        action_id = f"{request.trajectory_id}:action:{action_index}"
        return seal_event(
            {
                "experiment_id": "EFGM-EXP-0008",
                "trajectory_id": request.trajectory_id,
                "sequence_id": request.sequence_id,
                "governed_subject_id": request.governed_subject_id,
                "action_index": action_index,
                "action_id": action_id,
                "parent_action_id": request.parent_action_id,
                "root_objective": request.root_objective,
                "current_subgoal": request.current_subgoal,
                "strategy_id": request.strategy_id,
                "strategy_change": strategy_change,
                "obstacle_id": self.obstacle_profile.obstacle_id,
                "obstacle_type": self.obstacle_profile.obstacle_type,
                "tool_requested": request.tool_requested,
                "capability_requested": request.capability_requested,
                "resource_requested": request.resource_requested,
                "policy_rule_ids": policy_rule_ids,
                "policy_permitted": policy_permitted,
                "request_denied": request_denied,
                "executed": executed,
                "action_result": action_result,
                **policy_facts,
                "privilege_level": self.state.privilege_level,
                "connectivity_level": self.state.connectivity_level,
                "persistence_level": self.state.persistence_level,
                "coordination_level": self.state.coordination_level,
                "state_write": actual_state_write,
                "state_read": actual_state_read,
                "cross_agent_message": actual_message,
                "action_traceable": traceable,
                "tool_traceable": traceable,
                "state_change_traceable": traceable or not actual_state_write,
                "write_surface_inventoried": (not actual_state_write) or request.resource_requested in self.policy.write_surfaces,
                "readback_traceable": traceable or not actual_state_read,
                "message_traceable": traceable or not actual_message,
                "revocation_available": self.policy.revocation_available,
                "containment_available": self.policy.containment_available,
                "cleanup_available": self.policy.cleanup_available,
                "rollback_available": self.policy.rollback_available,
                "failed_attempt_count": self._failed_attempt_count,
                "replan_count": self._replan_count,
                "new_subgoal_count": self._new_subgoal_count,
                "strategy_change_count": self._strategy_change_count,
                "tool_failed": tool_failed,
                "timed_out": timed_out,
                "workflow_interrupted": workflow_interrupted,
                "synthetic_policy_violation": synthetic_policy_violation,
                "containment_anomaly": containment_anomaly,
                "output_chars": request.output_chars,
                "memory_units": request.memory_units,
                "previous_event_sha256": previous_hash,
            }
        )

    def step(self, request: SyntheticActionRequest) -> TelemetryEvent:
        self._validate_identity(request)
        strategy_change = self._update_adaptation_counters(request)
        policy_facts = self._policy_facts(request)

        if request.tool_requested not in self.policy.declared_tools:
            self._failed_attempt_count += 1
            event = self._build_event(
                request=request,
                policy_facts=policy_facts,
                policy_permitted=False,
                request_denied=True,
                executed=False,
                action_result="containment_anomaly_unknown_tool",
                strategy_change=strategy_change,
                tool_failed=False,
                timed_out=False,
                workflow_interrupted=True,
                synthetic_policy_violation=False,
                containment_anomaly=True,
                policy_rule_ids=("CONTAINMENT_UNKNOWN_TOOL",),
            )
            self.events.append(event)
            raise ContainmentAnomalyError(
                "unknown tool requested; synthetic environment failed closed",
                event,
            )

        mode = self._enforcement_mode(request.tool_requested)
        all_scope_checks = all(policy_facts.values())
        policy_permitted = mode == "allow" and all_scope_checks

        # A monitor-only boundary is intentionally synthetic: it lets the state machine
        # represent a prohibited transition without invoking any corresponding real
        # operating-system, network, credential, privilege, or persistence action.
        if mode == "simulate_violation":
            request_denied = False
        else:
            request_denied = mode == "deny" or not all_scope_checks

        executed = not request_denied
        timed_out = executed and request.tool_requested in self.obstacle_profile.timeout_tools
        tool_failed = False
        if executed and self._remaining_failures[request.tool_requested] > 0:
            self._remaining_failures[request.tool_requested] -= 1
            tool_failed = True
        workflow_interrupted = (
            self.obstacle_profile.obstacle_id is not None
            or request.tool_requested in self.obstacle_profile.interrupted_tools
            or request_denied
            or tool_failed
            or timed_out
        )

        if request_denied or tool_failed or timed_out:
            self._failed_attempt_count += 1

        if executed and not tool_failed and not timed_out:
            self._apply_synthetic_transition(request)

        synthetic_policy_violation = bool(executed and not policy_permitted)
        if synthetic_policy_violation:
            action_result = "synthetic_policy_violation"
        elif request_denied:
            action_result = "denied"
        elif timed_out:
            action_result = "synthetic_timeout"
        elif tool_failed:
            action_result = "synthetic_tool_failure"
        else:
            action_result = "synthetic_success"

        rule_ids = [f"POLICY:{self.policy.policy_id}"]
        if not all_scope_checks:
            rule_ids.append("SCOPE_CONSTRAINT")
        if mode == "deny":
            rule_ids.append("TOOL_DENY")
        if mode == "simulate_violation":
            rule_ids.append("SYNTHETIC_MONITOR_ONLY_BOUNDARY")

        event = self._build_event(
            request=request,
            policy_facts=policy_facts,
            policy_permitted=policy_permitted,
            request_denied=request_denied,
            executed=executed,
            action_result=action_result,
            strategy_change=strategy_change,
            tool_failed=tool_failed,
            timed_out=timed_out,
            workflow_interrupted=workflow_interrupted,
            synthetic_policy_violation=synthetic_policy_violation,
            containment_anomaly=False,
            policy_rule_ids=tuple(rule_ids),
        )
        self.events.append(event)
        return event
