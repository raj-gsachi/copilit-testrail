from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TESTRAIL_BASE_URL: str | None = None
    TESTRAIL_USER: str | None = None
    TESTRAIL_API_KEY: str | None = None

    # GitHub Models / LLM
    GITHUB_MODELS_BASE_URL: str = "https://models.github.ai/v1"
    GITHUB_MODELS_API_KEY: str | None = None
    LLM_MODEL_NAME: str = "gpt-4o-mini"
    LLM_MAX_BATCH_SIZE: int = 10

    # Analysis
    PROJECT_ID: int = 1
    SUITE_IDS: list[int] = [1]
    ANALYSIS_MODE: str = "llm"  # reserved for future "rule"

    class Config:
        env_file = ".env"


settings = Settings()
