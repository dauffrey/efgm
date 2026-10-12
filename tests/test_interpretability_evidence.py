"""Fictional evidence packets only. These tests do not inspect a model."""
from copy import deepcopy

from efgm.interpretability_evidence import assess_interpretability_claim


def packet():
    return {
        "schema_version": "interpretability-evidence/0.1",
        "claim_id": "fictional-causal-claim",
        "mechanism": "Fabricated circuit ablation predicts a fabricated output change.",
        "model_sha256": "a" * 64,
        "protocol_sha256": "b" * 64,
        "development_dataset_sha256": "c" * 64,
        "evaluation_dataset_sha256": "d" * 64,
        "evidence_manifest_sha256": "e" * 64,
        "proposer_id": "fictional-proposer",
        "evaluator_id": "fictional-independent-evaluator",
        "protocol_frozen_before_evaluation": True,
        "known_counterexample_count": 0,
        "causal_intervention": "observed",
        "negative_control": "observed",
        "independent_replication": "observed",
        "heldout_evaluation": "observed",
    }


def test_fabricated_complete_packet_is_not_certification():
    result = assess_interpretability_claim(packet())
    assert result.status == "READY_FOR_EXTERNAL_AUDIT"
    assert result.reasons == ()
    assert result.scientific_claim_validated is False
    assert result.grants_authority is False


def test_missingness_cannot_become_a_favorable_zero_or_success():
    for field in ("causal_intervention", "negative_control", "independent_replication", "heldout_evaluation"):
        for status in ("unknown", "inferred", "not_applicable"):
            example = packet()
            example[field] = status
            result = assess_interpretability_claim(example)
            assert result.status == "INSUFFICIENT_EVIDENCE"
            assert field + "_not_observed" in result.reasons
            assert not result.grants_authority


def test_separation_freeze_and_counterexample_failures():
    mutations = [
        ("protocol_frozen_before_evaluation", False, "protocol_not_frozen"),
        ("evaluator_id", "fictional-proposer", "evaluator_not_separate"),
        ("evaluation_dataset_sha256", "c" * 64, "evaluation_identity_equals_development"),
        ("known_counterexample_count", 1, "counterexamples_need_adjudication"),
    ]
    for key, value, reason in mutations:
        item = packet()
        item[key] = value
        result = assess_interpretability_claim(item)
        assert result.status == "INSUFFICIENT_EVIDENCE"
        assert reason in result.reasons
        assert not result.scientific_claim_validated


def test_invalid_input_rejected_without_trusting_numeric_or_hash_coercions():
    examples = [None, [], {}, deepcopy(packet())]
    examples[-1]["extra"] = "unreviewed"
    for item in examples:
        assert assess_interpretability_claim(item).status == "INVALID"
    mutations = [
        ("known_counterexample_count", True),
        ("known_counterexample_count", -1),
        ("protocol_frozen_before_evaluation", 1),
        ("model_sha256", "A" * 64),
        ("model_sha256", "bad"),
        ("causal_intervention", True),
        ("causal_intervention", "successful"),
        ("claim_id", " "),
    ]
    for field, value in mutations:
        example = packet()
        example[field] = value
        assert assess_interpretability_claim(example).status == "INVALID"


def test_cannot_self_validate_by_modifying_a_result():
    result = assess_interpretability_claim(packet())
    assert result.scientific_claim_validated is False
    assert result.grants_authority is False
