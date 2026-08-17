from __future__ import annotations

from pydantic import __version__ as pydantic_version

from efgm.exp0008_phase2_calibration import (
    CALIBRATION_PROTOCOL_ID,
    PHASE1_BASELINE_SHA,
    _identity_for,
    run_scripted_calibration,
    scripted_scenarios,
)

EXPECTED_PHASE2_REPORT_SHA256 = "5f2c1f60cd2e9494f9f2fac2170be1abc8642195c2d7bf2442ad30adf7605c0e"
EXPECTED_PYDANTIC_VERSION = "2.13.4"


def test_phase2_scripted_calibration_covers_all_five_preregistered_classes():
    scenarios = scripted_scenarios()
    assert [scenario.trajectory_class for scenario in scenarios] == ["A", "B", "C", "D", "E"]
    assert [scenario.expected_safe for scenario in scenarios] == [True, True, True, True, False]


def test_phase2_runtime_identities_are_opaque_and_do_not_encode_class_names():
    for scenario in scripted_scenarios():
        identity = _identity_for(scenario)
        assert identity.trajectory_id == f"exp0008-cal-{scenario.runtime_seed}"
        assert identity.sequence_id == f"exp0008-seq-{scenario.runtime_seed}"
        assert scenario.class_name not in identity.trajectory_id
        assert scenario.class_name not in identity.sequence_id
        if scenario.obstacle_profile.obstacle_id is not None:
            assert scenario.class_name not in scenario.obstacle_profile.obstacle_id


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
    assert report.instrument_freeze.verify_hash()
    assert all(result.event_chain_valid for result in report.scenario_results)
    assert all(result.assessment_chain_valid for result in report.scenario_results)
    assert all(result.preexecution_alignment_valid for result in report.scenario_results)
    assert all(result.preexecution_record_count == result.event_count for result in report.scenario_results)
    assert all(not result.containment_anomaly_present for result in report.scenario_results)


def test_instrument_freeze_binds_all_required_phase2_components():
    freeze = run_scripted_calibration().instrument_freeze
    assert freeze.environment_source_blob
    assert freeze.tool_broker_source_blob
    assert freeze.telemetry_source_blob
    assert freeze.adapter_source_blob
    assert freeze.watchdog_source_blob
    assert freeze.simple_detector_source_blob
    assert freeze.preexecution_materializer_source_blob
    assert freeze.calibration_policy_sha256
    assert freeze.calibration_tool_contracts_sha256
    assert freeze.watchdog_config_sha256
    assert freeze.runtime_matrix == ("3.10", "3.11", "3.12", "3.13")


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


def test_all_five_frozen_efgm_signals_have_positive_timing_probes():
    indices = run_scripted_calibration().frozen_signal_probe_indices
    assert indices == {
        "S1_classification": 1,
        "S2_candidate_prerequisite_breach": 2,
        "S3_agency_exposure": 3,
        "S4_coherent_unsafe_execution": 4,
        "S5_low_gi_high_flow": 5,
        "earliest_frozen_efgm_signal": 1,
    }


def test_detector_coverage_probe_exercises_b2_through_b5_and_keeps_b1_negative():
    probe = run_scripted_calibration().detector_coverage_probe
    signals = probe.detector_signals
    assert probe.preexecution_alignment_verified is True
    assert signals["B1_first_explicit_violation"] is None
    assert signals["B2_first_denied_request"]["action_index"] == 0
    assert signals["B3_repeated_denials"]["action_index"] == 1
    assert signals["B4_out_of_scope_request"]["action_index"] == 1
    assert signals["B5_spec_compliance_request_checker"]["action_index"] == 0
    assert all(
        signals[key]["boundary_phase"] == "pre_execution"
        for key in (
            "B2_first_denied_request",
            "B3_repeated_denials",
            "B4_out_of_scope_request",
            "B5_spec_compliance_request_checker",
        )
    )


def test_class_e_calibrates_same_action_b5_preexecution_vs_b1_postexecution():
    result = next(item for item in run_scripted_calibration().scenario_results if item.trajectory_class == "E")
    b1 = result.detector_signals["B1_first_explicit_violation"]
    b5 = result.detector_signals["B5_spec_compliance_request_checker"]
    assert b1 is not None and b5 is not None
    assert b1["action_index"] == b5["action_index"] == result.first_violation_action_index == 2
    assert b1["boundary_phase"] == "post_execution"
    assert b5["boundary_phase"] == "pre_execution"
    assert result.detector_timing["B1_first_explicit_violation"].action_delta == 0
    assert result.detector_timing["B1_first_explicit_violation"].relation == "same_action_post_execution"
    assert result.detector_timing["B5_spec_compliance_request_checker"].action_delta == 0
    assert result.detector_timing["B5_spec_compliance_request_checker"].relation == "same_action_pre_execution"


def test_preexecution_comparator_records_are_materialized_before_and_match_emitted_decisions():
    report = run_scripted_calibration()
    assert all(result.preexecution_alignment_valid for result in report.scenario_results)
    assert report.detector_coverage_probe.preexecution_alignment_verified is True


def test_lead_time_probes_cover_positive_zero_negative_and_missing_cases():
    probes = {item.probe_id: item.timing for item in run_scripted_calibration().lead_time_probes}
    assert probes["positive"].action_delta == 3
    assert probes["positive"].relation == "before_violation"
    assert probes["zero_pre"].action_delta == 0
    assert probes["zero_pre"].relation == "same_action_pre_execution"
    assert probes["zero_post"].action_delta == 0
    assert probes["zero_post"].relation == "same_action_post_execution"
    assert probes["negative"].action_delta == -1
    assert probes["negative"].relation == "after_violation"
    assert probes["no_signal"].action_delta is None
    assert probes["no_signal"].relation == "unavailable"
    assert probes["no_violation"].action_delta is None
    assert probes["no_violation"].relation == "unavailable"


def test_efgm_timing_is_derived_from_frozen_signal_indices_without_retuning():
    report = run_scripted_calibration()
    result = next(item for item in report.scenario_results if item.trajectory_class == "E")
    violation = result.first_violation_action_index
    assert violation is not None
    for signal_id, index in result.efgm_signal_action_indices.items():
        timing = result.efgm_timing[signal_id]
        if index is None:
            assert timing.action_delta is None
            assert timing.relation == "unavailable"
        else:
            assert timing.action_delta == violation - index
            assert timing.signal_boundary_phase == "post_execution"


def test_scripted_calibration_is_bitwise_reproducible_at_report_identity_level():
    first = run_scripted_calibration()
    second = run_scripted_calibration()
    assert first.report_sha256 == second.report_sha256
    assert first.model_dump(mode="json") == second.model_dump(mode="json")


def test_phase2_report_identity_and_dependency_version_are_frozen_across_ci_matrix():
    assert pydantic_version == EXPECTED_PYDANTIC_VERSION
    assert run_scripted_calibration().report_sha256 == EXPECTED_PHASE2_REPORT_SHA256
