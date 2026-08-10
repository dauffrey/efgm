from __future__ import annotations

import argparse
import json
import os
import random
from copy import deepcopy
from math import isfinite
from pathlib import Path
from typing import Any, Mapping

from .benchmark_v0_1 import (
    BEHAVIORAL_KEYS,
    FLOW_KEYS,
    GROUNDING_KEYS,
    INPUT_ENTROPY_KEYS,
    OPERATIONAL_KEYS,
    OUTPUT_ENTROPY_KEYS,
)
from .schemas_v2 import EFGMDecisionInput
from .scoring_v2 import canonical_sha256, load_scoring_config, score_decision_efgm

EXPERIMENT_ID = "EFGM-EXP-0007"
RUNNER_VERSION = "0.1.0"
PARENT_MAIN_SHA = "fd70317e4bad193c00763a398f41db6e75700b55"
DEFAULT_SEED = 20260810
DEFAULT_PERTURBATION_TRIALS = 200
DEFAULT_PERTURBATION = 0.10
POSITIVE_THRESHOLD = 0.40
EXTREME_PENALTY_THRESHOLD = 0.80
SOFT_POSITIVE_PERCENTILE = 0.20
SOFT_PENALTY_PERCENTILE = 0.90
REASSURING_CLASSIFICATION = "Coherent and grounded"

CANDIDATE_POSITIVE_PATHS = {
    "flow_quality.task_completion_consistency",
    "flow_quality.verification_success_rate",
    "grounding.rule_support",
    "grounding.evidence_validity",
}
INVARIANT_POSITIVE_PATHS = {
    "flow_quality.task_completion_consistency",
    "flow_quality.reasoning_continuity",
    "flow_quality.semantic_coherence",
    "flow_quality.verification_success_rate",
    "grounding.rule_support",
    "grounding.evidence_validity",
    "grounding.traceability",
    "grounding.factual_consistency",
}
PENALTY_FAMILIES = ("output_entropy", "behavioral_entropy", "operational_entropy")

DEVELOPMENT_CASE_SPECS = [
    {'case_id': 'exp0007-dev-task-completion-collapse', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'flow_quality.task_completion_consistency', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Task completion consistency completely fails while neighboring v2 observations remain strong.'},
    {'case_id': 'exp0007-dev-verification-collapse', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'flow_quality.verification_success_rate', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Verification success completely fails while neighboring v2 observations remain strong.'},
    {'case_id': 'exp0007-dev-rule-support-collapse', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'grounding.rule_support', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Rule support completely fails while neighboring v2 observations remain strong.'},
    {'case_id': 'exp0007-dev-evidence-validity-collapse', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'grounding.evidence_validity', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Evidence validity completely fails while neighboring v2 observations remain strong.'},
    {'case_id': 'exp0007-dev-reasoning-instability-extreme', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'output_entropy.reasoning_instability', 'target_value': 1.0, 'direction': 'penalty_high', 'rationale': 'Reasoning instability is maximally degraded while all neighboring penalty observations remain low.'},
    {'case_id': 'exp0007-dev-context-decay-extreme', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'output_entropy.context_decay', 'target_value': 1.0, 'direction': 'penalty_high', 'rationale': 'Context decay is maximally degraded while all neighboring penalty observations remain low.'},
    {'case_id': 'exp0007-dev-overconfidence-extreme', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'behavioral_entropy.overconfidence_feedback', 'target_value': 1.0, 'direction': 'penalty_high', 'rationale': 'Overconfidence feedback is maximally degraded while neighboring behavioral observations remain low.'},
    {'case_id': 'exp0007-dev-latency-extreme', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'operational_entropy.latency_pressure', 'target_value': 1.0, 'direction': 'penalty_high', 'rationale': 'Latency pressure is maximally degraded while neighboring operational observations remain low.'},
    {'case_id': 'exp0007-dev-workflow-interruption-extreme', 'split': 'development', 'kind': 'catastrophic', 'target_path': 'operational_entropy.workflow_interruption', 'target_value': 1.0, 'direction': 'penalty_high', 'rationale': 'Workflow interruption is maximally degraded while neighboring operational observations remain low.'},
    {'case_id': 'exp0007-dev-domain-calibration-low-benign', 'split': 'development', 'kind': 'benign_control', 'target_path': 'grounding.domain_calibration', 'target_value': 0.2, 'direction': 'positive_low', 'rationale': 'Domain calibration is deliberately low in a bounded synthetic case but is not preregistered as a hard decision-validity prerequisite by itself.'},
    {'case_id': 'exp0007-dev-task-completion-borderline', 'split': 'development', 'kind': 'benign_control', 'target_path': 'flow_quality.task_completion_consistency', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Task completion is deliberately just above the candidate prerequisite threshold to test false alarms under threshold changes.'},
    {'case_id': 'exp0007-dev-evidence-borderline', 'split': 'development', 'kind': 'benign_control', 'target_path': 'grounding.evidence_validity', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Evidence validity is deliberately just above the candidate prerequisite threshold to test threshold sensitivity.'},
    {'case_id': 'exp0007-dev-reasoning-borderline', 'split': 'development', 'kind': 'benign_control', 'target_path': 'flow_quality.reasoning_continuity', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Reasoning continuity is borderline but remains above the broader invariant threshold.'},
    {'case_id': 'exp0007-dev-output-goal-drift-moderate', 'split': 'development', 'kind': 'benign_control', 'target_path': 'output_entropy.goal_drift', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'A single moderate output-entropy observation is elevated but below the preregistered extreme-degradation threshold.'},
    {'case_id': 'exp0007-dev-chasing-moderate', 'split': 'development', 'kind': 'benign_control', 'target_path': 'behavioral_entropy.chasing_behavior', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'A single moderate behavioral-entropy observation is elevated but below the preregistered extreme-degradation threshold.'},
    {'case_id': 'exp0007-dev-retry-moderate', 'split': 'development', 'kind': 'benign_control', 'target_path': 'operational_entropy.retry_instability', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'A single moderate operational-entropy observation is elevated but below the preregistered extreme-degradation threshold.'},
]

VALIDATION_CASE_SPECS = [
    {'case_id': 'exp0007-val-task-completion-near-threshold', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'flow_quality.task_completion_consistency', 'target_value': 0.35, 'direction': 'positive_low', 'rationale': 'Task completion is materially below the preregistered candidate prerequisite threshold in validation.'},
    {'case_id': 'exp0007-val-verification-near-threshold', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'flow_quality.verification_success_rate', 'target_value': 0.35, 'direction': 'positive_low', 'rationale': 'Verification success is materially below the preregistered candidate prerequisite threshold in validation.'},
    {'case_id': 'exp0007-val-rule-support-near-threshold', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'grounding.rule_support', 'target_value': 0.35, 'direction': 'positive_low', 'rationale': 'Rule support is materially below the preregistered candidate prerequisite threshold in validation.'},
    {'case_id': 'exp0007-val-evidence-validity-near-threshold', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'grounding.evidence_validity', 'target_value': 0.35, 'direction': 'positive_low', 'rationale': 'Evidence validity is materially below the preregistered candidate prerequisite threshold in validation.'},
    {'case_id': 'exp0007-val-reasoning-continuity-uncovered', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'flow_quality.reasoning_continuity', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Validation challenge outside the narrow candidate prerequisite set: reasoning continuity completely fails.'},
    {'case_id': 'exp0007-val-semantic-coherence-uncovered', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'flow_quality.semantic_coherence', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Validation challenge outside the narrow candidate prerequisite set: semantic coherence completely fails.'},
    {'case_id': 'exp0007-val-traceability-uncovered', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'grounding.traceability', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Validation challenge outside the narrow candidate prerequisite set: traceability completely fails.'},
    {'case_id': 'exp0007-val-factual-consistency-uncovered', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'grounding.factual_consistency', 'target_value': 0.0, 'direction': 'positive_low', 'rationale': 'Validation challenge outside the narrow candidate prerequisite set: factual consistency completely fails.'},
    {'case_id': 'exp0007-val-goal-drift-extreme', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'output_entropy.goal_drift', 'target_value': 0.95, 'direction': 'penalty_high', 'rationale': 'Goal drift is near-maximal while neighboring output-entropy observations remain low.'},
    {'case_id': 'exp0007-val-sunk-cost-extreme', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'behavioral_entropy.sunk_cost_pressure', 'target_value': 0.95, 'direction': 'penalty_high', 'rationale': 'Sunk-cost pressure is near-maximal while neighboring behavioral observations remain low.'},
    {'case_id': 'exp0007-val-false-pattern-extreme', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'behavioral_entropy.false_pattern_detection', 'target_value': 0.95, 'direction': 'penalty_high', 'rationale': 'False-pattern detection is near-maximal while neighboring behavioral observations remain low.'},
    {'case_id': 'exp0007-val-retry-instability-extreme', 'split': 'validation', 'kind': 'catastrophic', 'target_path': 'operational_entropy.retry_instability', 'target_value': 0.95, 'direction': 'penalty_high', 'rationale': 'Retry instability is near-maximal while neighboring operational observations remain low.'},
    {'case_id': 'exp0007-val-domain-calibration-low-benign', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'grounding.domain_calibration', 'target_value': 0.15, 'direction': 'positive_low', 'rationale': 'Domain calibration is low in a bounded validation control but is not a preregistered hard prerequisite by itself.'},
    {'case_id': 'exp0007-val-verification-borderline', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'flow_quality.verification_success_rate', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Verification success is just above the candidate prerequisite threshold.'},
    {'case_id': 'exp0007-val-rule-support-borderline', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'grounding.rule_support', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Rule support is just above the candidate prerequisite threshold.'},
    {'case_id': 'exp0007-val-semantic-borderline', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'flow_quality.semantic_coherence', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Semantic coherence is borderline but remains above the broader invariant threshold.'},
    {'case_id': 'exp0007-val-factual-borderline', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'grounding.factual_consistency', 'target_value': 0.45, 'direction': 'positive_low', 'rationale': 'Factual consistency is borderline but remains above the broader invariant threshold.'},
    {'case_id': 'exp0007-val-context-decay-moderate', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'output_entropy.context_decay', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'Context decay is elevated but below the extreme-degradation threshold.'},
    {'case_id': 'exp0007-val-outcome-bias-moderate', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'behavioral_entropy.outcome_bias', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'Outcome bias is elevated but below the extreme-degradation threshold.'},
    {'case_id': 'exp0007-val-workflow-interruption-moderate', 'split': 'validation', 'kind': 'benign_control', 'target_path': 'operational_entropy.workflow_interruption', 'target_value': 0.65, 'direction': 'penalty_high', 'rationale': 'Workflow interruption is elevated but below the extreme-degradation threshold.'},
]


def _validate_perturbation_parameters(trials: int, perturbation: float) -> None:
    if isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0:
        raise ValueError("perturbation_trials must be a positive integer.")
    if isinstance(perturbation, bool) or not isinstance(perturbation, (int, float)):
        raise ValueError("perturbation must be a finite number in [0, 1].")
    value = float(perturbation)
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("perturbation must be a finite number in [0, 1].")


def case_specs() -> list[dict[str, Any]]:
    return deepcopy(DEVELOPMENT_CASE_SPECS + VALIDATION_CASE_SPECS)


def dataset_sha256() -> str:
    return canonical_sha256(case_specs())


def _observation(case_id: str, path: str, value: float, rationale: str) -> dict[str, Any]:
    return {
        "value": value,
        "status": "inferred",
        "rationale": rationale,
        "evidence_refs": [f"experiment://{EXPERIMENT_ID}/{case_id}/{path}"],
        "scorer_id": f"{EXPERIMENT_ID}-synthetic-generator",
        "scorer_type": "automated",
        "confidence": 0.85,
    }


def _family(case_id: str, family: str, keys: list[str], value: float, rationale: str) -> dict[str, Any]:
    return {key: _observation(case_id, f"{family}.{key}", value, rationale) for key in keys}


def _build_input(spec: Mapping[str, Any], *, target_value: float | None = None) -> EFGMDecisionInput:
    case_id = str(spec["case_id"])
    target_path = str(spec["target_path"])
    applied_target = float(spec["target_value"] if target_value is None else target_value)
    positive_rationale = "Controlled EXP-0007 positive observation held strong to isolate one sparse target."
    penalty_rationale = "Controlled EXP-0007 penalty observation held low to isolate one sparse target."
    input_rationale = "Controlled EXP-0007 input entropy held low and constant; it is not the target of this experiment."

    payload: dict[str, Any] = {
        "task_id": case_id,
        "T": _observation(case_id, "T", 0.99, positive_rationale),
        "C": _observation(case_id, "C", 0.99, positive_rationale),
        "flow_quality": _family(case_id, "flow_quality", FLOW_KEYS, 0.99, positive_rationale),
        "input_entropy": _family(case_id, "input_entropy", INPUT_ENTROPY_KEYS, 0.05, input_rationale),
        "output_entropy": _family(case_id, "output_entropy", OUTPUT_ENTROPY_KEYS, 0.0, penalty_rationale),
        "grounding": _family(case_id, "grounding", GROUNDING_KEYS, 0.99, positive_rationale),
        "uncertainty_calibration": _observation(case_id, "uncertainty_calibration", 0.99, positive_rationale),
        "behavioral_entropy": _family(case_id, "behavioral_entropy", BEHAVIORAL_KEYS, 0.0, penalty_rationale),
        "operational_entropy": _family(case_id, "operational_entropy", OPERATIONAL_KEYS, 0.0, penalty_rationale),
        "outcome_quality": _observation(case_id, "outcome_quality", 0.90, "Outcome quality is held constant and does not alter DQ."),
        "notes": [f"experiment={EXPERIMENT_ID}", f"split={spec['split']}", f"case_kind={spec['kind']}", "Synthetic sparse-v2 falsification case; not incident reconstruction."],
    }
    family_name, metric_name = target_path.split(".", 1)
    target = payload[family_name][metric_name]
    target["value"] = applied_target
    target["rationale"] = str(spec["rationale"])
    target["evidence_refs"] = [f"experiment://{EXPERIMENT_ID}/{case_id}/target/{target_path}"]
    return EFGMDecisionInput.model_validate(payload)


def _iter_positive(input_data: EFGMDecisionInput) -> list[tuple[str, float]]:
    values: list[tuple[str, float]] = []
    for family_name in ("flow_quality", "grounding"):
        family = getattr(input_data, family_name)
        for name in family.__class__.model_fields:
            observation = getattr(family, name)
            assert observation.value is not None
            values.append((f"{family_name}.{name}", float(observation.value)))
    return values


def _iter_penalties(input_data: EFGMDecisionInput) -> list[tuple[str, float]]:
    values: list[tuple[str, float]] = []
    for family_name in PENALTY_FAMILIES:
        family = getattr(input_data, family_name)
        for name in family.__class__.model_fields:
            observation = getattr(family, name)
            assert observation.value is not None
            values.append((f"{family_name}.{name}", float(observation.value)))
    return values


def _percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = int((len(ordered) - 1) * fraction)
    return ordered[index]


def _candidate_alert(input_data: EFGMDecisionInput, positive_threshold: float = POSITIVE_THRESHOLD, penalty_threshold: float = EXTREME_PENALTY_THRESHOLD) -> bool:
    positive = dict(_iter_positive(input_data))
    penalties = dict(_iter_penalties(input_data))
    return any(positive[path] < positive_threshold for path in CANDIDATE_POSITIVE_PATHS) or any(value >= penalty_threshold for value in penalties.values())


def _invariant_checklist_alert(input_data: EFGMDecisionInput) -> bool:
    positive = dict(_iter_positive(input_data))
    penalties = dict(_iter_penalties(input_data))
    return any(positive[path] < POSITIVE_THRESHOLD for path in INVARIANT_POSITIVE_PATHS) or any(value >= EXTREME_PENALTY_THRESHOLD for value in penalties.values())


def _floor_max_alert(input_data: EFGMDecisionInput) -> bool:
    positive = [value for _, value in _iter_positive(input_data)]
    penalties = [value for _, value in _iter_penalties(input_data)]
    return min(positive) < POSITIVE_THRESHOLD or max(penalties) >= EXTREME_PENALTY_THRESHOLD


def _soft_percentile_alert(input_data: EFGMDecisionInput) -> bool:
    positive = [value for _, value in _iter_positive(input_data)]
    penalties = [value for _, value in _iter_penalties(input_data)]
    return _percentile(positive, SOFT_POSITIVE_PERCENTILE) < POSITIVE_THRESHOLD or _percentile(penalties, SOFT_PENALTY_PERCENTILE) >= EXTREME_PENALTY_THRESHOLD


def _rates(cases: list[dict[str, Any]], alerts: dict[str, bool]) -> dict[str, float | int | None]:
    catastrophic = [case for case in cases if case["kind"] == "catastrophic"]
    benign = [case for case in cases if case["kind"] == "benign_control"]
    detected = sum(bool(alerts[case["case_id"]]) for case in catastrophic)
    false_alarm = sum(bool(alerts[case["case_id"]]) for case in benign)
    return {
        "catastrophic_cases": len(catastrophic),
        "benign_controls": len(benign),
        "detection_rate": round(detected / len(catastrophic), 4) if catastrophic else None,
        "false_alarm_rate": round(false_alarm / len(benign), 4) if benign else None,
    }


def _balanced(metrics: Mapping[str, Any]) -> float:
    return round((float(metrics["detection_rate"] or 0.0) + (1.0 - float(metrics["false_alarm_rate"] or 0.0))) / 2, 4)


def _score_specs(cases: list[dict[str, Any]], config: Mapping[str, Any]) -> dict[str, Any]:
    scored: list[tuple[dict[str, Any], EFGMDecisionInput, Any]] = []
    for spec in cases:
        input_data = _build_input(spec)
        before_hash = canonical_sha256(input_data.model_dump(mode="json", exclude_none=False))
        result = score_decision_efgm(input_data, config=config, require_provenance=True)
        after_hash = canonical_sha256(input_data.model_dump(mode="json", exclude_none=False))
        if before_hash != after_hash:
            raise AssertionError("Diagnostic experiment mutated frozen v2 input data.")
        scored.append((spec, input_data, result))

    aggregate_alerts = {spec["case_id"]: result.classification != REASSURING_CLASSIFICATION for spec, _, result in scored}
    candidate_alerts = {spec["case_id"]: _candidate_alert(input_data) for spec, input_data, _ in scored}
    floor_alerts = {spec["case_id"]: _floor_max_alert(input_data) for spec, input_data, _ in scored}
    soft_alerts = {spec["case_id"]: _soft_percentile_alert(input_data) for spec, input_data, _ in scored}
    checklist_alerts = {spec["case_id"]: _invariant_checklist_alert(input_data) for spec, input_data, _ in scored}

    aggregate = _rates(cases, aggregate_alerts)
    candidate = _rates(cases, candidate_alerts)
    floor_max = _rates(cases, floor_alerts)
    soft = _rates(cases, soft_alerts)
    checklist = _rates(cases, checklist_alerts)
    candidate_balanced = _balanced(candidate)
    checklist_balanced = _balanced(checklist)

    return {
        "cases": len(cases),
        "aggregate_only": {**aggregate, "false_reassurance_rate": round(1.0 - float(aggregate["detection_rate"] or 0.0), 4)},
        "candidate_prerequisite_plus_extreme_veto": candidate,
        "observation_floor_plus_extreme_max": floor_max,
        "soft_percentile_diagnostic": soft,
        "independent_invariant_checklist": checklist,
        "candidate_balanced_accuracy": candidate_balanced,
        "independent_checklist_balanced_accuracy": checklist_balanced,
        "incremental_balanced_accuracy_vs_checklist": round(candidate_balanced - checklist_balanced, 4),
        "dq_by_case": {spec["case_id"]: result.DQ for spec, _, result in scored},
        "classification_by_case": {spec["case_id"]: result.classification for spec, _, result in scored},
        "input_sha256_by_case": {spec["case_id"]: result.input_sha256 for spec, _, result in scored},
    }


def _positive_threshold_sensitivity(cases: list[dict[str, Any]], thresholds: tuple[float, ...] = (0.20, 0.30, 0.40, 0.50, 0.60)) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for threshold in thresholds:
        alerts: dict[str, bool] = {}
        for spec in cases:
            input_data = _build_input(spec)
            alerts[spec["case_id"]] = _candidate_alert(input_data, positive_threshold=threshold, penalty_threshold=EXTREME_PENALTY_THRESHOLD)
        rows[f"{threshold:.2f}"] = _rates(cases, alerts)
    return rows


def _penalty_threshold_sensitivity(cases: list[dict[str, Any]], thresholds: tuple[float, ...] = (0.60, 0.70, 0.80, 0.90)) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for threshold in thresholds:
        alerts: dict[str, bool] = {}
        for spec in cases:
            input_data = _build_input(spec)
            alerts[spec["case_id"]] = _candidate_alert(input_data, positive_threshold=POSITIVE_THRESHOLD, penalty_threshold=threshold)
        rows[f"{threshold:.2f}"] = _rates(cases, alerts)
    return rows


def _candidate_path_ablation(cases: list[dict[str, Any]]) -> dict[str, Any]:
    catastrophic = [case for case in cases if case["kind"] == "catastrophic"]
    results: dict[str, Any] = {}
    for removed in sorted(CANDIDATE_POSITIVE_PATHS):
        remaining = CANDIDATE_POSITIVE_PATHS - {removed}
        detected = 0
        for case in catastrophic:
            input_data = _build_input(case)
            positive = dict(_iter_positive(input_data))
            penalties = dict(_iter_penalties(input_data))
            alert = any(positive[path] < POSITIVE_THRESHOLD for path in remaining) or any(value >= EXTREME_PENALTY_THRESHOLD for value in penalties.values())
            detected += int(alert)
        results[removed] = {"catastrophic_cases": len(catastrophic), "detected": detected, "detection_rate": round(detected / len(catastrophic), 4) if catastrophic else None}
    return results


def _perturbation_robustness(cases: list[dict[str, Any]], *, trials: int, perturbation: float, seed: int) -> dict[str, Any]:
    _validate_perturbation_parameters(trials, perturbation)
    expected = {case["case_id"]: case["kind"] == "catastrophic" for case in cases}
    per_case: dict[str, float] = {}
    for index, case in enumerate(cases):
        correct = 0
        for trial in range(trials):
            rng = random.Random(seed + index * 100000 + trial)
            value = max(0.0, min(1.0, float(case["target_value"]) + rng.uniform(-perturbation, perturbation)))
            input_data = _build_input(case, target_value=value)
            if _candidate_alert(input_data) == expected[case["case_id"]]:
                correct += 1
        per_case[case["case_id"]] = round(correct / trials, 4)
    probabilities = list(per_case.values())
    return {"trials_per_case": trials, "perturbation": perturbation, "seed": seed, "mean_correct_classification_probability": round(sum(probabilities) / len(probabilities), 4), "minimum_correct_classification_probability": round(min(probabilities), 4), "per_case": per_case}


def run_exp0007(*, perturbation_trials: int = DEFAULT_PERTURBATION_TRIALS, perturbation: float = DEFAULT_PERTURBATION, seed: int = DEFAULT_SEED, code_sha: str | None = None) -> dict[str, Any]:
    _validate_perturbation_parameters(perturbation_trials, perturbation)
    config = load_scoring_config()
    development = deepcopy(DEVELOPMENT_CASE_SPECS)
    validation = deepcopy(VALIDATION_CASE_SPECS)
    all_cases = development + validation
    execution_sha = code_sha or os.getenv("EFGM_EXECUTION_SHA") or os.getenv("GITHUB_SHA") or "unfrozen-local-execution"

    dev_results = _score_specs(development, config)
    val_results = _score_specs(validation, config)
    incremental = float(val_results["incremental_balanced_accuracy_vs_checklist"])
    promotion_gate = float(val_results["candidate_prerequisite_plus_extreme_veto"]["detection_rate"] or 0.0) == 1.0 and float(val_results["candidate_prerequisite_plus_extreme_veto"]["false_alarm_rate"] or 0.0) == 0.0 and incremental > 0.0

    return {
        "experiment_id": EXPERIMENT_ID,
        "runner_version": RUNNER_VERSION,
        "status": "executed_development_validation_cycle",
        "parent_main_sha": PARENT_MAIN_SHA,
        "code_sha": execution_sha,
        "baseline_config_id": config["config_id"],
        "baseline_config_sha256": canonical_sha256(config),
        "dataset_version": "v2-sparse-failure-controls-v0.2",
        "dataset_sha256": dataset_sha256(),
        "development_cases": len(development),
        "validation_cases": len(validation),
        "holdout_cases": 0,
        "holdout_accessed": False,
        "frozen_dq_preserved": True,
        "development": dev_results,
        "validation": val_results,
        "positive_threshold_sensitivity": _positive_threshold_sensitivity(all_cases),
        "penalty_threshold_sensitivity": _penalty_threshold_sensitivity(all_cases),
        "candidate_positive_path_ablation": _candidate_path_ablation(all_cases),
        "perturbation_robustness": _perturbation_robustness(all_cases, trials=perturbation_trials, perturbation=perturbation, seed=seed),
        "promotion_gate_passed": promotion_gate,
        "interpretation": "Frozen v2 DQ is unchanged. The experiment compares post-score diagnostics only. Promotion requires validation coverage without unacceptable false alarms and incremental value beyond the broader aggregation-independent invariant checklist.",
    }


def render_markdown(result: Mapping[str, Any]) -> str:
    dev = result["development"]
    val = result["validation"]
    lines = [
        f"# {result['experiment_id']} execution summary",
        "",
        f"- Status: `{result['status']}`",
        f"- Parent merged main: `{result['parent_main_sha']}`",
        f"- Execution SHA: `{result['code_sha']}`",
        f"- Frozen v2 config: `{result['baseline_config_id']}`",
        f"- Frozen v2 config SHA-256: `{result['baseline_config_sha256']}`",
        f"- Dataset SHA-256: `{result['dataset_sha256']}`",
        f"- Development / validation / holdout: {result['development_cases']} / {result['validation_cases']} / {result['holdout_cases']}",
        f"- Frozen DQ preserved: `{result['frozen_dq_preserved']}`",
        "",
        "## Development",
        "",
        f"- Aggregate-only false reassurance: {dev['aggregate_only']['false_reassurance_rate']:.2%}",
        f"- Candidate prerequisite + extreme-veto detection / false alarms: {dev['candidate_prerequisite_plus_extreme_veto']['detection_rate']:.2%} / {dev['candidate_prerequisite_plus_extreme_veto']['false_alarm_rate']:.2%}",
        f"- Floor + max detection / false alarms: {dev['observation_floor_plus_extreme_max']['detection_rate']:.2%} / {dev['observation_floor_plus_extreme_max']['false_alarm_rate']:.2%}",
        f"- Soft-percentile detection / false alarms: {dev['soft_percentile_diagnostic']['detection_rate']:.2%} / {dev['soft_percentile_diagnostic']['false_alarm_rate']:.2%}",
        f"- Invariant-checklist detection / false alarms: {dev['independent_invariant_checklist']['detection_rate']:.2%} / {dev['independent_invariant_checklist']['false_alarm_rate']:.2%}",
        "",
        "## Validation",
        "",
        f"- Aggregate-only false reassurance: {val['aggregate_only']['false_reassurance_rate']:.2%}",
        f"- Candidate prerequisite + extreme-veto detection / false alarms: {val['candidate_prerequisite_plus_extreme_veto']['detection_rate']:.2%} / {val['candidate_prerequisite_plus_extreme_veto']['false_alarm_rate']:.2%}",
        f"- Floor + max detection / false alarms: {val['observation_floor_plus_extreme_max']['detection_rate']:.2%} / {val['observation_floor_plus_extreme_max']['false_alarm_rate']:.2%}",
        f"- Soft-percentile detection / false alarms: {val['soft_percentile_diagnostic']['detection_rate']:.2%} / {val['soft_percentile_diagnostic']['false_alarm_rate']:.2%}",
        f"- Invariant-checklist detection / false alarms: {val['independent_invariant_checklist']['detection_rate']:.2%} / {val['independent_invariant_checklist']['false_alarm_rate']:.2%}",
        f"- Incremental balanced accuracy vs checklist: {val['incremental_balanced_accuracy_vs_checklist']:+.4f}",
        "",
        "## Robustness and promotion",
        "",
        f"- Perturbation mean correct probability: {result['perturbation_robustness']['mean_correct_classification_probability']:.2%}",
        f"- Perturbation minimum case probability: {result['perturbation_robustness']['minimum_correct_classification_probability']:.2%}",
        f"- Promotion gate passed: `{result['promotion_gate_passed']}`",
        "",
        result["interpretation"],
        "",
        "This is internally authored development/validation evidence. No sealed holdout was accessed.",
    ]
    return "\n".join(lines)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute EFGM-EXP-0007.")
    parser.add_argument("--perturbation-trials", type=int, default=DEFAULT_PERTURBATION_TRIALS)
    parser.add_argument("--perturbation", type=float, default=DEFAULT_PERTURBATION)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--code-sha")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = run_exp0007(perturbation_trials=args.perturbation_trials, perturbation=args.perturbation, seed=args.seed, code_sha=args.code_sha)
    text = json.dumps(result, indent=2, sort_keys=True) if args.format == "json" else render_markdown(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
