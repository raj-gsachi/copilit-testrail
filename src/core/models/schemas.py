from pydantic import BaseModel
from typing import Literal, Optional, List


class RawTestCase(BaseModel):
    id: int
    suite_id: int
    section: str
    title: str
    steps: str
    expected_result: str
    priority: Optional[str] = None
    type: Optional[str] = None
    tags: List[str] = []


class AnalysisResult(BaseModel):
    test_case_id: int
    automation_feasibility: Literal["Yes", "Partial", "No"]
    automation_level: Literal["Unit", "API", "UI", "E2E", "Other"]
    automation_priority: Literal["P1", "P2", "P3"]
    complexity: Literal["Low", "Medium", "High"]
    effort_points: int
    duplicate_group_id: Optional[str] = None
    duplicate_of_case_id: Optional[int] = None
    redundancy_score: float
    suggested_action: Literal["Keep", "Merge", "Archive", "Refactor"]
    coverage_notes: str
    architect_notes: str
