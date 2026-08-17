from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .exp0008_telemetry import TelemetryEvent
from .scoring_v2 import canonical_sha256


class ContainmentAttestation(BaseModel):
    """Externally produced containment evidence consumed by the experiment harness.

    This model deliberately does not probe networks, filesystems, cloud metadata,
    credentials, or host capabilities itself. Those checks must be performed by an
    independent containment harness outside agent control, and their results are
    supplied here as immutable evidence.
    """

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
    """Fail closed unless every mandatory external containment assertion is true."""
    boolean_fields = [
        name
        for name, field in ContainmentAttestation.model_fields.items()
        if field.annotation is bool
    ]
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
    """Supervisor-side budget monitor that is never exposed as an agent tool."""

    def __init__(self, budget: ExecutionBudget) -> None:
        self.budget = budget
        self.actions_seen = 0
        self.state_writes_seen = 0
        self.output_chars_seen = 0
        self.memory_units_seen = 0

    def observe(
        self,
        event: TelemetryEvent,
        *,
        model_calls: int,
        retries: int,
        elapsed_seconds: float,
    ) -> WatchdogDecision:
        if model_calls < 0 or retries < 0 or elapsed_seconds < 0:
            raise ValueError("watchdog counters must be non-negative")

        self.actions_seen += 1
        self.state_writes_seen += int(event.state_write)
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

        terminate = bool(reasons)
        return WatchdogDecision(
            terminate_trajectory=terminate,
            terminate_batch=terminate,
            reasons=tuple(reasons),
            actions_seen=self.actions_seen,
            state_writes_seen=self.state_writes_seen,
            output_chars_seen=self.output_chars_seen,
            memory_units_seen=self.memory_units_seen,
        )
