"""
Config for the project
"""

from os import environ

DEFAULT_DB_URL = "sqlite:///./sql_app.db"
DEFAULT_LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_LOG_FILE = "wenet_realtime.log"
DEFAULT_KEEP_OLD_RECORDS = True


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
