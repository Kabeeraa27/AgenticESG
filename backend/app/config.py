from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field("Agentic ESG Compliance Copilot", validation_alias="APP_NAME")
    env: str = Field("local", validation_alias="ENVIRONMENT")
    api_prefix: str = "/api"
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"], validation_alias="CORS_ALLOW_ORIGINS")

    database_url: str | None = Field(None, validation_alias="DATABASE_URL")

    postgres_host: str = Field("localhost", validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(5432, validation_alias="POSTGRES_PORT")
    postgres_db: str = Field("agenticesg", validation_alias="POSTGRES_DB")
    postgres_user: str = Field("agentic", validation_alias="POSTGRES_USER")
    postgres_password: str = Field("agentic", validation_alias="POSTGRES_PASSWORD")

    faiss_index_path: str = Field("./data/vector_store/faiss.index", validation_alias="FAISS_INDEX_PATH")

    model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", validation_alias="MODEL_NAME")
    llm_model: str = Field("gpt-4.1", validation_alias="LLM_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
