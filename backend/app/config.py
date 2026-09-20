from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    nebius_api_key: str = ""
    nebius_model: str = ""
    nebius_base_url: str = "https://api.tokenfactory.nebius.com/v1/"
    tavily_api_key: str = ""
    enable_live_research: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
