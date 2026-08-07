from copy import deepcopy

from efgm.schemas_v2 import EFGMDecisionInput
from efgm.scoring_v2 import load_scoring_config, score_decision_efgm


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
        "outcome_quality": 0.90,
    }


def score(payload: dict):
    return score_decision_efgm(EFGMDecisionInput.model_validate(payload))


def test_score_decision_efgm_incident_triage_example():
    result = score(base_payload())

    assert result.config_id == "efgm-v2.0-baseline"
    assert result.Ei == 0.50
    assert result.Eo == 0.055
    assert result.CRC > 0.80
    assert result.Q > 0.88
    assert result.DQ > 0.80
    assert result.classification == "Coherent and grounded"
    assert result.OD is not None


def test_legacy_numeric_inputs_are_promoted_to_auditable_observations():
    model_input = EFGMDecisionInput.model_validate(base_payload())

    assert model_input.T.value == 0.95
    assert model_input.T.status == "inferred"
    assert "Legacy numeric input" in model_input.T.rationale
    assert model_input.grounding.evidence_validity.value == 0.86


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


def test_packaged_scoring_configuration_is_versioned():
    config = load_scoring_config()

    assert config["config_id"] == "efgm-v2.0-baseline"
    assert config["classification"]["critical_grounding_threshold"] == 0.40
