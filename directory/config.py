import os


class Base(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERET_KEY = os.getenv('SECRET_KEY')


class Development(Base):
    pass


class Production(Base):
    pass
