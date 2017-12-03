class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
	SQLALCHEMY_DATABASE_URI = 'postgres://postgres:k96sftvy/279akz'

class Dev(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'