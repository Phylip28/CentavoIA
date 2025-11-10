from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DATABASE_URL: PostgresDsn

    ANT_SPENDING_THRESHOLD: float = 50.0
    PEAK_SPENDING_THRESHOLD: float = 150.0
    RECURRENCE_DAY_TOLERANCE: int = 3
    RECURRENCE_AMOUNT_TOLERANCE: float = 0.10


settings = Settings() # type: ignore [call-arg]
