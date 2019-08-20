import os


# base dir path
basedir = os.path.abspath(os.path.dirname(__file__))


# base config class
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '48d39422ff504cec83fd2a98ac05ad5c'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


# config class for development
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'databases/abovo_dev.db')


# config class for testing
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'databases/abovo_test.db')


# config class for production
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
                              'postgresql://abovo:abovo123@soft21.pl:18954/abovo'


# map config name to proper class
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
