from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "KidsAI"
    debug: bool = False

    database_url: str = "postgresql+asyncpg://kidsai:kidsai@localhost:5432/kidsai"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret: str = "CHANGE-ME-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "kidsai"

    # AI providers
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    dashscope_api_key: str = ""
    volcano_access_key: str = ""
    volcano_secret_key: str = ""
    claude_api_key: str = ""

    # AI provider selection
    llm_provider: str = "deepseek"  # deepseek | claude | qwen
    stt_provider: str = "volcano"  # volcano | whisper
    tts_provider: str = "volcano"  # volcano | minimax | edge

    model_config = {"env_prefix": "KIDSAI_", "env_file": ".env"}


settings = Settings()
