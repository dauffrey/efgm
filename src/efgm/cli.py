from __future__ import annotations

import argparse
import json
from pathlib import Path

from .schemas import EFGMInput
from .scoring import score_efgm


def main() -> None:
    parser = argparse.ArgumentParser(description="Score an EFGM input JSON file.")
    parser.add_argument("input", help="Path to EFGM input JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))

    model_input = EFGMInput.model_validate(payload)
    result = score_efgm(model_input)

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()
