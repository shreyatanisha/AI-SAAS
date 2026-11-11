import os

from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(RuntimeError):
    pass


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigurationError(
            f"Missing required environment variable: {name}"
        )
    return value
