"""
These configuration variables can be modified to target a different database
"""

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "solar",
    "user": "solar_user",
    "password": "solar_pass",
    "raise_on_warnings": True
}


def get_config():
    global config
    return config