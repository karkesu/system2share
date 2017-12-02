class Config(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class Production(Config):
	# TO CHANGE
	SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class Dev(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'