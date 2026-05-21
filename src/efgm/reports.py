from __future__ import annotations

from .schemas import EFGMResult


def render_markdown_report(result: EFGMResult) -> str:
    """Render an EFGM scoring result as a Markdown governance report."""

    entropy_drivers = (
        "\n".join(f"- {driver}" for driver in result.entropy_drivers)
        if result.entropy_drivers
        else "- None above threshold"
    )

    lines = [
        "# EFGM Coherent Flow Report",
        "",
        "## Task",
        "",
        f"`{result.task_id}`",
        "",
        "## Score Summary",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| T | {result.T:.4f} |",
        f"| E | {result.E:.4f} |",
        f"| Fq | {result.Fq:.4f} |",
        f"| e | {result.e:.4f} |",
        f"| F | {result.F:.4f} |",
        "",
        "## Classification",
        "",
        f"**{result.classification}**",
        "",
        "## Entropy Drivers",
        "",
        entropy_drivers,
        "",
        "## Recommended Action",
        "",
        result.recommended_action,
        "",
        "## Formula",
        "",
        "```text",
        "F = (T × E × Fq) / (1 + e)",
        "```",
        "",
        "## Interpretation",
        "",
        (
            "The coherent flow score represents the degree to which the evaluated "
            "system, workflow, or reasoning chain is maintaining useful alignment "
            "while entropy accumulates."
        ),
        "",
        (
            "A lower score indicates that verification, context repair, or governance "
            "intervention may be required before relying on the result."
        ),
        "",
    ]

    return "\n".join(lines)