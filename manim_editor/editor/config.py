__all__ = ["set_config", "get_config"]


def set_config(new_config):
    global config
    config = new_config


def get_config():
    """Return config object."""
    global config
    return config
