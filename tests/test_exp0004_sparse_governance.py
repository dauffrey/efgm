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
    assert len(VALIDATION_CASE_SPECS) == 12
    assert dataset_sha256() == "999b60706e7a20d5a2b4eda123511a7a39922038854aacab2c2c6edc1698a758"
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

    for split in ("development", "validation"):
        summary = result[split]
        assert summary["aggregate_only"]["false_reassurance_rate"] == 1.0
        assert (
            summary["configured_candidate_prerequisites"]["detection_rate"]
            == 1.0
        )
        assert (
            summary["configured_candidate_prerequisites"]["false_alarm_rate"]
            == 0.0
        )
        assert summary["governance_observation_floor"]["detection_rate"] == 1.0
        assert summary["governance_observation_floor"]["false_alarm_rate"] == 0.5
        assert summary["governance_low_percentile"]["detection_rate"] == 0.0
        assert summary["governance_low_percentile"]["false_alarm_rate"] == 0.0
        assert summary["independent_invariant_checklist"]["detection_rate"] == 1.0
        assert summary["independent_invariant_checklist"]["false_alarm_rate"] == 0.0
        assert summary["incremental_balanced_accuracy_vs_checklist"] == 0.0

    assert result["promotion_gate_passed"] is False


def test_exp0004_threshold_sensitivity_and_ablation_are_visible():
    result = run_exp0004(
        perturbation_trials=20,
        perturbation=0.10,
        seed=20260810,
        code_sha="test-code-sha",
    )

    sensitivity = result["threshold_sensitivity"]
    assert sensitivity["0.40"]["detection_rate"] == 1.0
    assert sensitivity["0.40"]["false_alarm_rate"] == 0.0
    assert sensitivity["0.30"]["detection_rate"] == 0.5
    assert sensitivity["0.50"]["false_alarm_rate"] == 0.5

    for ablation in result["candidate_prerequisite_path_ablation"].values():
        assert ablation["detection_rate"] == pytest.approx(10 / 12, abs=0.0001)


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
