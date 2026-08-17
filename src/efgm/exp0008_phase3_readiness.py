from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, ValidationError, model_validator

from .exp0008_safety import (
    ContainmentAttestation,
    SupervisedExecutionTerminatedError,
    SupervisedSyntheticExecutor,
    validate_containment_attestation,
)
from .exp0008_telemetry import SyntheticActionRequest
from .scoring_v2 import canonical_sha256


EXPERIMENT_ID = "EFGM-EXP-0008"
PHASE_ID = "phase_3_containment_readiness"
READINESS_IMPLEMENTATION_ID = "exp0008-phase3-readiness-v0.1"
PHASE2_BASELINE_SHA = "620dd9b85f7f05f0f04e4e34a69165510030535b"
PHASE2_BASELINE_REF = "baseline/exp0008-phase2-instruments-2026-08-17"
PHASE2_FREEZE_RECORD_SHA256 = "6efe4415ef64208fa8b1f1e6918d2e8d1739dbdd7150245138932b2e67c2b547"
FROZEN_RUNTIME_INSTRUMENT_SET_SHA256 = "1be866e307e5dd8ccaee7307ae0e6e4a8cc7d756595312e0820aaadcd7b8ce08"
FROZEN_PHASE2_REPORT_SHA256 = "94d9b7bad0024ff88dce942ba654bebfbc0749ed0cdd0bd343c5cfd53a20cda8"

FROZEN_SOURCE_IDENTITIES = {
    "environment_and_tool_broker": "88405f8ff0eb2ea55ece6aaaf0036d0fc02d2173",
    "telemetry": "521fdfb16bea48c1c37d2f6642ab1bab053a8e15",
    "adapter": "c417bc5e72e152c9d462b605de14bd3ff3150735",
    "watchdog": "49037cd4561ac5ef83bb440ff7cc1c4340afe502",
    "simple_detectors_and_preexecution_comparator": "edc6a1bf59abcf6a4cb6409d09bd9d39014a176f",
    "preexecution_materializer": "c1e3a8f4392df3b31845d85795563a391809a0e2",
}


class Phase3AuthorizationRequiredError(RuntimeError):
    pass


class ControllerIsolationContract(BaseModel):
    """Declarative controller boundary. The autonomous model is a data producer, never a code/tool host."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    provider_credentials_location: Literal["external_controller_only"] = "external_controller_only"
    model_output_surface: Literal["synthetic_action_request_only"] = "synthetic_action_request_only"
    direct_environment_reference_exposed_to_model: Literal[False] = False
    direct_watchdog_reference_exposed_to_model: Literal[False] = False
    direct_telemetry_reference_exposed_to_model: Literal[False] = False
    provider_credentials_exposed_to_model: Literal[False] = False
    shell_or_subprocess_exposed_to_model: Literal[False] = False
    filesystem_exposed_to_model: Literal[False] = False
    network_or_socket_exposed_to_model: Literal[False] = False
    browser_or_http_exposed_to_model: Literal[False] = False
    package_manager_exposed_to_model: Literal[False] = False
    arbitrary_code_execution_exposed_to_model: Literal[False] = False
    docker_or_host_control_exposed_to_model: Literal[False] = False
    raw_model_output_executes: Literal[False] = False
    unknown_request_fields_fail_closed: Literal[True] = True
    tool_execution_requires_supervised_controller: Literal[True] = True


class ModelProposalEnvelope(BaseModel):
    """Only data accepted from a future model provider."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    request: SyntheticActionRequest


class ControllerIsolationBoundary:
    """Parser-only model boundary. It intentionally owns no environment, watchdog, provider, or credentials."""

    def __init__(self, contract: ControllerIsolationContract | None = None) -> None:
        self.contract = contract or ControllerIsolationContract()

    def parse_model_output(self, payload: dict[str, Any]) -> SyntheticActionRequest:
        return ModelProposalEnvelope.model_validate(payload).request


class ExternalContainmentEvidence(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    evidence_kind: Literal["external_preflight", "scripted_fixture"]
    phase2_freeze_record_sha256: str
    runtime_instrument_set_sha256: str
    attestation: ContainmentAttestation

    @model_validator(mode="after")
    def validate_nonblank(self):
        if not self.phase2_freeze_record_sha256.strip():
            raise ValueError("phase2_freeze_record_sha256 must not be blank")
        if not self.runtime_instrument_set_sha256.strip():
            raise ValueError("runtime_instrument_set_sha256 must not be blank")
        return self


class HumanSafetyApproval(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    authorized: bool = False
    approver_identity: str | None = None
    approval_reference: str | None = None

    @model_validator(mode="after")
    def validate_approval(self):
        if self.authorized:
            if self.approver_identity is None or not self.approver_identity.strip():
                raise ValueError("authorized human safety approval requires approver_identity")
            if self.approval_reference is None or not self.approval_reference.strip():
                raise ValueError("authorized human safety approval requires approval_reference")
        elif self.approver_identity is not None or self.approval_reference is not None:
            raise ValueError("approval identity/reference must be absent while authorization is false")
        return self


class ReadinessAssessment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    experiment_id: str = EXPERIMENT_ID
    phase: str = PHASE_ID
    readiness_implementation_id: str = READINESS_IMPLEMENTATION_ID
    phase2_baseline_sha: str = PHASE2_BASELINE_SHA
    phase2_freeze_record_sha256: str
    runtime_instrument_set_sha256: str
    isolation_contract_sha256: str
    containment_attestation_sha256: str
    mechanical_preflight_passed: bool
    external_containment_evidence_accepted: bool
    human_safety_approval_present: bool
    authorization_eligible: bool
    autonomous_execution_authorized: Literal[False] = False
    failures: tuple[str, ...]
    authorization_blockers: tuple[str, ...]
    assessment_sha256: str

    def hash_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        payload.pop("assessment_sha256", None)
        return payload

    def verify_hash(self) -> bool:
        return canonical_sha256(self.hash_payload()) == self.assessment_sha256


def _verify_phase2_freeze_record(record: dict[str, Any]) -> tuple[str, ...]:
    failures: list[str] = []
    supplied_hash = str(record.get("freeze_record_sha256", ""))
    payload = dict(record)
    payload.pop("freeze_record_sha256", None)
    if canonical_sha256(payload) != supplied_hash:
        failures.append("phase2_freeze_record_hash_mismatch")
    if supplied_hash != PHASE2_FREEZE_RECORD_SHA256:
        failures.append("phase2_freeze_record_identity_mismatch")
    if record.get("status") != "frozen":
        failures.append("phase2_instruments_not_frozen")
    if record.get("behavioral_identity", {}).get("runtime_instrument_set_sha256") != FROZEN_RUNTIME_INSTRUMENT_SET_SHA256:
        failures.append("runtime_instrument_set_identity_mismatch")
    if record.get("behavioral_identity", {}).get("canonical_report_sha256") != FROZEN_PHASE2_REPORT_SHA256:
        failures.append("phase2_report_identity_mismatch")
    boundaries = record.get("boundaries", {})
    if boundaries.get("scientific_evidence") is not False:
        failures.append("phase2_freeze_scientific_boundary_changed")
    if boundaries.get("autonomous_execution") is not False:
        failures.append("phase2_freeze_autonomous_boundary_changed")
    if boundaries.get("phase3_authorized") is not False:
        failures.append("phase2_freeze_phase3_boundary_changed")
    source_ids = record.get("source_identities", {})
    for name, expected in FROZEN_SOURCE_IDENTITIES.items():
        if source_ids.get(name) != expected:
            failures.append(f"frozen_source_identity_mismatch:{name}")
    return tuple(failures)


def _containment_identity_failures(evidence: ExternalContainmentEvidence) -> tuple[str, ...]:
    failures: list[str] = []
    attestation = evidence.attestation
    expected = {
        "environment_identity": FROZEN_SOURCE_IDENTITIES["environment_and_tool_broker"],
        "tool_broker_identity": FROZEN_SOURCE_IDENTITIES["environment_and_tool_broker"],
        "telemetry_schema_identity": FROZEN_SOURCE_IDENTITIES["telemetry"],
        "measurement_adapter_identity": FROZEN_SOURCE_IDENTITIES["adapter"],
        "watchdog_identity": FROZEN_SOURCE_IDENTITIES["watchdog"],
    }
    for field_name, expected_value in expected.items():
        if getattr(attestation, field_name) != expected_value:
            failures.append(f"containment_identity_mismatch:{field_name}")
    if evidence.phase2_freeze_record_sha256 != PHASE2_FREEZE_RECORD_SHA256:
        failures.append("containment_phase2_freeze_identity_mismatch")
    if evidence.runtime_instrument_set_sha256 != FROZEN_RUNTIME_INSTRUMENT_SET_SHA256:
        failures.append("containment_runtime_instrument_identity_mismatch")
    return tuple(failures)


def evaluate_phase3_readiness(
    *,
    phase2_freeze_record: dict[str, Any],
    containment_evidence: ExternalContainmentEvidence,
    isolation_contract: ControllerIsolationContract | None = None,
    human_approval: HumanSafetyApproval | None = None,
) -> ReadinessAssessment:
    """Evaluate readiness without invoking a model provider or authorizing autonomy by default."""

    contract = isolation_contract or ControllerIsolationContract()
    approval = human_approval or HumanSafetyApproval()

    failures = list(_verify_phase2_freeze_record(phase2_freeze_record))
    containment_result = validate_containment_attestation(containment_evidence.attestation)
    failures.extend(f"containment_attestation:{item}" for item in containment_result.failures)
    failures.extend(_containment_identity_failures(containment_evidence))

    mechanical_preflight_passed = not failures
    external_accepted = mechanical_preflight_passed and containment_evidence.evidence_kind == "external_preflight"
    human_present = approval.authorized

    blockers: list[str] = []
    if not mechanical_preflight_passed:
        blockers.append("mechanical_preflight_failed")
    if not external_accepted:
        blockers.append("external_containment_preflight_evidence_required")
    if not human_present:
        blockers.append("explicit_human_safety_approval_required")

    eligible = mechanical_preflight_passed and external_accepted and human_present
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "phase": PHASE_ID,
        "readiness_implementation_id": READINESS_IMPLEMENTATION_ID,
        "phase2_baseline_sha": PHASE2_BASELINE_SHA,
        "phase2_freeze_record_sha256": containment_evidence.phase2_freeze_record_sha256,
        "runtime_instrument_set_sha256": containment_evidence.runtime_instrument_set_sha256,
        "isolation_contract_sha256": canonical_sha256(contract.model_dump(mode="json")),
        "containment_attestation_sha256": containment_result.attestation_sha256,
        "mechanical_preflight_passed": mechanical_preflight_passed,
        "external_containment_evidence_accepted": external_accepted,
        "human_safety_approval_present": human_present,
        "authorization_eligible": eligible,
        "autonomous_execution_authorized": False,
        "failures": tuple(failures),
        "authorization_blockers": tuple(blockers),
    }
    return ReadinessAssessment(**payload, assessment_sha256=canonical_sha256(payload))


def require_autonomous_authorization(assessment: ReadinessAssessment) -> None:
    if not assessment.verify_hash():
        raise Phase3AuthorizationRequiredError("Phase-3 readiness assessment custody failed")
    blockers = ",".join(assessment.authorization_blockers)
    suffix = f": {blockers}" if blockers else ""
    raise Phase3AuthorizationRequiredError(
        "Phase-3 readiness cannot authorize autonomous execution; a separate explicit authorization artifact is required"
        + suffix
    )


def reserve_model_call_if_authorized(
    executor: SupervisedSyntheticExecutor,
    assessment: ReadinessAssessment,
) -> None:
    """Reserve watchdog budget before a future provider call; never performs the provider call itself."""

    require_autonomous_authorization(assessment)
    try:
        executor.note_model_call()
    except SupervisedExecutionTerminatedError:
        raise


def build_scripted_containment_fixture() -> ExternalContainmentEvidence:
    """CI-only fixture. It tests readiness mechanics and is deliberately inadmissible as real containment evidence."""

    attestation = ContainmentAttestation(
        environment_identity=FROZEN_SOURCE_IDENTITIES["environment_and_tool_broker"],
        tool_broker_identity=FROZEN_SOURCE_IDENTITIES["environment_and_tool_broker"],
        telemetry_schema_identity=FROZEN_SOURCE_IDENTITIES["telemetry"],
        measurement_adapter_identity=FROZEN_SOURCE_IDENTITIES["adapter"],
        watchdog_identity=FROZEN_SOURCE_IDENTITIES["watchdog"],
        evidence_reference="scripted-fixture:phase3-readiness",
        no_external_network_route=True,
        no_dns_resolution=True,
        no_http_https_proxy=True,
        no_package_registry_reachability=True,
        no_cloud_metadata_reachability=True,
        no_lan_reachability=True,
        no_real_secrets_or_tokens=True,
        no_shell_or_subprocess_capability=True,
        no_raw_socket_capability=True,
        no_host_or_external_mount_access=True,
        unknown_tools_fail_closed=True,
        safety_controls_immutable_to_agent=True,
        hard_execution_budgets_active=True,
        not_github_hosted_runner=True,
        not_network_connected_host=True,
    )
    return ExternalContainmentEvidence(
        evidence_kind="scripted_fixture",
        phase2_freeze_record_sha256=PHASE2_FREEZE_RECORD_SHA256,
        runtime_instrument_set_sha256=FROZEN_RUNTIME_INSTRUMENT_SET_SHA256,
        attestation=attestation,
    )


def default_freeze_artifact_path() -> Path:
    return Path(__file__).resolve().parents[2] / "experiments" / "manifests" / "EFGM-EXP-0008-phase2-instrument-freeze.json"


def _format_markdown(assessment: ReadinessAssessment) -> str:
    lines = [
        "# EFGM-EXP-0008 Phase 3 readiness mechanics",
        "",
        f"- Mechanical preflight: {'PASS' if assessment.mechanical_preflight_passed else 'FAIL'}",
        f"- External containment evidence accepted: {assessment.external_containment_evidence_accepted}",
        f"- Human safety approval present: {assessment.human_safety_approval_present}",
        f"- Authorization eligible: {assessment.authorization_eligible}",
        f"- Autonomous execution authorized: {assessment.autonomous_execution_authorized}",
        f"- Assessment SHA-256: `{assessment.assessment_sha256}`",
    ]
    if assessment.failures:
        lines.append(f"- Failures: {', '.join(assessment.failures)}")
    if assessment.authorization_blockers:
        lines.append(f"- Authorization blockers: {', '.join(assessment.authorization_blockers)}")
    lines.extend([
        "",
        "This command uses a scripted containment fixture only. It is not external containment evidence and cannot authorize Phase 3 autonomy.",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate EXP-0008 Phase 3 containment/readiness mechanics without autonomous execution.")
    parser.add_argument("--freeze-artifact", default=str(default_freeze_artifact_path()))
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args(argv)

    freeze_record = json.loads(Path(args.freeze_artifact).read_text(encoding="utf-8"))
    assessment = evaluate_phase3_readiness(
        phase2_freeze_record=freeze_record,
        containment_evidence=build_scripted_containment_fixture(),
    )
    if not assessment.mechanical_preflight_passed:
        raise SystemExit("Phase-3 readiness mechanics failed")
    if assessment.autonomous_execution_authorized:
        raise SystemExit("scripted readiness fixture must never authorize autonomous execution")

    if args.format == "json":
        print(json.dumps(assessment.model_dump(mode="json"), indent=2, sort_keys=True))
    else:
        print(_format_markdown(assessment))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
