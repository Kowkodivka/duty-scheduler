from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    BOT_TOKEN: str

    TIME_ZONE: str = "Asia/Novokuznetsk"
    DATABASE_PATH: str = "duties.db"


settings = Settings()
