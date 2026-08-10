from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .benchmark_v0_1 import BENCHMARK_ID, validate_expected_dataset, write_jsonl
from .experiment_runner import MODEL_NAMES, run_experiment


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run reproducible EFGM comparison experiments.")
    parser.add_argument(
        "--benchmark",
        choices=["v0.1"],
        default="v0.1",
        help="Built-in benchmark to run. Defaults to EFGM Benchmark v0.1.",
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
        help="Uniform +/- perturbation applied to normalized observations. Defaults to 0.10.",
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
        help="Optional path to write the canonical 144-case benchmark as JSONL before running.",
    )
    return parser


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# {BENCHMARK_ID} experiment",
        "",
        f"Frozen baseline: `{result['frozen_baseline_sha']}`",
        f"Benchmark SHA-256: `{result['benchmark_sha256']}`",
        f"Cases: **{result['case_count']}** | Pairs: **{result['pair_count']}** | Families: **{result['family_count']}**",
        f"Development cases: **{result['split_counts']['development']}** | Validation cases: **{result['split_counts']['validation']}**",
        "",
        "## Overall paired ranking",
        "",
        "| Model | Wins | Ties | Losses | Strict win rate | Tie-adjusted accuracy | Mean separation |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for model in MODEL_NAMES:
        metrics = result["results"]["all"][model]
        lines.append(
            f"| {model} | {metrics['wins']} | {metrics['ties']} | {metrics['losses']} | "
            f"{metrics['strict_win_rate']:.4f} | {metrics['tie_adjusted_accuracy']:.4f} | "
            f"{metrics['mean_separation']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Validation split",
            "",
            "| Model | Wins | Ties | Losses | Strict win rate | Tie-adjusted accuracy |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for model in MODEL_NAMES:
        metrics = result["results"]["validation"][model]
        lines.append(
            f"| {model} | {metrics['wins']} | {metrics['ties']} | {metrics['losses']} | "
            f"{metrics['strict_win_rate']:.4f} | {metrics['tie_adjusted_accuracy']:.4f} |"
        )

    sensitivity = result["sensitivity"]
    lines.extend(
        [
            "",
            f"## Sensitivity (+/- {sensitivity['perturbation']:.2f}, {sensitivity['trials_per_pair']} trials/pair)",
            "",
            "| Model | Mean preference probability | Median | Minimum | Pairs >= .95 | Pairs >= .80 |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for model in MODEL_NAMES:
        metrics = sensitivity["models"][model]
        lines.append(
            f"| {model} | {metrics['mean_pair_preference_probability']:.4f} | "
            f"{metrics['median_pair_preference_probability']:.4f} | "
            f"{metrics['minimum_pair_preference_probability']:.4f} | "
            f"{metrics['pairs_at_or_above_0_95']} | {metrics['pairs_at_or_above_0_80']} |"
        )

    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in result["limitations"])
    lines.extend(
        [
            "",
            "This is controlled synthetic internal evidence, not independent external validation.",
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
