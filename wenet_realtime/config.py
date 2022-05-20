"""
Config for the project
"""

from os import environ

DEFAULT_DB_URL = "sqlite:///./sql_app.db"
DEFAULT_LOG_FILE = "wenet_realtime.log"
DEFAULT_KEEP_OLD_RECORDS = True
DEFAULT_WENET_SENTRY_KEY = ""
DEFAULT_ENV = "dev"
DEFAULT_LOGGER_FORMAT = "[{}] %(asctime)s - %(name)s - %(levelname)s - %(message)s"

def _update_parameters_from_env():
    """update the config values from env"""
    for k, v in globals().items():
        if k.startswith("DEFAULT_"):
            if k in environ:
                new_v = type(v)(environ[k])
                print(
                    "Parameters {} was updated from {} to {} by environment override".format(
                        k, v, new_v
                    )
                )
                globals()[k] = new_v

def _update_fill_env():  # pragma: no cover
    envs = ["DEFAULT_LOGGER_FORMAT"]
    for env in envs:
        globals()[env] = globals()[env].format(DEFAULT_ENV)

_update_parameters_from_env()
_update_fill_env()