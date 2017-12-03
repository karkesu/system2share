class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
	SQLALCHEMY_DATABASE_URI = 'postgres://postgres:k96sftvy@localhost/279akz'

class Dev(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
    SQLALCHEMY_DATABASE_URI = 'postgres://localhost/postgres'