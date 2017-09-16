class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://stephen:thinkful@localhost:5432/merrily"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://stephen:thinkful@localhost:5432/merrily-test"
    DEBUG = True
