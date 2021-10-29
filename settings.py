from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Main settings."""

    # Bots credentials
    USERNAME: str
    PASSWORD: str
    SERVER: str

    class Config:  # noqa: WPS431
        env_file = ".env"
