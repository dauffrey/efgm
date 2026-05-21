from __future__ import annotations

import argparse
import json
from pathlib import Path

from .reports import render_markdown_report
from .schemas import EFGMInput
from .scoring import score_efgm


def main() -> None:
    parser = argparse.ArgumentParser(description="Score an EFGM input JSON file.")
    parser.add_argument("input", help="Path to EFGM input JSON")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format. Defaults to json.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to write the output. If omitted, output is printed to stdout.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))

    model_input = EFGMInput.model_validate(payload)
    result = score_efgm(model_input)

    if args.format == "markdown":
        output_text = render_markdown_report(result)
    else:
        output_text = json.dumps(result.model_dump(), indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
    else:
        print(output_text)


if __name__ == "__main__":
    main()