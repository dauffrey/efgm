from efgm.schemas import EFGMInput, EntropyMetrics, FlowQualityMetrics
from efgm.scoring import score_efgm


def test_score_efgm_returns_expected_shape():
    model_input = EFGMInput(
        task_id="unit-test",
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

    assert result.task_id == "unit-test"
    assert 0 <= result.F <= 1
    assert result.classification in {
        "Coherent",
        "Stable with watch items",
        "Degraded but usable",
        "High entropy",
        "Misaligned",
    }
