from copy import deepcopy

import pytest
from pydantic import ValidationError

from efgm.schemas_v2 import EFGMDecisionInput, MetricObservation
from efgm.scoring_v2 import (
    IncompleteAssessmentError,
    ProvenanceError,
    load_scoring_config,
    score_decision_efgm,
)


def zeros(names: list[str]) -> dict[str, float]:
    return {name: 0.0 for name in names}


def base_payload() -> dict:
    return {
        "task_id": "v2-test",
        "T": 0.95,
        "C": 0.85,
        "flow_quality": {
            "task_completion_consistency": 0.92,
            "reasoning_continuity": 0.90,
            "semantic_coherence": 0.91,
            "verification_success_rate": 0.86,
        },
        "input_entropy": {
            "input_contradiction": 0.55,
            "input_ambiguity": 0.70,
            "input_goal_conflict": 0.45,
            "missing_context": 0.60,
            "hidden_information_load": 0.20,
        },
        "output_entropy": {
            "output_contradiction": 0.05,
            "uncertainty_mismatch": 0.10,
            "goal_drift": 0.05,
            "reasoning_instability": 0.00,
            "context_decay": 0.05,
        },
        "grounding": {
            "rule_support": 0.88,
            "evidence_validity": 0.86,
            "traceability": 0.90,
            "factual_consistency": 0.88,
            "domain_calibration": 0.88,
        },
        "uncertainty_calibration": 0.90,
        "behavioral_entropy": zeros([
            "chasing_behavior",
            "outcome_bias",
            "sunk_cost_pressure",
            "false_pattern_detection",
            "overconfidence_feedback",
        ]),
        "operational_entropy": zeros([
            "timeout_rate",
            "retry_instability",
            "tool_failure_rate",
            "latency_pressure",
            "workflow_interruption",
        ]),
        "outcome_quality": 0.90,
    }


def explicit_observation(value: float, ref: str) -> dict:
    return {
        "value": value,
        "status": "observed",
        "rationale": f"Test observation supported by {ref}.",
        "evidence_refs": [ref],
        "scorer_id": "test-reviewer",
        "scorer_type": "human",
        "confidence": 0.90,
    }


def provenance_payload() -> dict:
    payload = base_payload()
    payload["T"] = explicit_observation(payload["T"], "test://T")
    payload["C"] = explicit_observation(payload["C"], "test://C")
    payload["uncertainty_calibration"] = explicit_observation(
        payload["uncertainty_calibration"], "test://U"
    )
    payload["outcome_quality"] = explicit_observation(payload["outcome_quality"], "test://OQ")
    for family in [
        "flow_quality",
        "input_entropy",
        "output_entropy",
        "grounding",
        "behavioral_entropy",
        "operational_entropy",
    ]:
        payload[family] = {
            name: explicit_observation(value, f"test://{family}/{name}")
            for name, value in payload[family].items()
        }
    return payload


def score(payload: dict, **kwargs):
    return score_decision_efgm(EFGMDecisionInput.model_validate(payload), **kwargs)


def test_score_decision_efgm_incident_triage_example():
    result = score(base_payload())

    assert result.config_id == "efgm-v2.0-baseline"
    assert len(result.config_sha256) == 64
    assert len(result.input_sha256) == 64
    assert result.provenance_complete is False
    assert result.Ei == 0.50
    assert result.Eo == 0.055
    assert result.CRC > 0.80
    assert result.Q > 0.88
    assert result.DQ > 0.80
    assert result.classification == "Coherent and grounded"
    assert result.OD is not None


def test_legacy_numeric_inputs_are_promoted_to_inferred_observations():
    model_input = EFGMDecisionInput.model_validate(base_payload())

    assert model_input.T.value == 0.95
    assert model_input.T.status == "inferred"
    assert "Legacy numeric input" in model_input.T.rationale
    assert model_input.grounding.evidence_validity.value == 0.86


def test_missing_nested_observation_is_unknown_not_zero():
    payload = base_payload()
    del payload["output_entropy"]["context_decay"]
    model_input = EFGMDecisionInput.model_validate(payload)

    assert model_input.output_entropy.context_decay.status == "unknown"
    assert model_input.output_entropy.context_decay.value is None
    with pytest.raises(IncompleteAssessmentError, match="context_decay is unknown"):
        score_decision_efgm(model_input)


def test_omitted_entropy_family_cannot_silently_become_zero():
    payload = base_payload()
    del payload["behavioral_entropy"]

    with pytest.raises(IncompleteAssessmentError, match="behavioral_entropy.chasing_behavior is unknown"):
        score(payload)


def test_unknown_and_not_applicable_cannot_carry_numeric_values():
    with pytest.raises(ValidationError):
        MetricObservation(value=0.0, status="unknown")
    with pytest.raises(ValidationError):
        MetricObservation(value=0.0, status="not_applicable")


def test_not_applicable_metric_is_excluded_and_weights_are_renormalized():
    payload = base_payload()
    payload["output_entropy"]["context_decay"] = {
        "status": "not_applicable",
        "rationale": "Single-shot case has no prior context to decay.",
        "scorer_id": "reviewer-1",
        "scorer_type": "human",
        "confidence": 0.9,
    }

    result = score(payload)

    assert result.Eo == 0.0559


def test_whole_behavioral_and_operational_families_may_be_explicitly_not_applicable():
    payload = base_payload()
    for family in ["behavioral_entropy", "operational_entropy"]:
        payload[family] = {
            name: {
                "status": "not_applicable",
                "rationale": "Not applicable to this controlled test.",
                "scorer_id": "reviewer-1",
                "scorer_type": "human",
                "confidence": 0.9,
            }
            for name in payload[family]
        }

    result = score(payload)

    assert result.Be == 0.0
    assert result.Oe == 0.0


def test_research_provenance_mode_rejects_legacy_numeric_inputs():
    with pytest.raises(ProvenanceError, match="Research-grade provenance validation failed"):
        score(base_payload(), require_provenance=True)


def test_research_provenance_mode_accepts_evidence_backed_observations():
    result = score(provenance_payload(), require_provenance=True)

    assert result.provenance_complete is True
    assert result.provenance_issues == []


def test_explicit_observation_metadata_is_preserved():
    payload = base_payload()
    payload["grounding"]["evidence_validity"] = {
        "value": 0.86,
        "status": "observed",
        "rationale": "Validated against the source record.",
        "evidence_refs": ["evidence://source-record-1"],
        "scorer_id": "reviewer-1",
        "scorer_type": "human",
        "confidence": 0.95,
    }
    model_input = EFGMDecisionInput.model_validate(payload)
    observation = model_input.grounding.evidence_validity

    assert observation.status == "observed"
    assert observation.evidence_refs == ["evidence://source-record-1"]
    assert observation.confidence == 0.95


def test_critical_grounding_gate_prevents_reassuring_classification():
    payload = base_payload()
    payload["grounding"] = {name: 0.25 for name in payload["grounding"]}

    result = score(payload)

    assert result.G == 0.25
    assert result.classification == "Weakly grounded - verification required"
    assert "Establish valid evidence" in result.recommended_action


def test_higher_output_entropy_cannot_improve_decision_quality():
    low_entropy = base_payload()
    high_entropy = deepcopy(low_entropy)
    high_entropy["output_entropy"] = {name: 0.70 for name in high_entropy["output_entropy"]}

    low_result = score(low_entropy)
    high_result = score(high_entropy)

    assert high_result.Eo > low_result.Eo
    assert high_result.DQ < low_result.DQ


def test_hidden_information_reduces_outcome_confidence_without_changing_dq():
    low_hidden = base_payload()
    high_hidden = deepcopy(low_hidden)
    low_hidden["input_entropy"]["hidden_information_load"] = 0.10
    high_hidden["input_entropy"]["hidden_information_load"] = 0.80

    low_result = score(low_hidden)
    high_result = score(high_hidden)

    assert high_result.DQ == low_result.DQ
    assert high_result.outcome_confidence < low_result.outcome_confidence


def test_outcome_quality_changes_divergence_not_decision_quality():
    favorable = base_payload()
    unfavorable = deepcopy(favorable)
    favorable["outcome_quality"] = 0.95
    unfavorable["outcome_quality"] = 0.20

    favorable_result = score(favorable)
    unfavorable_result = score(unfavorable)

    assert favorable_result.DQ == unfavorable_result.DQ
    assert favorable_result.OD > unfavorable_result.OD


def test_crc_can_be_negative_and_unbounded_when_output_amplifies_entropy():
    payload = base_payload()
    payload["input_entropy"] = {name: 0.10 for name in payload["input_entropy"]}
    payload["output_entropy"] = {name: 0.70 for name in payload["output_entropy"]}

    result = score(payload)

    assert result.CRC < -1.0


def test_packaged_scoring_configuration_is_versioned_and_hashed():
    config = load_scoring_config()
    result = score(base_payload(), config=config)
    candidate = deepcopy(config)
    candidate["classification"]["critical_grounding_threshold"] = 0.39
    candidate_result = score(base_payload(), config=candidate)

    assert config["schema_version"] == 1
    assert config["config_id"] == "efgm-v2.0-baseline"
    assert result.config_sha256 != candidate_result.config_sha256


@pytest.mark.parametrize(
    "mutator",
    [
        lambda c: c.update({"epsilon": 0}),
        lambda c: c.update({"schema_version": 999}),
        lambda c: c["classification"].update({"coherent_dq_threshold": 1.2}),
        lambda c: c["classification"].update({"stable_dq_threshold": 0.75}),
        lambda c: c["weights"]["input_entropy"].update({"input_contradiction": -0.10, "input_ambiguity": 0.50}),
        lambda c: c["weights"]["grounding"].update({"typo_metric": 0.0}),
    ],
)
def test_invalid_candidate_configurations_are_rejected(mutator):
    candidate = deepcopy(load_scoring_config())
    mutator(candidate)

    with pytest.raises(ValueError):
        load_scoring_config(candidate)
