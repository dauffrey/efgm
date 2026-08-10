from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .benchmark_v0_2 import BENCHMARK_ID, validate_expected_dataset, write_jsonl
from .experiment_runner_v0_2 import MODEL_NAMES, run_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the experimental EFGM v0.3 agent-governance comparison."
    )
    parser.add_argument(
        "--sensitivity-trials",
        type=int,
        default=100,
        help="Perturbation trials per pair. Defaults to 100.",
    )
    parser.add_argument(
        "--perturbation",
        type=float,
        default=0.10,
        help="Uniform +/- perturbation applied to normalized observations.",
    )
    parser.add_argument(
        "--sensitivity-seed",
        type=int,
        default=20260808,
        help="Deterministic sensitivity seed.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format.",
    )
    parser.add_argument("--output", help="Optional output file; otherwise prints to stdout.")
    parser.add_argument(
        "--materialize-dataset",
        help="Optional path to write the canonical 132-case benchmark as JSONL.",
    )
    return parser


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {BENCHMARK_ID} experiment",
        "",
        "**Status: experimental EFGM v0.3 candidate; not an accepted EFGM formula.**",
        "",
        f"Frozen v0.2 baseline: `{result['frozen_baseline_sha']}`",
        f"Parent research head: `{result['parent_research_sha']}`",
        f"Benchmark SHA-256: `{result['benchmark_sha256']}`",
        (
            f"Cases: **{result['case_count']}** | Pairs: **{result['pair_count']}** | "
            f"Families: **{result['family_count']}**"
        ),
        "",
        "## Overall paired ranking",
        "",
        "| Model | Wins | Ties | Losses | Tie-adjusted accuracy | Mean separation |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for model in MODEL_NAMES:
        metrics = result["results"]["all"][model]
        lines.append(
            f"| {model} | {metrics['wins']} | {metrics['ties']} | {metrics['losses']} | "
            f"{metrics['tie_adjusted_accuracy']:.4f} | {metrics['mean_separation']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation guardrail",
            "",
            "The v0.2 task-flow observations are held constant inside each preferred/mutated pair.",
            "Any added discrimination therefore comes from the experimental governance dimensions, not from changing cognitive/task coherence.",
            "",
            "## Sensitivity",
            "",
            "| Model | Mean preference probability | Median | Minimum |",
            "|---|---:|---:|---:|",
        ]
    )
    for model in MODEL_NAMES:
        metrics = result["sensitivity"]["models"][model]
        lines.append(
            f"| {model} | {metrics['mean_pair_preference_probability']:.4f} | "
            f"{metrics['median_pair_preference_probability']:.4f} | "
            f"{metrics['minimum_pair_preference_probability']:.4f} |"
        )

    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(
        [
            "",
            "Black Hat USA 2026 is treated as empirical inspiration only, not benchmark ground truth.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    validate_expected_dataset()
    if args.materialize_dataset:
        write_jsonl(args.materialize_dataset)

    result = run_experiment(
        sensitivity_trials=args.sensitivity_trials,
        perturbation=args.perturbation,
        sensitivity_seed=args.sensitivity_seed,
    )
    output = (
        render_markdown(result)
        if args.format == "markdown"
        else json.dumps(result, indent=2, sort_keys=True)
    )

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
