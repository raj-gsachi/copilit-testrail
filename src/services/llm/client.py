import json
import requests
from typing import List
from core.models.schemas import RawTestCase, AnalysisResult
from config.settings import settings


class LLMClient:
    def __init__(self) -> None:
        if not settings.GITHUB_MODELS_API_KEY:
            raise RuntimeError("GITHUB_MODELS_API_KEY is not set")
        self.base_url = settings.GITHUB_MODELS_BASE_URL.rstrip("/")
        self.api_key = settings.GITHUB_MODELS_API_KEY
        self.model = settings.LLM_MODEL_NAME

    def _build_messages(self, batch: List[RawTestCase]) -> list[dict]:
        system = (
            "You are a Test Automation Architect. For each test case, analyze it and "
            "return structured JSON. For each test case include: "
            "test_case_id, automation_feasibility (Yes|Partial|No), automation_level "
            "(Unit|API|UI|E2E|Other), automation_priority (P1|P2|P3), complexity "
            "(Low|Medium|High), effort_points (1-8), duplicate_group_id (string or null), "
            "duplicate_of_case_id (int or null), redundancy_score (0-1), "
            "suggested_action (Keep|Merge|Archive|Refactor), coverage_notes, architect_notes."
        )
        user_content = {
            "instruction": "Analyze these test cases and return JSON with key 'results' as an array.",
            "schema": "Each item in results must contain the fields listed in the system message.",
            "test_cases": [c.model_dump() for c in batch],
        }
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user_content)},
        ]

    def analyze_batch(self, batch: List[RawTestCase]) -> List[AnalysisResult]:
        messages = self._build_messages(batch)
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        results = parsed["results"]
        return [AnalysisResult(**item) for item in results]
