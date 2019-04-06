import os


class Config(object):
    """
    Parent configuration class
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """
    Configuration for Dev
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/.usrmgrdev.db'


class TestingConfig(Config):
    """
    Configuration for testing, with a different db
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/.usrmgrtest.db'
    DEBUG = True


class StagingConfig(Config):
    """
    Staging configuration
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/.usrmgrstaging.db'


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/.usrmgrprod.db'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
