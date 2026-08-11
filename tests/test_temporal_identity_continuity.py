from efgm.exp0005_temporal_recovery import DEVELOPMENT_CASE_SPECS, _build_states
from efgm.scoring_v3 import load_agent_governance_config
from efgm.temporal_v0_3 import score_state_transition


def test_same_sequence_different_task_identity_can_be_verified_as_recovery():
    """Falsification: sequence_id alone does not prove before/after task continuity."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)

    # Preserve the same caller-supplied sequence_id but replace the post-state
    # assessment identity with an unrelated task identifier.
    after.assessment.task_id = "unrelated-post-intervention-task"
    after.assessment.decision.task_id = "unrelated-post-intervention-decision"

    result = score_state_transition(
        before,
        after,
        require_provenance=True,
        config=load_agent_governance_config(),
    )

    assert result.from_task_id != result.to_task_id
    # Current behavior documents the counterexample: the transition is still
    # accepted as verified recovery despite identity discontinuity.
    assert result.verified_recovery_signal is True
