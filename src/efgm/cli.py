from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .reports import render_decision_markdown_report, render_markdown_report
from .schemas import EFGMInput
from .schemas_v2 import EFGMDecisionInput
from .scoring import score_efgm
from .scoring_v2 import IncompleteAssessmentError, ProvenanceError, score_decision_efgm


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Score an EFGM input JSON file.")
    parser.add_argument("input", help="Path to EFGM input JSON")
    parser.add_argument(
        "--model",
        choices=["v1", "v2"],
        default="v2",
        help="Scoring model. Defaults to v2; use v1 for compatibility inputs.",
    )
    parser.add_argument(
        "--config",
        help="Optional v2 scoring-config JSON path. Omit to use the packaged baseline configuration.",
    )
    parser.add_argument(
        "--require-provenance",
        action="store_true",
        help="Require research-grade rationale, evidence references, and scorer metadata for v2 observations.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format. Defaults to json.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. If omitted, output is printed to stdout.",
    )
    return parser


def score_payload(
    payload: dict,
    model: str,
    config: str | None = None,
    *,
    require_provenance: bool = False,
):
    if model == "v1":
        if config:
            raise ValueError("--config is supported only for the v2 model.")
        if require_provenance:
            raise ValueError("--require-provenance is supported only for the v2 model.")
        return score_efgm(EFGMInput.model_validate(payload))
    return score_decision_efgm(
        EFGMDecisionInput.model_validate(payload),
        config=config,
        require_provenance=require_provenance,
    )


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    try:
        result = score_payload(
            payload,
            args.model,
            args.config,
            require_provenance=args.require_provenance,
        )
    except (IncompleteAssessmentError, ProvenanceError, ValueError) as exc:
        parser.error(str(exc))

    if args.format == "markdown":
        output = (
            render_markdown_report(result)
            if args.model == "v1"
            else render_decision_markdown_report(result)
        )
    else:
        output = json.dumps(result.model_dump(), indent=2)

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
