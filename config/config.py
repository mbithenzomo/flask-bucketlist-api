import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Default configurations """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")


class DevelopmentConfig(Config):
    """ Development configurations """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "bucketlist.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "p9Bv<3Eid9%$i01"


class TestingConfig(Config):
    """ Test configurations """

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(basedir, "test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """ Production configurations """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///models/bucketlist.db"

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
