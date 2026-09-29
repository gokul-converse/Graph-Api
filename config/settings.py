import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from azure.identity import ClientSecretCredential
from agent_framework.foundry import FoundryChatClient


load_dotenv()


class Settings(BaseSettings):
    # Azure / Foundry
    # =========================
    foundry_project_endpoint: str
    azure_ai_key: str
    azure_openai_deployment: str
    azure_openai_api_version: str

    azure_client_id: str
    azure_client_secret: str
    azure_tenant_id: str

    tenant_id: str
    client_id:str
    client_secret:str



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # extra="ignore",
    )


settings = Settings()


# =========================
# Foundry Client
# =========================

credential = ClientSecretCredential(
    tenant_id=settings.azure_tenant_id,
    client_id=settings.azure_client_id,
    client_secret=settings.azure_client_secret,
)

client = FoundryChatClient(
    project_endpoint=settings.foundry_project_endpoint,
    model=settings.azure_openai_deployment,
    credential=credential,
)