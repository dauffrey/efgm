from __future__ import annotations

import pytest

from efgm.exp0005_temporal_recovery import (
    DEVELOPMENT_CASE_SPECS,
    EXPECTED_DATASET_SHA256,
    EXPECTED_MATERIALIZED_STATE_SHA256,
    MATERIALIZATION_VERSION,
    RECOVERY_INVARIANT_PATHS,
    RUNNER_VERSION,
    VALIDATION_CASE_SPECS,
    dataset_sha256,
    materialized_state_sha256,
    run_exp0005,
)


def test_exp0005_dataset_identity_and_partition_are_frozen():
    assert len(DEVELOPMENT_CASE_SPECS) == 12
    assert len(VALIDATION_CASE_SPECS) == 14
    assert dataset_sha256() == EXPECTED_DATASET_SHA256 == "9755ad1ebc44c8ae44ac796597152eb2fa1ec48c9f5161a1532a3a4ffccc5b27"
    assert not {case["case_id"] for case in DEVELOPMENT_CASE_SPECS} & {case["case_id"] for case in VALIDATION_CASE_SPECS}


def test_exp0005_materialized_temporal_state_identity_is_separately_frozen():
    assert RUNNER_VERSION == "0.2.0"
    assert MATERIALIZATION_VERSION == "temporal-agent-state-v0.2"
    assert materialized_state_sha256() == EXPECTED_MATERIALIZED_STATE_SHA256
    assert len(EXPECTED_MATERIALIZED_STATE_SHA256) == 64


def test_exp0005_preregisters_uncovered_semantic_and_cross_sequence_challenges():
    validation_overrides = {path for case in VALIDATION_CASE_SPECS for path in case.get("post_metric_override", {})}
    assert "alignment.prohibited_goal_avoidance" in validation_overrides
    assert "boundary_integrity.capability_scope_adherence" in validation_overrides
    assert {"alignment.prohibited_goal_avoidance", "boundary_integrity.capability_scope_adherence"} <= RECOVERY_INVARIANT_PATHS
    identity_cases = [case for case in VALIDATION_CASE_SPECS if case["kind"] == "identity_rejection"]
    assert len(identity_cases) == 2


def test_exp0005_runner_checks_mechanics_without_encoding_scientific_outcome():
    result = run_exp0005(perturbation_trials=2, perturbation=0.02, seed=20260810, code_sha="test-code-sha")
    assert result["parent_main_sha"] == "fd70317e4bad193c00763a398f41db6e75700b55"
    assert result["code_sha"] == "test-code-sha"
    assert result["runner_version"] == RUNNER_VERSION
    assert result["candidate_config_id"] == "efgm-v0.3-agent-governance-candidate-r2"
    assert result["dataset_sha256"] == EXPECTED_DATASET_SHA256
    assert result["materialization_version"] == MATERIALIZATION_VERSION
    assert result["materialized_state_sha256"] == EXPECTED_MATERIALIZED_STATE_SHA256
    assert result["holdout_cases"] == 0
    assert result["holdout_accessed"] is False
    assert result["development_cases"] == 12
    assert result["validation_cases"] == 14
    for split in ("development", "validation"):
        assert "recovery_progress" in result[split]
        assert "verified_recovery" in result[split]
        assert "static_recovery_proxy" in result[split]
        assert "independent_recovery_checklist" in result[split]
        assert isinstance(result[split]["incremental_verified_accuracy_vs_static"], float)
        assert isinstance(result[split]["incremental_verified_accuracy_vs_checklist"], float)
    assert result["validation"]["sequence_identity_rejection_rate"] == 1.0
    assert isinstance(result["promotion_gate_passed"], bool)


@pytest.mark.parametrize(("trials", "perturbation"), [(0, 0.05), (-1, 0.05), (10, -0.01), (10, 1.01), (10, float("nan"))])
def test_exp0005_rejects_invalid_perturbation_inputs(trials, perturbation):
    with pytest.raises(ValueError):
        run_exp0005(perturbation_trials=trials, perturbation=perturbation, code_sha="test-code-sha")
