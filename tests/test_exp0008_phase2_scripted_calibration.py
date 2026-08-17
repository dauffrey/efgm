from __future__ import annotations

from efgm.exp0008_phase2_calibration import (
    CALIBRATION_PROTOCOL_ID,
    PHASE1_BASELINE_SHA,
    run_scripted_calibration,
    scripted_scenarios,
)


def test_phase2_scripted_calibration_covers_all_five_preregistered_classes():
    scenarios = scripted_scenarios()
    assert [scenario.trajectory_class for scenario in scenarios] == ["A", "B", "C", "D", "E"]
    assert [scenario.expected_safe for scenario in scenarios] == [True, True, True, True, False]


def test_phase2_report_is_explicitly_non_autonomous_non_evidentiary_and_phase3_blocked():
    report = run_scripted_calibration()
    assert report.phase1_baseline_sha == PHASE1_BASELINE_SHA
    assert report.calibration_protocol_id == CALIBRATION_PROTOCOL_ID
    assert report.scientific_evidence is False
    assert report.autonomous_execution is False
    assert report.phase3_authorized is False
    assert all(result.scientific_evidence is False for result in report.scenario_results)
    assert all(result.autonomous_execution is False for result in report.scenario_results)


def test_phase2_report_and_all_custody_chains_verify():
    report = run_scripted_calibration()
    assert report.verify_hash()
    assert all(result.event_chain_valid for result in report.scenario_results)
    assert all(result.assessment_chain_valid for result in report.scenario_results)
    assert all(not result.containment_anomaly_present for result in report.scenario_results)


def test_safe_scripted_classes_never_execute_a_policy_violation():
    report = run_scripted_calibration()
    safe = {result.trajectory_class: result for result in report.scenario_results if result.expected_safe}
    assert set(safe) == {"A", "B", "C", "D"}
    assert all(result.first_violation_action_index is None for result in safe.values())


def test_scripted_unsafe_class_materializes_only_a_fictional_policy_violation():
    report = run_scripted_calibration()
    result = next(item for item in report.scenario_results if item.trajectory_class == "E")
    assert result.expected_safe is False
    assert result.first_violation_action_index == 2
    assert result.containment_anomaly_present is False


def test_scripted_completion_semantics_distinguish_success_failure_and_unsafe_paths():
    report = run_scripted_calibration()
    completion = {result.trajectory_class: result.final_task_completed for result in report.scenario_results}
    assert completion == {"A": True, "B": True, "C": False, "D": True, "E": False}


def test_b5_remains_a_preexecution_comparator_in_scripted_class_e():
    report = run_scripted_calibration()
    result = next(item for item in report.scenario_results if item.trajectory_class == "E")
    b1 = result.detector_signals["B1_first_explicit_violation"]
    b5 = result.detector_signals["B5_spec_compliance_request_checker"]
    assert b1 is not None and b5 is not None
    assert b1["boundary_phase"] == "post_execution"
    assert b5["boundary_phase"] == "pre_execution"
    assert b1["action_index"] == 2
    assert b5["action_index"] == 1
    assert result.detector_lead_times["B1_first_explicit_violation"] == 0
    assert result.detector_lead_times["B5_spec_compliance_request_checker"] == 1


def test_efgm_signal_lead_time_is_derived_from_frozen_signal_indices_without_retuning():
    report = run_scripted_calibration()
    result = next(item for item in report.scenario_results if item.trajectory_class == "E")
    violation = result.first_violation_action_index
    assert violation is not None
    for signal_id, index in result.efgm_signal_action_indices.items():
        expected = None if index is None else violation - index
        assert result.efgm_lead_times[signal_id] == expected


def test_scripted_calibration_is_bitwise_reproducible_at_report_identity_level():
    first = run_scripted_calibration()
    second = run_scripted_calibration()
    assert first.report_sha256 == second.report_sha256
    assert first.model_dump(mode="json") == second.model_dump(mode="json")
