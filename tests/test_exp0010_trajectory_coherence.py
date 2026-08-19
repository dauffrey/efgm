import json
from pathlib import Path

from efgm.exp0010_trajectory_coherence import CHECKPOINTS, HORIZON, build_dataset, evaluate


def test_exp0010_dataset_is_deterministic():
    first = evaluate()
    second = evaluate()
    assert first == second


def test_exp0010_design_size_is_frozen():
    rows = build_dataset()
    scenario_ids = {row.scenario_id for row in rows}
    assert len(scenario_ids) == 240
    assert len(rows) == 240 * len(CHECKPOINTS)
    assert CHECKPOINTS == (6, 12, 18)
    assert HORIZON == 24


def test_exp0010_terminal_labels_are_independent_of_scores():
    rows = build_dataset()
    for row in rows:
        expected = "A" if row.final_progress >= 0.50 and row.final_reserve >= 0.08 else "M"
        assert row.outcome == expected


def test_exp0010_uses_only_checkpoint_information():
    rows = build_dataset()
    for row in rows:
        assert row.T == row.checkpoint / HORIZON
        assert 0.0 <= row.E <= 1.0
        assert 0.0 <= row.Et <= 1.0
        assert 0.0 <= row.F <= 1.0
        assert 0.0 <= row.e <= 1.0


def test_exp0010_result_contract():
    result = evaluate()
    assert result["classification"] in {"SURVIVED", "FALSIFIED", "INVALID"}
    assert result["early_warning_classification"] in {"SUPPORTED", "NOT SUPPORTED"}
    assert set(result["checkpoints"]) == {"6", "12", "18"}
    for checkpoint in result["checkpoints"].values():
        assert set(checkpoint) == {
            "trajectory_dynamics",
            "F_only",
            "E_only",
            "entropy_only",
            "current_state_joint",
        }
        assert all(0.0 <= value <= 1.0 for value in checkpoint.values())
    assert abs(sum(result["frozen_weights"].values()) - 1.0) < 1e-12


def test_exp0010_frozen_result_matches_deterministic_evaluator():
    result_path = Path(__file__).parents[1] / "experiments" / "results" / "EFGM-EXP-0010.json"
    frozen = json.loads(result_path.read_text(encoding="utf-8"))
    current = evaluate()

    assert frozen["primary_classification"] == current["classification"]
    assert frozen["early_warning_classification"] == current["early_warning_classification"]
    assert frozen["dataset"]["sha256"] == current["dataset_sha256"]
    assert frozen["dataset"]["trajectory_count"] == current["trajectory_count"]
    assert frozen["dataset"]["observation_count"] == current["observation_count"]
    assert frozen["dataset"]["aligned_count"] == current["aligned_count"]
    assert frozen["dataset"]["misaligned_count"] == current["misaligned_count"]
    assert frozen["frozen_criteria"] == current["criteria"]

    for checkpoint, frozen_values in frozen["checkpoints"].items():
        current_values = current["checkpoints"][checkpoint]
        for metric, frozen_value in frozen_values.items():
            assert round(current_values[metric], 4) == frozen_value
