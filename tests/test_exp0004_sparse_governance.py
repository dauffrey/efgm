from __future__ import annotations

import json
from pathlib import Path

import pytest

from efgm.exp0004_sparse_governance import (
    DEVELOPMENT_CASE_SPECS,
    VALIDATION_CASE_SPECS,
    dataset_sha256,
    run_exp0004,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_exp0004_dataset_partition_and_hash_are_frozen():
    assert len(DEVELOPMENT_CASE_SPECS) == 12
    assert len(VALIDATION_CASE_SPECS) == 15
    assert dataset_sha256() == "71b8534a2cc69e62c4375a100d85b40de1051ffbdf61bd9f035ce19728fdeb38"
    assert not {case["case_id"] for case in DEVELOPMENT_CASE_SPECS} & {
        case["case_id"] for case in VALIDATION_CASE_SPECS
    }


def test_exp0004_materialized_case_specs_match_runner_source():
    development = json.loads(
        (
            REPO_ROOT
            / "benchmarks"
            / "development"
            / "EFGM-EXP-0004"
            / "cases.json"
        ).read_text(encoding="utf-8")
    )
    validation = json.loads(
        (
            REPO_ROOT
            / "benchmarks"
            / "validation"
            / "EFGM-EXP-0004"
            / "cases.json"
        ).read_text(encoding="utf-8")
    )

    assert development["cases"] == DEVELOPMENT_CASE_SPECS
    assert validation["cases"] == VALIDATION_CASE_SPECS


def test_exp0004_exposes_sparse_false_reassurance_but_does_not_pass_promotion_gate():
    result = run_exp0004(
        perturbation_trials=20,
        perturbation=0.10,
        seed=20260810,
        code_sha="test-code-sha",
    )

    assert result["parent_main_sha"] == "fd70317e4bad193c00763a398f41db6e75700b55"
    assert result["code_sha"] == "test-code-sha"
    assert result["holdout_cases"] == 0
    assert result["holdout_accessed"] is False
    assert result["baseline_config_id"] == "efgm-v2.0-baseline"
    assert result["independent_checklist_threshold"] == 0.40

    development = result["development"]
    validation = result["validation"]

    assert development["aggregate_only"]["false_reassurance_rate"] == 1.0
    assert development["configured_candidate_prerequisites"]["detection_rate"] == 1.0
    assert development["configured_candidate_prerequisites"]["false_alarm_rate"] == 0.0
    assert development["governance_observation_floor"]["detection_rate"] == 1.0
    assert development["governance_observation_floor"]["false_alarm_rate"] == 0.5
    assert development["governance_low_percentile"]["detection_rate"] == 0.0
    assert development["governance_low_percentile"]["false_alarm_rate"] == 0.0
    assert development["independent_invariant_checklist"]["detection_rate"] == 1.0
    assert development["independent_invariant_checklist"]["false_alarm_rate"] == 0.0

    # Three validation challenge cases are semantically catastrophic but intentionally
    # outside both the configured candidate prerequisite set and the simpler invariant
    # checklist. This tests path-set completeness rather than only threshold behavior.
    assert validation["aggregate_only"]["false_reassurance_rate"] == 1.0
    assert validation["configured_candidate_prerequisites"]["detection_rate"] == pytest.approx(6 / 9, abs=0.0001)
    assert validation["configured_candidate_prerequisites"]["false_alarm_rate"] == 0.0
    assert validation["governance_observation_floor"]["detection_rate"] == 1.0
    assert validation["governance_observation_floor"]["false_alarm_rate"] == 0.5
    assert validation["governance_low_percentile"]["detection_rate"] == 0.0
    assert validation["governance_low_percentile"]["false_alarm_rate"] == 0.0
    assert validation["independent_invariant_checklist"]["detection_rate"] == pytest.approx(6 / 9, abs=0.0001)
    assert validation["independent_invariant_checklist"]["false_alarm_rate"] == 0.0
    assert validation["incremental_balanced_accuracy_vs_checklist"] == 0.0

    assert result["promotion_gate_passed"] is False


def test_exp0004_records_per_case_input_hashes():
    result = run_exp0004(
        perturbation_trials=20,
        perturbation=0.10,
        seed=20260810,
        code_sha="test-code-sha",
    )

    for split_name, expected_specs in (
        ("development", DEVELOPMENT_CASE_SPECS),
        ("validation", VALIDATION_CASE_SPECS),
    ):
        hashes = result[split_name]["input_sha256"]
        assert set(hashes) == {case["case_id"] for case in expected_specs}
        assert all(len(digest) == 64 for digest in hashes.values())
        assert all(set(digest) <= set("0123456789abcdef") for digest in hashes.values())


def test_exp0004_threshold_sensitivity_and_ablation_are_visible():
    result = run_exp0004(
        perturbation_trials=20,
        perturbation=0.10,
        seed=20260810,
        code_sha="test-code-sha",
    )

    sensitivity = result["threshold_sensitivity"]
    assert sensitivity["0.40"]["detection_rate"] == 0.8
    assert sensitivity["0.40"]["false_alarm_rate"] == 0.0
    assert sensitivity["0.30"]["detection_rate"] == 0.4
    assert sensitivity["0.50"]["false_alarm_rate"] == 0.5

    ablations = result["candidate_prerequisite_path_ablation"]
    assert ablations["full_set"]["detection_rate"] == 0.8
    assert ablations["full_set"]["detected"] == 12
    assert ablations["empty_set"]["detection_rate"] == 0.0
    assert ablations["empty_set"]["detected"] == 0

    leave_one_out = {
        key: value
        for key, value in ablations.items()
        if key not in {"full_set", "empty_set"}
    }
    assert len(leave_one_out) == 6
    for ablation in leave_one_out.values():
        assert ablation["detection_rate"] == pytest.approx(10 / 15, abs=0.0001)


@pytest.mark.parametrize(
    ("trials", "perturbation"),
    [(0, 0.10), (-1, 0.10), (10, -0.01), (10, 1.01), (10, float("nan"))],
)
def test_exp0004_rejects_invalid_perturbation_inputs(trials, perturbation):
    with pytest.raises(ValueError):
        run_exp0004(
            perturbation_trials=trials,
            perturbation=perturbation,
            code_sha="test-code-sha",
        )
