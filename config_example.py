import os
class DeploymentConfig(object):
	DATABASE_URI = "postgresql://username:password@localhost:5432/merrily"
	DEBUG = False
	SECRET_KEY = os.environ.get("MERRILY_SECRET_KEY", os.urandom(12))

class DevelopmentConfig(object):
	DATABASE_URI = "postgresql://username:password@localhost:5432/merrily"
	DEBUG = True
	SECRET_KEY = os.environ.get("MERRILY_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
	DATABASE_URI = "postgresql://username:password@localhost:5432/merrily-test"
	DEBUG = True
	SECRET_KEY = os.environ.get("MERRILY_SECRET_KEY", os.urandom(12))
