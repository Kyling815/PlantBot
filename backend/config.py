"""
Application-wide configuration loaded from environment variables.
"""

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",                     # silently ignore unknown env vars (e.g. NEXT_PUBLIC_*)
        protected_namespaces=("settings_",) # avoids warning for fields starting with "model_"
    )

    # LLM
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # CNN Model paths
    model_path: str = Field(
        default=os.path.join(
            os.path.dirname(__file__), "..", "plant_disease", "plant_disease_98.pth"
        )
    )
    class_names_path: str = Field(
        default=os.path.join(
            os.path.dirname(__file__), "..", "plant_disease", "class_names.json"
        )
    )

    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    debug: bool = True

    # Database
    database_url: str = "sqlite+aiosqlite:///./plantbot.db"


settings = Settings()
