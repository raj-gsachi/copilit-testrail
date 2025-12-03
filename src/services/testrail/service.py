import csv
from pathlib import Path
from typing import List
from core.models.schemas import RawTestCase

DATA_PATH = Path("data/sample-export.csv")


def fetch_cases() -> List[RawTestCase]:
    cases: List[RawTestCase] = []
    if not DATA_PATH.exists():
        return cases
    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            cases.append(
                RawTestCase(
                    id=int(row["id"]),
                    suite_id=int(row.get("suite_id", 0)),
                    section=row.get("section", ""),
                    title=row.get("title", ""),
                    steps=row.get("steps", ""),
                    expected_result=row.get("expected_result", ""),
                    priority=row.get("priority") or None,
                    type=row.get("type") or None,
                    tags=[t.strip() for t in row.get("tags", "").split(",") if t.strip()],
                )
            )
    return cases
