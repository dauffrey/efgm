from __future__ import annotations

from .schemas import EFGMResult
from .schemas_v2 import EFGMDecisionResult


def _bullets(items: list[str], empty: str) -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {empty}"


def render_markdown_report(result: EFGMResult) -> str:
    return "\n".join([
        "# EFGM v1 Coherent Flow Report", "", "## Task", "", f"`{result.task_id}`", "",
        "## Score Summary", "", "| Metric | Value |", "|---|---:|",
        f"| T | {result.T:.4f} |", f"| E | {result.E:.4f} |", f"| Fq | {result.Fq:.4f} |",
        f"| e | {result.e:.4f} |", f"| F | {result.F:.4f} |", "", "## Classification", "",
        f"**{result.classification}**", "", "## Entropy Drivers", "",
        _bullets(result.entropy_drivers, "None above threshold"), "", "## Recommended Action", "",
        result.recommended_action, "", "## Formula", "", "```text",
        "Q = (T × E × Fq)^(1/3)", "F = Q / (1 + e)", "```", "",
    ])


def render_decision_markdown_report(result: EFGMDecisionResult) -> str:
    sections = [
        ("Input entropy drivers", result.input_entropy_drivers, "None above threshold"),
        ("Output entropy drivers", result.output_entropy_drivers, "None above threshold"),
        ("Grounding gaps", result.grounding_drivers, "None below threshold"),
        ("Behavioral entropy drivers", result.behavioral_entropy_drivers, "None above threshold"),
        ("Operational entropy drivers", result.operational_entropy_drivers, "None above threshold"),
    ]
    lines = [
        "# EFGM v2 Decision Integrity Report", "", "## Task", "", f"`{result.task_id}`", "",
        "## Reproducibility", "",
        f"Scoring configuration: `{result.config_id}`  ",
        f"Configuration SHA-256: `{result.config_sha256}`  ",
        f"Input SHA-256: `{result.input_sha256}`  ",
        f"Research provenance complete: `{'yes' if result.provenance_complete else 'no'}`", "",
    ]
    if result.provenance_issues:
        lines.extend(["### Provenance issues", "", _bullets(result.provenance_issues, "None"), ""])

    lines.extend([
        "## Score Summary", "", "| Metric | Value |", "|---|---:|",
        f"| T | {result.T:.4f} |", f"| C | {result.C:.4f} |", f"| Fq | {result.Fq:.4f} |",
        f"| G | {result.G:.4f} |", f"| U | {result.U:.4f} |", f"| Ei | {result.Ei:.4f} |",
        f"| Eo | {result.Eo:.4f} |", f"| Be | {result.Be:.4f} |", f"| Oe | {result.Oe:.4f} |",
        f"| CRC | {result.CRC:.4f} |", f"| Q | {result.Q:.4f} |", f"| DQ | {result.DQ:.4f} |",
        f"| Outcome confidence | {result.outcome_confidence:.4f} |",
    ])
    if result.OQ is not None:
        lines.extend([f"| OQ | {result.OQ:.4f} |", f"| OD | {result.OD:.4f} |"])
    lines.extend(["", "## Classification", "", f"**{result.classification}**", "", "## Recommended Action", "", result.recommended_action])
    for heading, items, empty in sections:
        lines.extend(["", f"## {heading}", "", _bullets(items, empty)])
    lines.extend([
        "", "## Formula", "", "```text", "Ei = weighted input entropy", "Eo = weighted output entropy",
        "CRC = (Ei - Eo) / max(Ei, ε)", "Q = (T × C × Fq × G × U)^(1/5)",
        "DQ = Q / (1 + Eo + Be + Oe)", "OutcomeConfidence = DQ × (1 - H)", "OD = OQ - DQ", "```", "",
        "CRC is a recovery/amplification ratio and is intentionally not bounded to [-1, 1]. Positive values indicate entropy reduction; negative values indicate entropy amplification.", "",
    ])
    return "\n".join(lines)
