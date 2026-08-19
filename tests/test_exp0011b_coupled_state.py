from efgm.exp0011b_coupled_state import (
    CHECKPOINTS,
    ENTROPY_BANDS,
    HORIZON,
    SEED_END,
    SEED_START,
    build_dataset,
    dataset_manifest,
)


def test_exp0011b_holdout_is_deterministic():
    assert dataset_manifest() == dataset_manifest()


def test_exp0011b_design_is_frozen():
    rows = build_dataset()
    scenario_ids = {row.scenario_id for row in rows}
    seeds = {row.scenario_seed for row in rows}
    assert len(scenario_ids) == 288
    assert len(rows) == 288 * 3
    assert seeds == set(range(SEED_START, SEED_END + 1))
    assert CHECKPOINTS == (6, 12, 18)
    assert HORIZON == 24
    assert ENTROPY_BANDS == (0.10, 0.25, 0.40, 0.55, 0.70, 0.82)


def test_exp0011b_labels_use_only_terminal_rule():
    for row in build_dataset():
        expected = "A" if row.final_progress >= 0.50 and row.final_reserve >= 0.08 else "M"
        assert row.outcome == expected


def test_exp0011b_checkpoint_measurements_are_normalized():
    for row in build_dataset():
        assert row.T == row.checkpoint / HORIZON
        assert 0.0 <= row.E <= 1.0
        assert 0.0 <= row.Et <= 1.0
        assert 0.0 <= row.F <= 1.0
        assert 0.0 <= row.e <= 1.0


def test_exp0011b_manifest_is_preexecution_only_and_valid():
    manifest = dataset_manifest()
    assert manifest["scientific_scoring_exposed"] is False
    assert manifest["scenario_count"] == 288
    assert manifest["observation_count"] == 864
    assert manifest["seed_start"] == 120001
    assert manifest["seed_end"] == 120288
    assert manifest["seed_count"] == 288
    assert manifest["checkpoints"] == [6, 12, 18]
    assert manifest["minority_class_fraction"] >= 0.15
