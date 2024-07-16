import logging


class BaseConfig:
    DEBUG = True
    CONFIG_LEVEL = logging.DEBUG 
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    DEBUG = False
    CONFIG_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/production.db"


class ConfigSelector:
    @staticmethod
    def get_config(level: int) -> BaseConfig:
        if level == logging.DEBUG:
            return DevConfig()
        elif level == logging.INFO:
            return ProdConfig()
        raise NotImplementedError()