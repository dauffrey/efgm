from efgm.schemas_v2 import (
    EFGMDecisionInput,
    FlowQualityMetricsV2,
    GroundingMetrics,
    InputEntropyMetrics,
    OutputEntropyMetrics,
)
from efgm.scoring_v2 import score_decision_efgm


def test_score_decision_efgm_incident_triage_example():
    model_input = EFGMDecisionInput(
        task_id="incident-triage-example",
        T=0.95,
        C=0.85,
        flow_quality=FlowQualityMetricsV2(
            task_completion_consistency=0.92,
            reasoning_continuity=0.90,
            semantic_coherence=0.91,
            verification_success_rate=0.86,
        ),
        input_entropy=InputEntropyMetrics(
            input_contradiction=0.55,
            input_ambiguity=0.70,
            input_goal_conflict=0.45,
            missing_context=0.60,
            hidden_information_load=0.80,
        ),
        output_entropy=OutputEntropyMetrics(
            output_contradiction=0.05,
            uncertainty_mismatch=0.10,
            goal_drift=0.05,
            reasoning_instability=0.00,
            context_decay=0.05,
        ),
        grounding=GroundingMetrics(
            rule_support=0.88,
            evidence_validity=0.86,
            traceability=0.90,
            factual_consistency=0.88,
            domain_calibration=0.88,
        ),
        uncertainty_calibration=0.90,
        outcome_quality=0.90,
    )

    result = score_decision_efgm(model_input)

    assert result.Ei == 0.62
    assert result.Eo == 0.055
    assert result.CRC > 0.90
    assert result.Q > 0.88
    assert result.DQ > 0.80
    assert result.classification == "Coherent and grounded"
    assert result.OD is not None
