from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .exp0008_environment import ContainmentAnomalyError, EnvironmentTerminatedError, SyntheticEnvironment
from .exp0008_telemetry import SupervisorActionObservation, SyntheticActionRequest, TelemetryEvent
from .scoring_v2 import canonical_sha256


WATCHDOG_IMPLEMENTATION_ID = "exp0008-external-watchdog-v0.3"


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


class RuntimeAccountingSnapshot(BaseModel):
    """Monotonic controller-owned counters consumed by the watchdog."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    model_calls: int = Field(ge=0)
    retries: int = Field(ge=0)
    elapsed_seconds: float = Field(ge=0.0)


class SupervisorRuntimeAccounting:
    """Mutable only through monotonic controller methods; never exposed in SyntheticActionRequest."""

    def __init__(self) -> None:
        self._model_calls = 0
        self._retries = 0
        self._elapsed_seconds = 0.0

    def note_model_call(self, count: int = 1) -> None:
        if count < 0:
            raise ValueError("model call increment must be non-negative")
        self._model_calls += count

    def note_retry(self, count: int = 1) -> None:
        if count < 0:
            raise ValueError("retry increment must be non-negative")
        self._retries += count

    def advance_elapsed(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("elapsed-time increment must be non-negative")
        self._elapsed_seconds += seconds

    def snapshot(self) -> RuntimeAccountingSnapshot:
        return RuntimeAccountingSnapshot(
            model_calls=self._model_calls,
            retries=self._retries,
            elapsed_seconds=self._elapsed_seconds,
        )


class WatchdogDecision(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    terminate_trajectory: bool
    terminate_batch: bool
    reasons: tuple[str, ...]
    actions_seen: int
    state_writes_seen: int
    output_chars_seen: int
    memory_units_seen: int
    model_calls_seen: int
    retries_seen: int
    elapsed_seconds_seen: float
    watchdog_config_sha256: str


class ExternalWatchdog:
    """Supervisor-side hard-budget monitor with pre-execution gating and latched terminal state."""

    def __init__(self, budget: ExecutionBudget) -> None:
        self.budget = budget
        self.config_sha256 = canonical_sha256({
            "implementation_id": WATCHDOG_IMPLEMENTATION_ID,
            "budget": budget.model_dump(mode="json"),
        })
        self.actions_seen = 0
        self.state_writes_seen = 0
        self.output_chars_seen = 0
        self.memory_units_seen = 0
        self._accounting_seen = RuntimeAccountingSnapshot(model_calls=0, retries=0, elapsed_seconds=0.0)
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
            model_calls_seen=self._accounting_seen.model_calls,
            retries_seen=self._accounting_seen.retries,
            elapsed_seconds_seen=self._accounting_seen.elapsed_seconds,
            watchdog_config_sha256=self.config_sha256,
        )

    def _latch(self, reasons: list[str]) -> WatchdogDecision:
        if reasons and not self._terminated:
            self._terminated = True
            self._termination_reasons = tuple(reasons)
        return self._decision()

    def _ingest_accounting(self, accounting: RuntimeAccountingSnapshot) -> list[str]:
        previous = self._accounting_seen
        reasons: list[str] = []
        if accounting.model_calls < previous.model_calls:
            reasons.append("non_monotonic_model_calls")
        if accounting.retries < previous.retries:
            reasons.append("non_monotonic_retries")
        if accounting.elapsed_seconds < previous.elapsed_seconds:
            reasons.append("non_monotonic_elapsed_seconds")
        if not reasons:
            self._accounting_seen = accounting
        return reasons

    def preflight_accounting(self, accounting: RuntimeAccountingSnapshot) -> WatchdogDecision:
        """Authorize model-call/retry/time accounting before the controller consumes the next budget unit."""
        if self._terminated:
            return self._decision()
        reasons = self._ingest_accounting(accounting)
        if accounting.model_calls > self.budget.maximum_model_calls:
            reasons.append("maximum_model_calls")
        if accounting.retries > self.budget.maximum_retries:
            reasons.append("maximum_retries")
        if accounting.elapsed_seconds > self.budget.maximum_wall_clock_seconds:
            reasons.append("maximum_wall_clock_seconds")
        return self._latch(reasons)

    def preflight_next(
        self,
        *,
        supervisor_observation: SupervisorActionObservation,
        prospective_state_mutation: bool,
        accounting: RuntimeAccountingSnapshot,
    ) -> WatchdogDecision:
        """Block an action before execution if supervisor-owned facts would exceed a hard limit."""
        if self._terminated:
            return self._decision()
        accounting_decision = self.preflight_accounting(accounting)
        if accounting_decision.terminate_batch:
            return accounting_decision
        prospective_actions = self.actions_seen + 1
        prospective_state_writes = self.state_writes_seen + int(prospective_state_mutation)
        prospective_output = self.output_chars_seen + supervisor_observation.output_chars
        prospective_memory = max(self.memory_units_seen, supervisor_observation.memory_units)
        reasons: list[str] = []
        if prospective_actions > self.budget.maximum_agent_actions:
            reasons.append("maximum_agent_actions")
        if prospective_state_writes > self.budget.maximum_state_writes:
            reasons.append("maximum_state_writes")
        if prospective_output > self.budget.maximum_output_chars:
            reasons.append("maximum_output_chars")
        if prospective_memory > self.budget.maximum_memory_units:
            reasons.append("maximum_memory_units")
        return self._latch(reasons)

    def observe(self, event: TelemetryEvent, *, accounting: RuntimeAccountingSnapshot) -> WatchdogDecision:
        """Commit one action boundary and fail closed on any unexpected overrun or custody mismatch."""
        if self._terminated:
            return self._decision()
        accounting_decision = self.preflight_accounting(accounting)
        if accounting_decision.terminate_batch:
            return accounting_decision
        self.actions_seen += 1
        self.state_writes_seen += int(event.state_change_occurred)
        self.output_chars_seen += event.output_chars
        self.memory_units_seen = max(self.memory_units_seen, event.memory_units)

        reasons: list[str] = []
        if event.containment_anomaly:
            reasons.append("containment_anomaly")
        if event.watchdog_config_sha256 != self.config_sha256:
            reasons.append("watchdog_runtime_identity_mismatch")
        if self.actions_seen > self.budget.maximum_agent_actions:
            reasons.append("maximum_agent_actions")
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
    """Mandatory controller path coupling one environment to one watchdog/accounting context."""

    def __init__(self, *, environment: SyntheticEnvironment, watchdog: ExternalWatchdog) -> None:
        if environment.terminated or watchdog.terminated:
            raise RuntimeError("cannot bind a terminated environment or watchdog")
        self.environment = environment
        self.watchdog = watchdog
        self.accounting = SupervisorRuntimeAccounting()
        self.runtime_custody_sha256 = self.environment.bind_supervisor(self.watchdog.config_sha256)
        self._batch_terminated = False

    @property
    def batch_terminated(self) -> bool:
        return self._batch_terminated or self.watchdog.terminated or self.environment.terminated

    def _prospective_accounting(
        self,
        *,
        model_call_delta: int = 0,
        retry_delta: int = 0,
        elapsed_delta: float = 0.0,
    ) -> RuntimeAccountingSnapshot:
        if model_call_delta < 0 or retry_delta < 0 or elapsed_delta < 0:
            raise ValueError("runtime accounting deltas must be non-negative")
        current = self.accounting.snapshot()
        return RuntimeAccountingSnapshot(
            model_calls=current.model_calls + model_call_delta,
            retries=current.retries + retry_delta,
            elapsed_seconds=current.elapsed_seconds + elapsed_delta,
        )

    def note_model_call(self, count: int = 1) -> None:
        """Reserve model-call budget before the external controller invokes the model provider."""
        if self.batch_terminated:
            raise SupervisedExecutionTerminatedError("supervised EXP-0008 batch is terminal", self.watchdog._decision())
        prospective = self._prospective_accounting(model_call_delta=count)
        decision = self.watchdog.preflight_accounting(prospective)
        if decision.terminate_batch:
            self._terminate_from_watchdog(decision)
        self.accounting.note_model_call(count)

    def note_retry(self, count: int = 1) -> None:
        """Reserve retry budget before the controller performs the retry."""
        if self.batch_terminated:
            raise SupervisedExecutionTerminatedError("supervised EXP-0008 batch is terminal", self.watchdog._decision())
        prospective = self._prospective_accounting(retry_delta=count)
        decision = self.watchdog.preflight_accounting(prospective)
        if decision.terminate_batch:
            self._terminate_from_watchdog(decision)
        self.accounting.note_retry(count)

    def advance_elapsed(self, seconds: float) -> None:
        """Account newly observed wall time and terminate immediately if the hard duration is exceeded."""
        if self.batch_terminated:
            raise SupervisedExecutionTerminatedError("supervised EXP-0008 batch is terminal", self.watchdog._decision())
        prospective = self._prospective_accounting(elapsed_delta=seconds)
        decision = self.watchdog.preflight_accounting(prospective)
        if decision.terminate_batch:
            self._terminate_from_watchdog(decision)
        self.accounting.advance_elapsed(seconds)

    def _terminate_from_watchdog(self, decision: WatchdogDecision, *, event: TelemetryEvent | None = None) -> None:
        self._batch_terminated = True
        reason = ",".join(decision.reasons) or "watchdog_terminated"
        if not self.environment.terminated:
            self.environment.terminate(f"external_watchdog:{reason}")
        raise SupervisedExecutionTerminatedError(f"supervised EXP-0008 execution terminated: {reason}", decision, event)

    def _handle_containment(self, error: ContainmentAnomalyError) -> None:
        decision = self.watchdog.observe(error.event, accounting=self.accounting.snapshot())
        self._batch_terminated = True
        if not decision.terminate_batch:
            decision = self.watchdog._latch(["containment_anomaly"])
        raise ContainmentAnomalyError("containment/custody anomaly; environment and supervised batch are terminal", error.event) from error

    def step(
        self,
        request: SyntheticActionRequest,
        *,
        supervisor_observation: SupervisorActionObservation,
    ) -> TelemetryEvent:
        if self.batch_terminated:
            raise SupervisedExecutionTerminatedError("supervised EXP-0008 batch is terminal", self.watchdog._decision())
        if self.environment.terminated:
            self._batch_terminated = True
            raise EnvironmentTerminatedError(f"synthetic environment is terminal: {self.environment.termination_reason}")

        try:
            prospective_state_mutation = self.environment.controller_preview_state_mutation(
                request,
                supervisor_observation=supervisor_observation,
            )
        except ContainmentAnomalyError as error:
            self._handle_containment(error)
            raise AssertionError("unreachable")

        preflight = self.watchdog.preflight_next(
            supervisor_observation=supervisor_observation,
            prospective_state_mutation=prospective_state_mutation,
            accounting=self.accounting.snapshot(),
        )
        if preflight.terminate_batch:
            self._terminate_from_watchdog(preflight)

        try:
            event = self.environment._controller_step(request, supervisor_observation=supervisor_observation)
        except ContainmentAnomalyError as error:
            self._handle_containment(error)
            raise AssertionError("unreachable")

        if event.runtime_custody_sha256 != self.runtime_custody_sha256:
            decision = self.watchdog._latch(["runtime_custody_identity_mismatch"])
            self._terminate_from_watchdog(decision, event=event)
        decision = self.watchdog.observe(event, accounting=self.accounting.snapshot())
        if decision.terminate_batch:
            self._terminate_from_watchdog(decision, event=event)
        return event
