from efgm.schemas import EFGMInput, EntropyMetrics, FlowQualityMetrics
from efgm.scoring import geometric_mean, score_efgm


def test_geometric_mean():
    assert round(geometric_mean([0.8, 0.9, 0.7225]), 4) == 0.8039


def test_score_efgm_uses_geometric_mean_for_positive_factors():
    model_input = EFGMInput(
        task_id="geometric-mean-test",
        T=0.8,
        E=0.9,
        entropy=EntropyMetrics(
            contradiction_density=0.2,
            uncertainty_variance=0.3,
            memory_fragmentation=0.2,
            recursion_instability=0.1,
            context_decay=0.2,
        ),
        flow_quality=FlowQualityMetrics(
            task_completion_consistency=0.8,
            reasoning_continuity=0.7,
            semantic_coherence=0.75,
            verification_success_rate=0.6,
        ),
    )

    result = score_efgm(model_input)

    assert result.e == 0.205
    assert result.Fq == 0.7225
    assert result.F == 0.6671
    assert result.classification == "Stable with watch items"
