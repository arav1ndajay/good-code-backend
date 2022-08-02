from pydantic import BaseSettings


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    host_url: str

    class Config:
        env_file = ".env"


settings = Settings()