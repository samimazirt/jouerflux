import os
import logging
import logging.config

class Config:
    SECRET_KEY = 'fortinet'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jouerflux.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def setup_logging():
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            handlers=[
                                logging.FileHandler("app.log"),
                                logging.StreamHandler()
                            ])

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jouerflux.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONF_NAME = "development"

class LocalConfig(DevelopmentConfig):
    CONF_NAME = "local"
    SQLALCHEMY_DATABASE_URI = "sqlite:///jouerflux.db"
    ENABLE_RSA_PRIME_CALL = True

config_by_name = dict(
    local=LocalConfig,
    development=DevelopmentConfig
)
