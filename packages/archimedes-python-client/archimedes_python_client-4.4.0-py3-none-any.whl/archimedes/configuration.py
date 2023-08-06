import os
import abc
import pandas as pd
import requests

# Global archimedes config
USER_HOME_DIR = os.path.expanduser("~")
ARCHIMEDES_CONF_DIR = os.path.join(USER_HOME_DIR, ".archimedes")


def get_environment():
    env = os.environ.get("ARCHIMEDES_ENVIRONMENT")
    if env is None:
        env = os.environ.get("ENVIRONMENT", "prod")
    return env.strip().lower()


def get_msal_path():
    msal_path = os.path.join(ARCHIMEDES_CONF_DIR, f"msal-{get_environment()}.cache.bin")
    return msal_path


# Local archimedes config
ARCHIMEDES_API_CONFIG_URL = "https://arcl.optimeering.no/config.json"


class ArchimedesConstants:
    DATE_LOW = pd.to_datetime("1900-01-01T00:00:00+00:00")
    DATE_HIGH = pd.to_datetime("2090-01-01T00:00:00+00:00")


class InvalidEnvironmentException(Exception):
    pass


class ApiConfig(abc.ABC):
    def __init__(self, env):
        config_result = requests.get(ARCHIMEDES_API_CONFIG_URL)
        self.config = config_result.json()
        if env not in self.config.keys():
            raise InvalidEnvironmentException(
                f"Invalid environment {env}, "
                f"supported values are {', '.join([str(key) for key in self.config.keys()])}"
            )
        self.environment = env.lower()

    def __getattr__(self, item):
        env_config = self.config[self.environment]
        return env_config[item]


def get_api_config():
    return ApiConfig(get_environment())


def get_api_base_url(api_version: int) -> str:
    return f"{get_api_config().url}/v{api_version}"
