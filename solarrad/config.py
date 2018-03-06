"""
These configuration variables can be modified to target a different database
"""

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "database": "solarrad",
    "user": "solar",
    "password": "solar",
    "raise_on_warnings": True
}


def get_config():
    global config
    return config
