from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    RISK_FREE_RATE: float = 0.02
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )