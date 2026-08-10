from __future__ import annotations

import copy
import math
import random
from collections import defaultdict
from statistics import mean, median
from typing import Any, Callable

from .baselines import (
    grounding_calibration_baseline,
    independent_checklist_baseline,
    weighted_linear_baseline,
)
from .benchmark_v0_1 import BENCHMARK_ID, EXPECTED_DATASET_SHA256, dataset_sha256, generate_cases
from .schemas import EFGMInput
from .schemas_v2 import EFGMDecisionInput
from .scoring import score_efgm
from .scoring_v2 import score_decision_efgm

RUNNER_VERSION = "0.1.0"
FROZEN_BASELINE_SHA = "b717f611a0d09bd8e52bc1b0be5ee178eecacf25"
DEFAULT_SENSITIVITY_SEED = 20260808
MODEL_NAMES = ("v1", "v2", "g_plus_u", "linear", "independent_checklist")


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, round(float(value), 4)))


def _observation(case: dict[str, Any], path: str, value: float) -> dict[str, Any]:
    return {
        "value": value,
        "status": "inferred",
        "rationale": (
            f"Controlled synthetic benchmark assignment for family={case['family']}, "
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
    values = case["values"]
    payload = {
        "task_id": case["case_id"],
        "T": _observation(case, "T", values["T"]),
        "C": _observation(case, "C", values["C"]),
        "flow_quality": _observation_family(case, "flow_quality", values["flow_quality"]),
        "input_entropy": _observation_family(case, "input_entropy", values["input_entropy"]),
        "output_entropy": _observation_family(case, "output_entropy", values["output_entropy"]),
        "grounding": _observation_family(case, "grounding", values["grounding"]),
        "uncertainty_calibration": _observation(
            case,
            "uncertainty_calibration",
            values["uncertainty_calibration"],
        ),
        "behavioral_entropy": _observation_family(
            case,
            "behavioral_entropy",
            values["behavioral_entropy"],
        ),
        "operational_entropy": _observation_family(
            case,
            "operational_entropy",
            values["operational_entropy"],
        ),
        "outcome_quality": _observation(case, "outcome_quality", values["outcome_quality"]),
        "notes": [
            f"benchmark={BENCHMARK_ID}",
            f"pair={case['pair_id']}",
            f"family={case['family']}",
            f"split={case['split']}",
            f"label_source={case['label_source']}",
        ],
    }
    return EFGMDecisionInput.model_validate(payload)


def case_to_v1_input(case: dict[str, Any]) -> EFGMInput:
    """Project v2 benchmark observations into the legacy v1 input space.

    V1 has one entropy vector and cannot represent input/output separation, grounding,
    calibration, behavioral entropy, or operational entropy. The projection therefore
    uses transparent nearest-neighbor mappings rather than inventing new v1 constructs.
    This limitation is part of the comparison and must be retained in reports.
    """
    values = case["values"]
    input_entropy = values["input_entropy"]
    output_entropy = values["output_entropy"]
    entropy = {
        "contradiction_density": round(
            (input_entropy["input_contradiction"] + output_entropy["output_contradiction"]) / 2,
            4,
        ),
        "uncertainty_variance": round(
            (input_entropy["input_ambiguity"] + output_entropy["uncertainty_mismatch"]) / 2,
            4,
        ),
        "memory_fragmentation": round(
            (input_entropy["missing_context"] + output_entropy["context_decay"]) / 2,
            4,
        ),
        "recursion_instability": output_entropy["reasoning_instability"],
        "context_decay": output_entropy["context_decay"],
    }
    return EFGMInput.model_validate(
        {
            "task_id": case["case_id"],
            "T": values["T"],
            "E": values["C"],
            "entropy": entropy,
            "flow_quality": values["flow_quality"],
            "notes": [
                f"Projected from {BENCHMARK_ID} v2 fixture into legacy v1 space.",
                "V1 cannot directly represent G, U, Be, Oe, or separate Ei/Eo.",
            ],
        }
    )


def score_case(case: dict[str, Any], model_name: str) -> float:
    if model_name not in MODEL_NAMES:
        raise ValueError(f"Unknown comparison model {model_name!r}; expected one of {MODEL_NAMES}")

    if model_name == "v1":
        return score_efgm(case_to_v1_input(case)).F

    v2_input = case_to_v2_input(case)
    if model_name == "v2":
        return score_decision_efgm(v2_input, require_provenance=True).DQ
    if model_name == "g_plus_u":
        return grounding_calibration_baseline(v2_input)
    if model_name == "linear":
        return weighted_linear_baseline(v2_input)
    return independent_checklist_baseline(case["independent_checklist"])


def _pairs(cases: list[dict[str, Any]]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        grouped[case["pair_id"]].append(case)

    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pair_id in sorted(grouped):
        group = grouped[pair_id]
        if len(group) != 2:
            raise ValueError(f"Pair {pair_id} must contain exactly two cases; got {len(group)}")
        preferred = [case for case in group if case["preferred"]]
        mutated = [case for case in group if not case["preferred"]]
        if len(preferred) != 1 or len(mutated) != 1:
            raise ValueError(f"Pair {pair_id} must contain one preferred and one mutated case")
        pairs.append((preferred[0], mutated[0]))
    return pairs


def _wilson_interval(successes: int, total: int, z: float = 1.96) -> list[float]:
    if total <= 0:
        return [0.0, 0.0]
    p = successes / total
    denominator = 1 + (z * z) / total
    center = (p + (z * z) / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt((p * (1 - p) / total) + (z * z) / (4 * total * total))
        / denominator
    )
    return [round(max(0.0, center - margin), 4), round(min(1.0, center + margin), 4)]


def _summarize_model(
    pairs: list[tuple[dict[str, Any], dict[str, Any]]],
    scorer: Callable[[dict[str, Any]], float],
) -> dict[str, Any]:
    wins = ties = losses = 0
    preferred_scores: list[float] = []
    mutated_scores: list[float] = []
    separations: list[float] = []
    by_family: dict[str, dict[str, int]] = defaultdict(lambda: {"wins": 0, "ties": 0, "losses": 0})

    for preferred, mutated in pairs:
        preferred_score = scorer(preferred)
        mutated_score = scorer(mutated)
        preferred_scores.append(preferred_score)
        mutated_scores.append(mutated_score)
        separations.append(preferred_score - mutated_score)
        family = preferred["family"]
        if preferred_score > mutated_score:
            wins += 1
            by_family[family]["wins"] += 1
        elif preferred_score < mutated_score:
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
        "strict_win_rate_95pct_wilson": _wilson_interval(wins, total),
        "tie_adjusted_accuracy": round((wins + 0.5 * ties) / total, 4),
        "mean_preferred_score": round(mean(preferred_scores), 4),
        "mean_mutated_score": round(mean(mutated_scores), 4),
        "mean_separation": round(mean(separations), 4),
        "median_separation": round(median(separations), 4),
        "by_family": dict(sorted(by_family.items())),
    }


def _perturb_case(case: dict[str, Any], rng: random.Random, delta: float) -> dict[str, Any]:
    perturbed = copy.deepcopy(case)

    def perturb(value: float) -> float:
        return _clamp(value + rng.uniform(-delta, delta))

    values = perturbed["values"]
    values["T"] = perturb(values["T"])
    values["C"] = perturb(values["C"])
    values["uncertainty_calibration"] = perturb(values["uncertainty_calibration"])
    values["outcome_quality"] = perturb(values["outcome_quality"])
    for family in (
        "flow_quality",
        "input_entropy",
        "output_entropy",
        "grounding",
        "behavioral_entropy",
        "operational_entropy",
    ):
        for name in values[family]:
            values[family][name] = perturb(values[family][name])
    for name in perturbed["independent_checklist"]:
        perturbed["independent_checklist"][name] = perturb(perturbed["independent_checklist"][name])
    return perturbed


def sensitivity_analysis(
    cases: list[dict[str, Any]],
    *,
    trials: int = 100,
    perturbation: float = 0.10,
    seed: int = DEFAULT_SENSITIVITY_SEED,
) -> dict[str, Any]:
    if trials <= 0:
        raise ValueError("Sensitivity trials must be greater than zero")
    if not 0 <= perturbation <= 1:
        raise ValueError("Perturbation must be between 0 and 1")

    pairs = _pairs(cases)
    per_model_probabilities: dict[str, list[float]] = {model: [] for model in MODEL_NAMES}

    for pair_index, (preferred, mutated) in enumerate(pairs):
        wins = {model: 0 for model in MODEL_NAMES}
        for trial in range(trials):
            rng = random.Random(seed + pair_index * 100000 + trial)
            preferred_perturbed = _perturb_case(preferred, rng, perturbation)
            mutated_perturbed = _perturb_case(mutated, rng, perturbation)
            for model in MODEL_NAMES:
                if score_case(preferred_perturbed, model) > score_case(mutated_perturbed, model):
                    wins[model] += 1
        for model in MODEL_NAMES:
            per_model_probabilities[model].append(wins[model] / trials)

    return {
        "trials_per_pair": trials,
        "perturbation": perturbation,
        "seed": seed,
        "models": {
            model: {
                "mean_pair_preference_probability": round(mean(probabilities), 4),
                "median_pair_preference_probability": round(median(probabilities), 4),
                "minimum_pair_preference_probability": round(min(probabilities), 4),
                "pairs_at_or_above_0_95": sum(value >= 0.95 for value in probabilities),
                "pairs_at_or_above_0_80": sum(value >= 0.80 for value in probabilities),
            }
            for model, probabilities in per_model_probabilities.items()
        },
    }


def _run_split(cases: list[dict[str, Any]]) -> dict[str, Any]:
    pairs = _pairs(cases)
    return {
        model: _summarize_model(pairs, lambda case, name=model: score_case(case, name))
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
            "Cases and labels are synthetic and internally constructed rather than independently collected.",
            "The benchmark families were chosen from EFGM's intended construct space, which can favor EFGM-aligned models.",
            "The independent checklist is structurally independent of EFGM composites but was authored by the same benchmark generator.",
            "V1 requires a documented lossy projection because it cannot represent several v2 constructs.",
            "These results test construct responsiveness and robustness; they do not establish external predictive validity.",
        ],
    }
