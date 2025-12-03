from typing import List
from pathlib import Path
from openpyxl import Workbook
from core.models.schemas import AnalysisResult


def generate_excel_report(results: List[AnalysisResult], path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Analysis"
    headers = [
        "TestCaseID", "Automation", "Level", "Priority", "Complexity",
        "Effort", "DupGroup", "DupOf", "Redundancy", "Action",
        "CoverageNotes", "ArchitectNotes",
    ]
    ws.append(headers)
    for r in results:
        ws.append([
            r.test_case_id,
            r.automation_feasibility,
            r.automation_level,
            r.automation_priority,
            r.complexity,
            r.effort_points,
            r.duplicate_group_id,
            r.duplicate_of_case_id,
            r.redundancy_score,
            r.suggested_action,
            r.coverage_notes,
            r.architect_notes,
        ])
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def generate_html_report(results: List[AnalysisResult], path: str) -> None:
    rows_html = ""
    for r in results:
        rows_html += (
            f"<tr><td>{r.test_case_id}</td>"
            f"<td>{r.automation_feasibility}</td>"
            f"<td>{r.automation_level}</td>"
            f"<td>{r.automation_priority}</td>"
            f"<td>{r.complexity}</td>"
            f"<td>{r.effort_points}</td>"
            f"<td>{r.duplicate_group_id or ''}</td>"
            f"<td>{r.duplicate_of_case_id or ''}</td>"
            f"<td>{r.redundancy_score:.2f}</td>"
            f"<td>{r.suggested_action}</td>"
            f"<td>{r.coverage_notes}</td>"
            f"<td>{r.architect_notes}</td></tr>"
        )
    html = f"""
<html><head><title>TestRail Analysis</title></head>
<body>
<h1>TestRail LLM Analysis Report</h1>
<table border="1" cellspacing="0" cellpadding="4">
<tr>
<th>ID</th><th>Automation</th><th>Level</th><th>Priority</th><th>Complexity</th>
<th>Effort</th><th>DupGroup</th><th>DupOf</th><th>Redundancy</th>
<th>Action</th><th>Coverage</th><th>Notes</th>
</tr>
{rows_html}
</table>
</body></html>
"""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(html, encoding="utf-8")
