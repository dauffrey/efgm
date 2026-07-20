from efgm.reports import render_decision_markdown_report, render_markdown_report
from efgm.schemas import EFGMResult
from efgm.schemas_v2 import EFGMDecisionInput, FlowQualityMetricsV2, GroundingMetrics, InputEntropyMetrics, OutputEntropyMetrics
from efgm.scoring_v2 import score_decision_efgm


def test_v1_report_uses_geometric_mean_formula():
    result = EFGMResult(task_id="report-test", T=0.8, E=0.9, Fq=0.7225, e=0.205, F=0.6674, classification="Stable with watch items", recommended_action="Proceed with monitoring. Track watch items.", entropy_drivers=[])
    report = render_markdown_report(result)
    assert "# EFGM v1 Coherent Flow Report" in report
    assert "Q = (T × E × Fq)^(1/3)" in report
    assert "F = (T × E × Fq) /" not in report


def test_v2_report_contains_decision_metrics():
    model_input = EFGMDecisionInput(task_id="report-v2", T=0.95, C=0.85, flow_quality=FlowQualityMetricsV2(task_completion_consistency=0.92, reasoning_continuity=0.90, semantic_coherence=0.91, verification_success_rate=0.86), input_entropy=InputEntropyMetrics(hidden_information_load=0.80), output_entropy=OutputEntropyMetrics(output_contradiction=0.05), grounding=GroundingMetrics(rule_support=0.88, evidence_validity=0.86, traceability=0.90, factual_consistency=0.88, domain_calibration=0.88), uncertainty_calibration=0.90, outcome_quality=0.90)
    report = render_decision_markdown_report(score_decision_efgm(model_input))
    assert "# EFGM v2 Decision Integrity Report" in report
    assert "| DQ |" in report
    assert "OD = OQ - DQ" in report
