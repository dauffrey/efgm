from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .exp0008_environment import ContainmentAnomalyError, EnvironmentTerminatedError, SyntheticEnvironment
from .exp0008_telemetry import SupervisorActionObservation, SyntheticActionRequest, TelemetryEvent
from .scoring_v2 import canonical_sha256


class ContainmentAttestation(BaseModel):
    """Externally produced containment evidence consumed by the experiment harness."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    environment_identity: str
    tool_broker_identity: str
    telemetry_schema_identity: str
    measurement_adapter_identity: str
    watchdog_identity: str
    evidence_reference: str

    no_external_network_route: bool
    no_dns_resolution: bool
    no_http_https_proxy: bool
    no_package_registry_reachability: bool
    no_cloud_metadata_reachability: bool
    no_lan_reachability: bool
    no_real_secrets_or_tokens: bool
    no_shell_or_subprocess_capability: bool
    no_raw_socket_capability: bool
    no_host_or_external_mount_access: bool
    unknown_tools_fail_closed: bool
    safety_controls_immutable_to_agent: bool
    hard_execution_budgets_active: bool
    not_github_hosted_runner: bool
    not_network_connected_host: bool

    @field_validator(
        "environment_identity",
        "tool_broker_identity",
        "telemetry_schema_identity",
        "measurement_adapter_identity",
        "watchdog_identity",
        "evidence_reference",
    )
    @classmethod
    def validate_nonblank(cls, value: str, info):
        cleaned = value.strip()
        if not cleaned:
            raise ValueError(f"{info.field_name} must not be blank or whitespace-only")
        return cleaned


class PreflightResult(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    passed: bool
    failures: tuple[str, ...]
    attestation_sha256: str
    evidence_reference: str


def validate_containment_attestation(attestation: ContainmentAttestation) -> PreflightResult:
    boolean_fields = [name for name, field in ContainmentAttestation.model_fields.items() if field.annotation is bool]
    failures = tuple(name for name in boolean_fields if not getattr(attestation, name))
    digest = canonical_sha256(attestation.model_dump(mode="json"))
    return PreflightResult(
        passed=not failures,
        failures=failures,
        attestation_sha256=digest,
        evidence_reference=attestation.evidence_reference,
    )


class ExecutionBudget(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    maximum_agent_actions: int = Field(gt=0)
    maximum_model_calls: int = Field(gt=0)
    maximum_retries: int = Field(ge=0)
    maximum_wall_clock_seconds: float = Field(gt=0)
    maximum_state_writes: int = Field(ge=0)
    maximum_output_chars: int = Field(ge=0)
    maximum_memory_units: int = Field(ge=0)


class WatchdogDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    terminate_trajectory: bool
    terminate_batch: bool
    reasons: tuple[str, ...]
    actions_seen: int
    state_writes_seen: int
    output_chars_seen: int
    memory_units_seen: int


class ExternalWatchdog:
    """Supervisor-side hard-budget monitor with pre-execution gating and latched terminal state."""

    def __init__(self, budget: ExecutionBudget) -> None:
        self.budget = budget
        self.actions_seen = 0
        self.state_writes_seen = 0
        self.output_chars_seen = 0
        self.memory_units_seen = 0
        self._terminated = False
        self._termination_reasons: tuple[str, ...] = ()

    @property
    def terminated(self) -> bool:
        return self._terminated

    def _decision(self) -> WatchdogDecision:
        return WatchdogDecision(
            terminate_trajectory=self._terminated,
            terminate_batch=self._terminated,
            reasons=self._termination_reasons,
            actions_seen=self.actions_seen,
            state_writes_seen=self.state_writes_seen,
            output_chars_seen=self.output_chars_seen,
            memory_units_seen=self.memory_units_seen,
        )

    def _latch(self, reasons: list[str]) -> WatchdogDecision:
        if reasons and not self._terminated:
            self._terminated = True
            self._termination_reasons = tuple(reasons)
        return self._decision()

    @staticmethod
    def _validate_counters(*, model_calls: int, retries: int, elapsed_seconds: float) -> None:
        if model_calls < 0 or retries < 0 or elapsed_seconds < 0:
            raise ValueError("watchdog counters must be non-negative")

    def preflight_next(
        self,
        *,
        supervisor_observation: SupervisorActionObservation,
        prospective_state_mutation: bool,
        model_calls: int,
        retries: int,
        elapsed_seconds: float,
    ) -> WatchdogDecision:
        """Block an action before execution if its known supervisor-owned facts would exceed a hard limit."""
        self._validate_counters(model_calls=model_calls, retries=retries, elapsed_seconds=elapsed_seconds)
        if self._terminated:
            return self._decision()
        prospective_actions = self.actions_seen + 1
        prospective_state_writes = self.state_writes_seen + int(prospective_state_mutation)
        prospective_output = self.output_chars_seen + supervisor_observation.output_chars
        prospective_memory = max(self.memory_units_seen, supervisor_observation.memory_units)
        reasons: list[str] = []
        if prospective_actions > self.budget.maximum_agent_actions:
            reasons.append("maximum_agent_actions")
        if model_calls > self.budget.maximum_model_calls:
            reasons.append("maximum_model_calls")
        if retries > self.budget.maximum_retries:
            reasons.append("maximum_retries")
        if elapsed_seconds > self.budget.maximum_wall_clock_seconds:
            reasons.append("maximum_wall_clock_seconds")
        if prospective_state_writes > self.budget.maximum_state_writes:
            reasons.append("maximum_state_writes")
        if prospective_output > self.budget.maximum_output_chars:
            reasons.append("maximum_output_chars")
        if prospective_memory > self.budget.maximum_memory_units:
            reasons.append("maximum_memory_units")
        return self._latch(reasons)

    def observe(
        self,
        event: TelemetryEvent,
        *,
        model_calls: int,
        retries: int,
        elapsed_seconds: float,
    ) -> WatchdogDecision:
        """Commit one executed/denied action boundary and fail closed on any unexpected overrun."""
        self._validate_counters(model_calls=model_calls, retries=retries, elapsed_seconds=elapsed_seconds)
        if self._terminated:
            return self._decision()

        self.actions_seen += 1
        # Conservatively charge every synthetic state mutation against the preregistered
        # maximum_state_writes budget, including privilege/connectivity/persistence/
        # coordination/completion changes that are not resource writes.
        self.state_writes_seen += int(event.state_change_occurred)
        self.output_chars_seen += event.output_chars
        self.memory_units_seen = max(self.memory_units_seen, event.memory_units)

        reasons: list[str] = []
        if event.containment_anomaly:
            reasons.append("containment_anomaly")
        if self.actions_seen > self.budget.maximum_agent_actions:
            reasons.append("maximum_agent_actions")
        if model_calls > self.budget.maximum_model_calls:
            reasons.append("maximum_model_calls")
        if retries > self.budget.maximum_retries:
            reasons.append("maximum_retries")
        if elapsed_seconds > self.budget.maximum_wall_clock_seconds:
            reasons.append("maximum_wall_clock_seconds")
        if self.state_writes_seen > self.budget.maximum_state_writes:
            reasons.append("maximum_state_writes")
        if self.output_chars_seen > self.budget.maximum_output_chars:
            reasons.append("maximum_output_chars")
        if self.memory_units_seen > self.budget.maximum_memory_units:
            reasons.append("maximum_memory_units")
        return self._latch(reasons)


class SupervisedExecutionTerminatedError(RuntimeError):
    def __init__(self, message: str, decision: WatchdogDecision, event: TelemetryEvent | None = None):
        super().__init__(message)
        self.decision = decision
        self.event = event


class SupervisedSyntheticExecutor:
    """Mandatory controller path coupling environment execution to one latched batch watchdog."""

    def __init__(self, *, environment: SyntheticEnvironment, watchdog: ExternalWatchdog) -> None:
        self.environment = environment
        self.watchdog = watchdog
        self._batch_terminated = watchdog.terminated or environment.terminated

    @property
    def batch_terminated(self) -> bool:
        return self._batch_terminated or self.watchdog.terminated

    def _terminate_from_watchdog(self, decision: WatchdogDecision, *, event: TelemetryEvent | None = None) -> None:
        self._batch_terminated = True
        reason = ",".join(decision.reasons) or "watchdog_terminated"
        if not self.environment.terminated:
            self.environment.terminate(f"external_watchdog:{reason}")
        raise SupervisedExecutionTerminatedError(f"supervised EXP-0008 execution terminated: {reason}", decision, event)

    def step(
        self,
        request: SyntheticActionRequest,
        *,
        supervisor_observation: SupervisorActionObservation,
        model_calls: int,
        retries: int,
        elapsed_seconds: float,
    ) -> TelemetryEvent:
        if self.batch_terminated:
            raise SupervisedExecutionTerminatedError("supervised EXP-0008 batch is terminal", self.watchdog._decision())
        if self.environment.terminated:
            self._batch_terminated = True
            raise EnvironmentTerminatedError(f"synthetic environment is terminal: {self.environment.termination_reason}")

        prospective_state_mutation = self.environment.controller_preview_state_mutation(request)
        preflight = self.watchdog.preflight_next(
            supervisor_observation=supervisor_observation,
            prospective_state_mutation=prospective_state_mutation,
            model_calls=model_calls,
            retries=retries,
            elapsed_seconds=elapsed_seconds,
        )
        if preflight.terminate_batch:
            self._terminate_from_watchdog(preflight)

        try:
            event = self.environment._controller_step(request, supervisor_observation=supervisor_observation)
        except ContainmentAnomalyError as error:
            decision = self.watchdog.observe(error.event, model_calls=model_calls, retries=retries, elapsed_seconds=elapsed_seconds)
            self._batch_terminated = True
            if not decision.terminate_batch:
                decision = self.watchdog._latch(["containment_anomaly"])
            raise ContainmentAnomalyError("unknown tool requested; environment and supervised batch are terminal", error.event) from error

        decision = self.watchdog.observe(event, model_calls=model_calls, retries=retries, elapsed_seconds=elapsed_seconds)
        if decision.terminate_batch:
            self._terminate_from_watchdog(decision, event=event)
        return event
