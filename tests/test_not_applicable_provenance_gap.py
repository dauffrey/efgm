from copy import deepcopy

import pytest
from pydantic import ValidationError

from efgm.exp0004_sparse_governance import DEVELOPMENT_CASE_SPECS, _build_input
from efgm.schemas_v2 import MetricObservation
from efgm.scoring_v2 import ProvenanceError, score_decision_efgm
from efgm.scoring_v3 import score_agent_governance


def _unsupported_not_applicable() -> MetricObservation:
    return MetricObservation(
        status="not_applicable",
        rationale="Declared not applicable for falsification; no supporting evidence supplied.",
        evidence_refs=[],
        scorer_id="EFGM-CE-0005-falsification",
        scorer_type="human",
        confidence=0.0,
    )


def _supported_not_applicable(path: str) -> MetricObservation:
    return MetricObservation(
        status="not_applicable",
        rationale="Independent scope evidence establishes that this metric is not applicable to the assessed case.",
        evidence_refs=[f"experiment://EFGM-CE-0005/scope/{path}"],
        scorer_id="EFGM-CE-0005-scope-reviewer",
        scorer_type="human",
        confidence=0.95,
    )


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("evidence_refs", ["   "]),
        ("scorer_id", "\t"),
    ],
)
def test_blank_provenance_identifiers_are_rejected_at_schema_boundary(field_name, bad_value):
    payload = {
        "status": "not_applicable",
        "rationale": "Scope was independently reviewed.",
        "evidence_refs": ["experiment://EFGM-CE-0005/scope/control"],
        "scorer_id": "EFGM-CE-0005-reviewer",
        "scorer_type": "human",
        "confidence": 0.95,
    }
    payload[field_name] = bad_value

    with pytest.raises(ValidationError, match="blank|whitespace"):
        MetricObservation.model_validate(payload)


def test_whitespace_only_rationale_is_rejected_by_strict_provenance():
    spec = deepcopy(DEVELOPMENT_CASE_SPECS[0])
    assessment = _build_input(spec)
    assessment.decision.output_entropy.output_contradiction = MetricObservation(
        status="not_applicable",
        rationale="   ",
        evidence_refs=["experiment://EFGM-CE-0005/scope/rationale-control"],
        scorer_id="EFGM-CE-0005-reviewer",
        scorer_type="human",
        confidence=0.95,
    )

    with pytest.raises(ProvenanceError, match="missing rationale"):
        score_decision_efgm(assessment.decision, require_provenance=True)


def test_strict_v2_provenance_rejects_unsupported_na_that_would_remove_a_severe_penalty():
    spec = deepcopy(DEVELOPMENT_CASE_SPECS[0])
    assessment = _build_input(spec)

    assessment.decision.output_entropy.output_contradiction = MetricObservation(
        value=1.0,
        status="observed",
        rationale="A maximal output contradiction is explicitly evidenced for the control case.",
        evidence_refs=["experiment://EFGM-CE-0005/v2/output-contradiction"],
        scorer_id="EFGM-CE-0005-falsification",
        scorer_type="human",
        confidence=1.0,
    )
    observed = score_decision_efgm(assessment.decision, require_provenance=True)
    assert observed.classification == "Stable with watch items"
    assert observed.Eo == 0.2875

    assessment.decision.output_entropy.output_contradiction = _unsupported_not_applicable()
    with pytest.raises(ProvenanceError, match="not_applicable"):
        score_decision_efgm(assessment.decision, require_provenance=True)


def test_strict_v2_provenance_allows_evidence_backed_na_exclusion():
    spec = deepcopy(DEVELOPMENT_CASE_SPECS[0])
    assessment = _build_input(spec)
    assessment.decision.output_entropy.output_contradiction = _supported_not_applicable(
        "output_entropy.output_contradiction"
    )

    excluded = score_decision_efgm(assessment.decision, require_provenance=True)

    assert excluded.provenance_complete is True
    assert excluded.provenance_issues == []
    assert excluded.Eo == 0.05


def test_strict_agent_provenance_rejects_unsupported_na_that_would_erase_prerequisite():
    spec = next(
        deepcopy(item)
        for item in DEVELOPMENT_CASE_SPECS
        if item["target_path"] == "boundary_integrity.trust_boundary_adherence"
    )
    assessment = _build_input(spec)

    observed = score_agent_governance(assessment, require_provenance=True)
    assert "boundary_integrity.trust_boundary_adherence" in observed.candidate_prerequisite_breaches

    assessment.boundary_integrity.trust_boundary_adherence = _unsupported_not_applicable()
    with pytest.raises(ProvenanceError, match="not_applicable"):
        score_agent_governance(assessment, require_provenance=True)


def test_strict_agent_provenance_allows_evidence_backed_na_exclusion():
    spec = next(
        deepcopy(item)
        for item in DEVELOPMENT_CASE_SPECS
        if item["target_path"] == "boundary_integrity.trust_boundary_adherence"
    )
    assessment = _build_input(spec)
    assessment.boundary_integrity.trust_boundary_adherence = _supported_not_applicable(
        "boundary_integrity.trust_boundary_adherence"
    )

    excluded = score_agent_governance(assessment, require_provenance=True)

    assert excluded.provenance_complete is True
    assert excluded.provenance_issues == []
    assert "boundary_integrity.trust_boundary_adherence" not in excluded.candidate_prerequisite_breaches
