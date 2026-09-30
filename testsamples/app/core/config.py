import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AZURE_SUBSCRIPTION_ID: str = "7deb6dec-3ee1-416d-b35f-f1b2bce29a90"
    # JWT_SECRET_KEY: str = "70bc8db669fbb7c9dcf04ef051ef9b265d6c5df5e5ffae82d1c6df3d1c15f922"
    # JWT_ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()