from __future__ import annotations

import json
from pathlib import Path

import pytest

from efgm.exp0007_v2_sparse_failure import (
    CANDIDATE_POSITIVE_PATHS,
    DEVELOPMENT_CASE_SPECS,
    INVARIANT_POSITIVE_PATHS,
    VALIDATION_CASE_SPECS,
    dataset_sha256,
    run_exp0007,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_exp0007_dataset_partition_and_identity_are_frozen():
    assert len(DEVELOPMENT_CASE_SPECS) == 16
    assert len(VALIDATION_CASE_SPECS) == 20
    assert dataset_sha256() == "799329f4b257a44461ca1004a616dd47373e19339612332033207b7d1783ffb2"
    assert not {case["case_id"] for case in DEVELOPMENT_CASE_SPECS} & {case["case_id"] for case in VALIDATION_CASE_SPECS}


def test_exp0007_validation_contains_preregistered_candidate_coverage_challenges():
    challenge_paths = {
        "flow_quality.reasoning_continuity",
        "flow_quality.semantic_coherence",
        "grounding.traceability",
        "grounding.factual_consistency",
    }
    validation_catastrophic_paths = {case["target_path"] for case in VALIDATION_CASE_SPECS if case["kind"] == "catastrophic"}
    assert challenge_paths <= validation_catastrophic_paths
    assert not challenge_paths & CANDIDATE_POSITIVE_PATHS
    assert challenge_paths <= INVARIANT_POSITIVE_PATHS


def test_exp0007_materialized_specs_match_runner_source():
    development = json.loads((REPO_ROOT / "benchmarks" / "development" / "EFGM-EXP-0007" / "cases.json").read_text(encoding="utf-8"))
    validation = json.loads((REPO_ROOT / "benchmarks" / "validation" / "EFGM-EXP-0007" / "cases.json").read_text(encoding="utf-8"))
    assert development["cases"] == DEVELOPMENT_CASE_SPECS
    assert validation["cases"] == VALIDATION_CASE_SPECS


def test_exp0007_runner_preserves_frozen_v2_and_holdout_boundary_without_asserting_scientific_outcome():
    result = run_exp0007(perturbation_trials=2, perturbation=0.05, seed=20260810, code_sha="test-code-sha")
    assert result["parent_main_sha"] == "fd70317e4bad193c00763a398f41db6e75700b55"
    assert result["code_sha"] == "test-code-sha"
    assert result["baseline_config_id"] == "efgm-v2.0-baseline"
    assert result["frozen_dq_preserved"] is True
    assert result["holdout_cases"] == 0
    assert result["holdout_accessed"] is False
    assert result["development_cases"] == 16
    assert result["validation_cases"] == 20
    for split in ("development", "validation"):
        assert "aggregate_only" in result[split]
        assert "candidate_prerequisite_plus_extreme_veto" in result[split]
        assert "observation_floor_plus_extreme_max" in result[split]
        assert "soft_percentile_diagnostic" in result[split]
        assert "independent_invariant_checklist" in result[split]
        assert len(result[split]["dq_by_case"]) == result[f"{split}_cases"]
        assert len(result[split]["input_sha256_by_case"]) == result[f"{split}_cases"]
    assert isinstance(result["promotion_gate_passed"], bool)


@pytest.mark.parametrize(("trials", "perturbation"), [(0, 0.10), (-1, 0.10), (10, -0.01), (10, 1.01), (10, float("nan"))])
def test_exp0007_rejects_invalid_perturbation_inputs(trials, perturbation):
    with pytest.raises(ValueError):
        run_exp0007(perturbation_trials=trials, perturbation=perturbation, code_sha="test-code-sha")
