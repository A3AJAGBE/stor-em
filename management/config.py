import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True