import os
import json
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    """
    Settings class for this application.
    Utilizes the BaseSettings from pydantic for environment variables.
    """

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    """Function to get and cache settings.
    The settings are cached to avoid repeated disk I/O."""
    environment = os.getenv("ENVIRONMENT", "local")
    
    if environment == "local":
        settings_file = ".env"
    elif environment == "dev":
        settings_file = ".env.dev"
    elif environment == "prod":
        settings_file = ".env.prod"
    else:
        raise ValueError(f"Invalid environment: {environment}")

    # Load settings from the respective .env file
    return Settings(_env_file=settings_file)  # type: ignore
