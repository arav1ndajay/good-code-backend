from pydantic import BaseSettings


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    primary_key: str
    backend_url: str
    frontend_url: str
    docusign_client_id: str
    docusign_client_secret: str

    class Config:
        env_file = ".env"


settings = Settings()