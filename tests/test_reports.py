from efgm.reports import render_markdown_report
from efgm.schemas import EFGMResult


def test_render_markdown_report_contains_key_sections():
    result = EFGMResult(
        task_id="report-test",
        T=0.8,
        E=0.9,
        Fq=0.7125,
        e=0.265,
        F=0.4055,
        classification="Degraded but usable",
        recommended_action="Verify assumptions and reduce entropy before relying on the result.",
        entropy_drivers=["Uncertainty variance"],
    )

    report = render_markdown_report(result)

    assert "# EFGM Coherent Flow Report" in report
    assert "`report-test`" in report
    assert "| F | 0.4055 |" in report
    assert "**Degraded but usable**" in report
    assert "- Uncertainty variance" in report
    assert "Verify assumptions" in report