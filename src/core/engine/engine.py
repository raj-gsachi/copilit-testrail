from typing import List
from core.models.schemas import RawTestCase, AnalysisResult
from services.llm.client import LLMClient
from config.settings import settings


def run_analysis(cases: List[RawTestCase]) -> List[AnalysisResult]:
    client = LLMClient()
    results: List[AnalysisResult] = []
    batch_size = settings.LLM_MAX_BATCH_SIZE
    for i in range(0, len(cases), batch_size):
        batch = cases[i : i + batch_size]
        batch_results = client.analyze_batch(batch)
        results.extend(batch_results)
    return results
