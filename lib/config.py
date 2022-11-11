"""Configuration"""
import toml

class Config(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Load TOML configuration file"""
        self.data = toml.load("./config.toml")

    def __getattr__(self, key):
        """Returns configuration value"""
        return self.data.get(key)