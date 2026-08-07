from efgm.benchmark_v0_1 import (
    EXPECTED_DATASET_SHA256,
    FAMILIES,
    dataset_sha256,
    generate_cases,
    validate_expected_dataset,
)
from efgm.experiment_runner import (
    FROZEN_BASELINE_SHA,
    MODEL_NAMES,
    case_to_v2_input,
    run_experiment,
    score_case,
)
from efgm.scoring_v2 import score_decision_efgm


def test_benchmark_v0_1_is_frozen_and_partitioned():
    cases = generate_cases()

    assert len(cases) == 144
    assert len({case["pair_id"] for case in cases}) == 72
    assert len({case["family"] for case in cases}) == 12
    assert set(FAMILIES) == {case["family"] for case in cases}
    assert sum(case["split"] == "development" for case in cases) == 96
    assert sum(case["split"] == "validation" for case in cases) == 48
    assert dataset_sha256(cases) == EXPECTED_DATASET_SHA256
    assert validate_expected_dataset() == EXPECTED_DATASET_SHA256


def test_benchmark_case_can_be_scored_in_strict_provenance_mode():
    case = generate_cases()[0]
    model_input = case_to_v2_input(case)
    result = score_decision_efgm(model_input, require_provenance=True)

    assert result.provenance_complete is True
    assert not result.provenance_issues
    assert result.DQ > 0


def test_comparison_models_return_normalized_scores():
    case = generate_cases()[0]
    scores = [score_case(case, model) for model in MODEL_NAMES]

    assert all(0 <= score <= 1 for score in scores)


def test_controlled_benchmark_has_expected_baseline_rankings():
    result = run_experiment(sensitivity_trials=2, perturbation=0.05)
    overall = result["results"]["all"]

    assert result["frozen_baseline_sha"] == FROZEN_BASELINE_SHA
    assert overall["v2"]["wins"] == 72
    assert overall["v2"]["ties"] == 0
    assert overall["linear"]["wins"] == 72
    assert overall["independent_checklist"]["wins"] == 66
    assert overall["independent_checklist"]["ties"] == 6
    assert overall["g_plus_u"]["wins"] == 48
    assert overall["g_plus_u"]["ties"] == 24
    assert overall["v1"]["wins"] == 42
    assert overall["v1"]["ties"] == 30


def test_behavioral_feedback_exposes_smaller_baseline_blind_spots():
    cases = [case for case in generate_cases() if case["pair_id"] == "behavioral_feedback-01"]
    preferred = next(case for case in cases if case["preferred"])
    mutated = next(case for case in cases if not case["preferred"])

    assert score_case(preferred, "v2") > score_case(mutated, "v2")
    assert score_case(preferred, "linear") > score_case(mutated, "linear")
    assert score_case(preferred, "v1") == score_case(mutated, "v1")
    assert score_case(preferred, "g_plus_u") == score_case(mutated, "g_plus_u")
    assert score_case(preferred, "independent_checklist") == score_case(mutated, "independent_checklist")


def test_outcome_variance_does_not_reverse_decision_ranking():
    cases = [case for case in generate_cases() if case["pair_id"] == "outcome_variance-01"]
    preferred = next(case for case in cases if case["preferred"])
    mutated = next(case for case in cases if not case["preferred"])

    assert preferred["values"]["outcome_quality"] < mutated["values"]["outcome_quality"]
    assert score_case(preferred, "v2") > score_case(mutated, "v2")
