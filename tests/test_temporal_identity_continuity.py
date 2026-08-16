import pytest
from pydantic import ValidationError

from efgm.exp0005_temporal_recovery import DEVELOPMENT_CASE_SPECS, _build_states
from efgm.schemas_v3 import EFGMAgentGovernanceInput
from efgm.scoring_v3 import load_agent_governance_config
from efgm.temporal_v0_3 import EFGMAgentState, score_state_transition


def test_same_subject_can_change_task_identity_and_remain_comparable():
    """Task may change between states while each governance envelope stays internally bound."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)

    after.assessment.task_id = "post-intervention-task"
    after.assessment.decision.task_id = "post-intervention-task"

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


def test_agent_governance_rejects_outer_nested_task_identity_mismatch():
    """A governance envelope cannot combine governance and decision data for different tasks."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    _, after = _build_states(spec)
    payload = after.assessment.model_dump(mode="json")
    payload["task_id"] = "governance-task"
    payload["decision"]["task_id"] = "different-decision-task"

    with pytest.raises(ValidationError, match="decision.task_id"):
        EFGMAgentGovernanceInput.model_validate(payload)


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


@pytest.mark.parametrize(
    ("field_name", "bad_value"),
    [
        ("governed_subject_id", "   "),
        ("identity_scorer_id", "\t"),
        ("identity_evidence_refs", ["  "]),
    ],
)
def test_blank_identity_provenance_is_rejected_at_schema_boundary(field_name, bad_value):
    spec = DEVELOPMENT_CASE_SPECS[0]
    _, after = _build_states(spec)
    payload = after.model_dump(mode="json")
    payload[field_name] = bad_value

    with pytest.raises(ValidationError, match="blank|whitespace"):
        EFGMAgentState.model_validate(payload)


def test_full_state_hash_binds_identity_evidence_beyond_assessment_hash():
    """Identity evidence can change recovery evidence and must therefore change state identity."""
    spec = DEVELOPMENT_CASE_SPECS[0]
    before, after = _build_states(spec)
    config = load_agent_governance_config()

    first = score_state_transition(before, after, require_provenance=True, config=config)
    changed_after = after.model_copy(deep=True)
    changed_after.identity_evidence_refs = [
        "experiment://EFGM-CE-0004/alternate-independent-identity-evidence"
    ]
    second = score_state_transition(
        before,
        changed_after,
        require_provenance=True,
        config=config,
    )

    assert first.after_input_sha256 == second.after_input_sha256
    assert first.after_state_sha256 != second.after_state_sha256
    assert len(first.before_state_sha256) == 64
    assert len(first.after_state_sha256) == 64
    assert first.verified_recovery_signal is True
    assert second.verified_recovery_signal is True
