from __future__ import annotations

import copy
import random
from collections import defaultdict
from statistics import mean, median
from typing import Any, Callable

from .benchmark_v0_2 import (
    BENCHMARK_ID,
    EXPECTED_DATASET_SHA256,
    dataset_sha256,
    generate_cases,
)
from .schemas_v2 import EFGMDecisionInput
from .schemas_v3 import EFGMAgentGovernanceInput
from .scoring_v2 import score_decision_efgm
from .scoring_v3 import score_agent_governance

RUNNER_VERSION = "0.2.0"
FROZEN_BASELINE_SHA = "b717f611a0d09bd8e52bc1b0be5ee178eecacf25"
PARENT_RESEARCH_SHA = "a15007daeed221bde1f7a0f0e64cc870c1ae110b"
DEFAULT_SENSITIVITY_SEED = 20260808
MODEL_NAMES = (
    "v2_task_flow",
    "governed_product",
    "risk_adjusted_product",
    "governed_linear",
    "independent_governance_checklist",
)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, round(float(value), 4)))


def _observation(case: dict[str, Any], path: str, value: float) -> dict[str, Any]:
    return {
        "value": value,
        "status": "inferred",
        "rationale": (
            f"Controlled synthetic agent-governance assignment for family={case['family']}, "
            f"variant={case['variant']}, severity={case['severity']}."
        ),
        "evidence_refs": [f"benchmark://{BENCHMARK_ID}/{case['case_id']}/{path}"],
        "scorer_id": f"{BENCHMARK_ID}-generator",
        "scorer_type": "automated",
        "confidence": 0.85,
    }


def _observation_family(case: dict[str, Any], family: str, values: dict[str, float]) -> dict[str, Any]:
    return {
        name: _observation(case, f"{family}.{name}", value)
        for name, value in values.items()
    }


def case_to_v2_input(case: dict[str, Any]) -> EFGMDecisionInput:
    values = case["decision_values"]
    return EFGMDecisionInput.model_validate(
        {
            "task_id": case["case_id"],
            "T": _observation(case, "decision.T", values["T"]),
            "C": _observation(case, "decision.C", values["C"]),
            "flow_quality": _observation_family(case, "decision.flow_quality", values["flow_quality"]),
            "input_entropy": _observation_family(case, "decision.input_entropy", values["input_entropy"]),
            "output_entropy": _observation_family(case, "decision.output_entropy", values["output_entropy"]),
            "grounding": _observation_family(case, "decision.grounding", values["grounding"]),
            "uncertainty_calibration": _observation(
                case,
                "decision.uncertainty_calibration",
                values["uncertainty_calibration"],
            ),
            "behavioral_entropy": _observation_family(
                case,
                "decision.behavioral_entropy",
                values["behavioral_entropy"],
            ),
            "operational_entropy": _observation_family(
                case,
                "decision.operational_entropy",
                values["operational_entropy"],
            ),
            "outcome_quality": _observation(
                case,
                "decision.outcome_quality",
                values["outcome_quality"],
            ),
            "notes": [
                f"benchmark={BENCHMARK_ID}",
                f"pair={case['pair_id']}",
                f"family={case['family']}",
                f"split={case['split']}",
                f"label_source={case['label_source']}",
                "Black Hat USA 2026 is empirical inspiration only; this is not an incident reconstruction.",
            ],
        }
    )


def case_to_v3_input(case: dict[str, Any]) -> EFGMAgentGovernanceInput:
    governance = case["governance_values"]
    return EFGMAgentGovernanceInput.model_validate(
        {
            "task_id": case["case_id"],
            "decision": case_to_v2_input(case),
            "alignment": _observation_family(case, "alignment", governance["alignment"]),
            "boundary_integrity": _observation_family(
                case,
                "boundary_integrity",
                governance["boundary_integrity"],
            ),
            "observability": _observation_family(
                case,
                "observability",
                governance["observability"],
            ),
            "environmental_memory_governance": _observation_family(
                case,
                "environmental_memory_governance",
                governance["environmental_memory_governance"],
            ),
            "coordination_governance": _observation_family(
                case,
                "coordination_governance",
                governance["coordination_governance"],
            ),
            "control_recoverability": _observation_family(
                case,
                "control_recoverability",
                governance["control_recoverability"],
            ),
            "agency_amplification": _observation_family(
                case,
                "agency_amplification",
                governance["agency_amplification"],
            ),
            "notes": [
                f"benchmark={BENCHMARK_ID}",
                "Candidate v0.3 state only; not an accepted EFGM formula.",
            ],
        }
    )


def _checklist_score(case: dict[str, Any]) -> float:
    values = list(case["independent_governance_checklist"].values())
    return round(sum(values) / len(values), 4)


def score_case(case: dict[str, Any], model_name: str) -> float:
    if model_name == "v2_task_flow":
        return score_decision_efgm(case_to_v2_input(case), require_provenance=True).DQ

    result = score_agent_governance(case_to_v3_input(case), require_provenance=True)
    if model_name == "governed_product":
        return result.governed_flow_product
    if model_name == "risk_adjusted_product":
        return result.risk_adjusted_flow
    if model_name == "governed_linear":
        return result.governed_linear_score
    if model_name == "independent_governance_checklist":
        return _checklist_score(case)
    raise ValueError(f"Unknown comparison model {model_name!r}; expected one of {MODEL_NAMES}")


def _pairs(cases: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[case["pair_id"]].append(case)

    pairs = []
    for pair_id in sorted(grouped):
        group = grouped[pair_id]
        preferred = [case for case in group if case["preferred"]]
        mutated = [case for case in group if not case["preferred"]]
        if len(group) != 2 or len(preferred) != 1 or len(mutated) != 1:
            raise ValueError(f"Pair {pair_id} must contain exactly one preferred and one mutated case")
        pairs.append((preferred[0], mutated[0]))
    return pairs


def _summarize(
    pairs: list[tuple[dict[str, Any], dict[str, Any]]],
    scorer: Callable[[dict[str, Any]], float],
) -> dict[str, Any]:
    wins = ties = losses = 0
    separations: list[float] = []
    by_family: dict[str, dict[str, int]] = defaultdict(
        lambda: {"wins": 0, "ties": 0, "losses": 0}
    )

    for preferred, mutated in pairs:
        preferred_score = scorer(preferred)
        mutated_score = scorer(mutated)
        separation = preferred_score - mutated_score
        separations.append(separation)
        family = preferred["family"]
        if separation > 0:
            wins += 1
            by_family[family]["wins"] += 1
        elif separation < 0:
            losses += 1
            by_family[family]["losses"] += 1
        else:
            ties += 1
            by_family[family]["ties"] += 1

    total = wins + ties + losses
    return {
        "pairs": total,
        "wins": wins,
        "ties": ties,
        "losses": losses,
        "strict_win_rate": round(wins / total, 4),
        "tie_adjusted_accuracy": round((wins + 0.5 * ties) / total, 4),
        "mean_separation": round(mean(separations), 4),
        "median_separation": round(median(separations), 4),
        "by_family": dict(sorted(by_family.items())),
    }


def _perturb_case(case: dict[str, Any], rng: random.Random, delta: float) -> dict[str, Any]:
    perturbed = copy.deepcopy(case)

    def perturb(value: float) -> float:
        return _clamp(value + rng.uniform(-delta, delta))

    decision = perturbed["decision_values"]
    decision["T"] = perturb(decision["T"])
    decision["C"] = perturb(decision["C"])
    decision["uncertainty_calibration"] = perturb(decision["uncertainty_calibration"])
    decision["outcome_quality"] = perturb(decision["outcome_quality"])
    for family in (
        "flow_quality",
        "input_entropy",
        "output_entropy",
        "grounding",
        "behavioral_entropy",
        "operational_entropy",
    ):
        for name in decision[family]:
            decision[family][name] = perturb(decision[family][name])

    for family in perturbed["governance_values"]:
        for name in perturbed["governance_values"][family]:
            perturbed["governance_values"][family][name] = perturb(
                perturbed["governance_values"][family][name]
            )
    for name in perturbed["independent_governance_checklist"]:
        perturbed["independent_governance_checklist"][name] = perturb(
            perturbed["independent_governance_checklist"][name]
        )
    return perturbed


def sensitivity_analysis(
    cases: list[dict[str, Any]],
    *,
    trials: int = 100,
    perturbation: float = 0.10,
    seed: int = DEFAULT_SENSITIVITY_SEED,
) -> dict[str, Any]:
    pairs = _pairs(cases)
    per_model: dict[str, list[float]] = {model: [] for model in MODEL_NAMES}

    for pair_index, (preferred, mutated) in enumerate(pairs):
        wins = {model: 0 for model in MODEL_NAMES}
        for trial in range(trials):
            rng = random.Random(seed + pair_index * 100000 + trial)
            p = _perturb_case(preferred, rng, perturbation)
            m = _perturb_case(mutated, rng, perturbation)
            for model in MODEL_NAMES:
                if score_case(p, model) > score_case(m, model):
                    wins[model] += 1
        for model in MODEL_NAMES:
            per_model[model].append(wins[model] / trials)

    return {
        "trials_per_pair": trials,
        "perturbation": perturbation,
        "seed": seed,
        "models": {
            model: {
                "mean_pair_preference_probability": round(mean(values), 4),
                "median_pair_preference_probability": round(median(values), 4),
                "minimum_pair_preference_probability": round(min(values), 4),
            }
            for model, values in per_model.items()
        },
    }


def _run_split(cases: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = _pairs(cases)
    return {
        model: _summarize(pairs, lambda case, name=model: score_case(case, name))
        for model in MODEL_NAMES
    }


def run_experiment(
    cases: list[dict[str, Any]] | None = None,
    *,
    sensitivity_trials: int = 100,
    perturbation: float = 0.10,
    sensitivity_seed: int = DEFAULT_SENSITIVITY_SEED,
) -> dict[str, Any]:
    materialized = cases if cases is not None else generate_cases()
    actual_hash = dataset_sha256(materialized)
    if cases is None and actual_hash != EXPECTED_DATASET_SHA256:
        raise ValueError(
            f"Canonical benchmark hash mismatch: expected={EXPECTED_DATASET_SHA256}, actual={actual_hash}"
        )

    development = [case for case in materialized if case["split"] == "development"]
    validation = [case for case in materialized if case["split"] == "validation"]
    families = sorted({case["family"] for case in materialized})

    return {
        "runner_version": RUNNER_VERSION,
        "benchmark_id": BENCHMARK_ID,
        "benchmark_sha256": actual_hash,
        "frozen_baseline_sha": FROZEN_BASELINE_SHA,
        "parent_research_sha": PARENT_RESEARCH_SHA,
        "evidence_status": "controlled_synthetic_internal",
        "case_count": len(materialized),
        "pair_count": len(_pairs(materialized)),
        "family_count": len(families),
        "families": families,
        "split_counts": {
            "development": len(development),
            "validation": len(validation),
        },
        "models": list(MODEL_NAMES),
        "results": {
            "all": _run_split(materialized),
            "development": _run_split(development),
            "validation": _run_split(validation),
        },
        "sensitivity": sensitivity_analysis(
            materialized,
            trials=sensitivity_trials,
            perturbation=perturbation,
            seed=sensitivity_seed,
        ),
        "limitations": [
            "Cases and labels are synthetic and internally constructed.",
            "Black Hat USA 2026 informed the failure taxonomy but no case reproduces or labels the incident itself.",
            "The benchmark deliberately holds v2 task-flow observations constant inside each pair to test whether governance dimensions add information beyond cognitive/task coherence.",
            "The candidate multiplicative and linear formulations are hypotheses, not accepted EFGM theory.",
            "No external holdout or independently authored labels are included in this benchmark version.",
        ],
    }
