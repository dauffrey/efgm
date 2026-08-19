from efgm.exp0011_coupled_state import (
    CHECKPOINTS,
    HORIZON,
    SEED_END,
    SEED_START,
    build_dataset,
    dataset_manifest,
)


def test_exp0011_fresh_holdout_is_deterministic():
    assert dataset_manifest() == dataset_manifest()


def test_exp0011_fresh_holdout_design_is_frozen():
    rows = build_dataset()
    scenario_ids = {row.scenario_id for row in rows}
    seeds = {row.scenario_seed for row in rows}

    assert len(scenario_ids) == 240
    assert len(rows) == 240 * 3
    assert seeds == set(range(SEED_START, SEED_END + 1))
    assert CHECKPOINTS == (6, 12, 18)
    assert HORIZON == 24


def test_exp0011_labels_use_only_terminal_rule():
    rows = build_dataset()
    for row in rows:
        expected = "A" if row.final_progress >= 0.50 and row.final_reserve >= 0.08 else "M"
        assert row.outcome == expected


def test_exp0011_checkpoint_measurements_are_normalized():
    for row in build_dataset():
        assert row.T == row.checkpoint / HORIZON
        assert 0.0 <= row.E <= 1.0
        assert 0.0 <= row.Et <= 1.0
        assert 0.0 <= row.F <= 1.0
        assert 0.0 <= row.e <= 1.0


def test_exp0011_manifest_does_not_expose_scientific_scoring():
    manifest = dataset_manifest()
    assert manifest["scientific_scoring_exposed"] is False
    assert set(manifest) == {
        "experiment_id",
        "dataset_version",
        "dataset_seed",
        "dataset_sha256",
        "canonical_float_decimals",
        "scenario_count",
        "observation_count",
        "steps_per_scenario",
        "checkpoints",
        "seed_start",
        "seed_end",
        "seed_count",
        "aligned_count",
        "misaligned_count",
        "minority_class_fraction",
        "scientific_scoring_exposed",
    }
    assert manifest["scenario_count"] == 240
    assert manifest["observation_count"] == 720
    assert manifest["minority_class_fraction"] >= 0.15
