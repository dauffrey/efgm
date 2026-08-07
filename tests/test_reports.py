from efgm.reports import render_decision_markdown_report, render_markdown_report
from efgm.schemas import EFGMResult
from efgm.schemas_v2 import EFGMDecisionInput
from efgm.scoring_v2 import score_decision_efgm


def test_v1_report_uses_geometric_mean_formula():
    result = EFGMResult(
        task_id="report-test",
        T=0.8,
        E=0.9,
        Fq=0.7225,
        e=0.205,
        F=0.6674,
        classification="Stable with watch items",
        recommended_action="Proceed with monitoring. Track watch items.",
        entropy_drivers=[],
    )
    report = render_markdown_report(result)
    assert "# EFGM v1 Coherent Flow Report" in report
    assert "Q = (T × E × Fq)^(1/3)" in report
    assert "F = (T × E × Fq) /" not in report


def test_v2_report_contains_decision_metrics_and_reproducibility_ids():
    payload = {
        "task_id": "report-v2",
        "T": 0.95,
        "C": 0.85,
        "flow_quality": {
            "task_completion_consistency": 0.92,
            "reasoning_continuity": 0.90,
            "semantic_coherence": 0.91,
            "verification_success_rate": 0.86,
        },
        "input_entropy": {
            "input_contradiction": 0.0,
            "input_ambiguity": 0.0,
            "input_goal_conflict": 0.0,
            "missing_context": 0.0,
            "hidden_information_load": 0.80,
        },
        "output_entropy": {
            "output_contradiction": 0.05,
            "uncertainty_mismatch": 0.0,
            "goal_drift": 0.0,
            "reasoning_instability": 0.0,
            "context_decay": 0.0,
        },
        "grounding": {
            "rule_support": 0.88,
            "evidence_validity": 0.86,
            "traceability": 0.90,
            "factual_consistency": 0.88,
            "domain_calibration": 0.88,
        },
        "uncertainty_calibration": 0.90,
        "behavioral_entropy": {
            "chasing_behavior": 0.0,
            "outcome_bias": 0.0,
            "sunk_cost_pressure": 0.0,
            "false_pattern_detection": 0.0,
            "overconfidence_feedback": 0.0,
        },
        "operational_entropy": {
            "timeout_rate": 0.0,
            "retry_instability": 0.0,
            "tool_failure_rate": 0.0,
            "latency_pressure": 0.0,
            "workflow_interruption": 0.0,
        },
        "outcome_quality": 0.90,
    }
    model_input = EFGMDecisionInput.model_validate(payload)
    report = render_decision_markdown_report(score_decision_efgm(model_input))
    assert "# EFGM v2 Decision Integrity Report" in report
    assert "| DQ |" in report
    assert "OD = OQ - DQ" in report
    assert "Configuration SHA-256" in report
    assert "Input SHA-256" in report
