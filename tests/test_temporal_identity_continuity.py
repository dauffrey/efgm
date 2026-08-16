import pytest

from efgm.exp0005_temporal_recovery import DEVELOPMENT_CASE_SPECS, _build_states
from efgm.scoring_v3 import load_agent_governance_config
from efgm.temporal_v0_3 import score_state_transition


def test_same_subject_can_change_task_identity_and_remain_comparable():
    """Task identity may change while the governed subject remains evidence-backed."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)

    after.assessment.task_id = "post-intervention-task"
    after.assessment.decision.task_id = "post-intervention-decision"

    result = score_state_transition(
        before,
        after,
        require_provenance=True,
        config=load_agent_governance_config(),
    )

    assert result.from_task_id != result.to_task_id
    assert result.identity_continuity_valid is True
    assert result.identity_issues == []
    assert result.verified_recovery_signal is True


def test_same_sequence_different_governed_subject_is_rejected():
    """A reused sequence label cannot bind two different governed subjects."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)
    after.governed_subject_id = "subject:unrelated-agent"

    with pytest.raises(ValueError, match="governed_subject_id"):
        score_state_transition(
            before,
            after,
            require_provenance=True,
            config=load_agent_governance_config(),
        )


def test_missing_identity_evidence_blocks_recovery_signals():
    """Matching subject labels alone are not sufficient evidence of continuity."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)
    after.identity_evidence_refs = []

    result = score_state_transition(
        before,
        after,
        require_provenance=True,
        config=load_agent_governance_config(),
    )

    assert result.identity_continuity_valid is False
    assert "identity.after: missing identity_evidence_refs" in result.identity_issues
    assert result.recovery_progress_signal is False
    assert result.verified_recovery_signal is False
