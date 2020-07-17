"""
Config for the project
"""

from os import environ

DEFAULT_DB_URL = "sqlite:///./sql_app.db"


def _update_parameters_from_env():
    """ update the config values from env
    """
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
