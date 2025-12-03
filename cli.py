import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR / "src"))

from services.testrail.service import fetch_cases
from core.engine.engine import run_analysis
from utils.report_generator import generate_excel_report, generate_html_report


def main() -> None:
    cases = fetch_cases()
    if not cases:
        print("No test cases found. Ensure data/sample-export.csv exists.")
        return
    results = run_analysis(cases)
    generate_excel_report(results, "reports/analysis.xlsx")
    generate_html_report(results, "reports/analysis.html")
    print("Reports generated in ./reports")


if __name__ == "__main__":
    main()
