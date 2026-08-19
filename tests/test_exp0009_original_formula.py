import json
from pathlib import Path

from efgm.exp0009_original_formula import build_dataset, evaluate


def test_exp0009_dataset_is_deterministic():
    first = evaluate()
    second = evaluate()
    assert first["dataset_sha256"] == second["dataset_sha256"]
    assert first == second


def test_exp0009_has_expected_frozen_design_size():
    rows = build_dataset()
    assert len(rows) == 200
    assert len({row.scenario_id for row in rows}) == 200


def test_exp0009_labels_do_not_depend_on_joint_proxy_threshold():
    rows = build_dataset()
    for row in rows:
        expected = "A" if row.final_progress >= 0.55 and row.final_reserve >= 0.10 else "M"
        assert row.outcome == expected


def test_exp0009_result_schema_without_encoding_desired_outcome():
    result = evaluate()
    assert result["classification"] in {"SURVIVED", "FALSIFIED", "INVALID"}
    assert set(result["aucs"]) == {
        "joint_proxy", "T_only", "E_only", "Et_only", "F_only", "entropy_only"
    }
    assert all(0.0 <= value <= 1.0 for value in result["aucs"].values())
    assert result["trajectory_count"] == result["aligned_count"] + result["misaligned_count"]


def test_exp0009_frozen_result_matches_deterministic_evaluator():
    result_path = Path(__file__).parents[1] / "experiments" / "results" / "EFGM-EXP-0009.json"
    frozen = json.loads(result_path.read_text(encoding="utf-8"))
    current = evaluate()

    assert frozen["classification"] == current["classification"]
    assert frozen["dataset"]["sha256"] == current["dataset_sha256"]
    assert frozen["dataset"]["trajectory_count"] == current["trajectory_count"]
    assert frozen["dataset"]["aligned_count"] == current["aligned_count"]
    assert frozen["dataset"]["misaligned_count"] == current["misaligned_count"]
    assert frozen["auc"] == current["aucs"]
    assert frozen["frozen_criteria"] == current["criteria"]
