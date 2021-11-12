from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """Main settings."""

    # Bots credentials
    USERNAME: str
    PASSWORD: str
    SERVER: str

    # YouTrack credentials
    DOMAIN: str
    TOKEN: str

    class Config:  # noqa: WPS431
        env_file = ".env"
