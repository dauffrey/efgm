"""Mechanical completeness checks for *candidate* causal explanation evidence.

This is not an internal model interpreter, evidence verifier, certification
engine, or authorization gate. The caller's fields are untrusted assertions.
"""
from dataclasses import dataclass
import re

_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_STATES = {"observed", "inferred", "unknown", "not_applicable"}
_CHECKS = ("causal_intervention", "negative_control", "independent_replication", "heldout_evaluation")
_FIELDS = frozenset({
    "schema_version", "claim_id", "mechanism", "model_sha256",
    "protocol_sha256", "development_dataset_sha256",
    "evaluation_dataset_sha256", "evidence_manifest_sha256",
    "proposer_id", "evaluator_id", "protocol_frozen_before_evaluation",
    "known_counterexample_count", *_CHECKS,
})


@dataclass(frozen=True)
class EvidenceDisposition:
    status: str
    reasons: tuple[str, ...]
    scientific_claim_validated: bool = False
    grants_authority: bool = False


def assess_interpretability_claim(record: object) -> EvidenceDisposition:
    """Classify record completeness, never the truth of a mechanistic claim.

    READY_FOR_EXTERNAL_AUDIT says only that the supplied *self-reported*
    fields pass elementary checks. Independently acquired source evidence,
    causal effect estimation, distributional tests and an external evaluator
    are still required before any scientific conclusion.
    """
    if type(record) is not dict or set(record) != _FIELDS:
        return EvidenceDisposition("INVALID", ("invalid_record_shape",))

    texts = ("claim_id", "mechanism", "proposer_id", "evaluator_id")
    hashes = ("model_sha256", "protocol_sha256", "development_dataset_sha256",
              "evaluation_dataset_sha256", "evidence_manifest_sha256")
    if type(record["schema_version"]) is not str or record["schema_version"] != "interpretability-evidence/0.1":
        return EvidenceDisposition("INVALID", ("unsupported_schema_version",))
    if any(type(record[k]) is not str or not record[k].strip() or record[k] != record[k].strip() for k in texts):
        return EvidenceDisposition("INVALID", ("invalid_text_identity",))
    if any(type(record[k]) is not str or _SHA256.fullmatch(record[k]) is None for k in hashes):
        return EvidenceDisposition("INVALID", ("invalid_sha256_identity",))
    if (type(record["protocol_frozen_before_evaluation"]) is not bool
            or type(record["known_counterexample_count"]) is not int
            or record["known_counterexample_count"] < 0
            or any(type(record[k]) is not str or record[k] not in _STATES for k in _CHECKS)):
        return EvidenceDisposition("INVALID", ("invalid_evidence_fields",))

    reasons = []
    if not record["protocol_frozen_before_evaluation"]:
        reasons.append("protocol_not_frozen")
    if record["proposer_id"] == record["evaluator_id"]:
        reasons.append("evaluator_not_separate")
    if record["development_dataset_sha256"] == record["evaluation_dataset_sha256"]:
        reasons.append("evaluation_identity_equals_development")
    if record["known_counterexample_count"]:
        reasons.append("counterexamples_need_adjudication")
    for key in _CHECKS:
        if record[key] != "observed":
            reasons.append(key + "_not_observed")
    if reasons:
        return EvidenceDisposition("INSUFFICIENT_EVIDENCE", tuple(sorted(reasons)))

    return EvidenceDisposition("READY_FOR_EXTERNAL_AUDIT", ())


__all__ = ["EvidenceDisposition", "assess_interpretability_claim"]
