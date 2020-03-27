class Config(object):
	DEBUG = False
	TESTING = False

	HOST_NAME = "ec2-54-246-90-26.eu-west-1.compute.amazonaws.com"
	DB_NAME = "d55v7qh9k51mqu"
	DB_USERNAME = "wisaevtuesximp"
	DB_PASSWORD = "7bd99538dc7ddaae24dd9f0ed6047b4f4c87d2320d6efb7403cedd21c5d5d914"
	DB_PORT = 5432

	SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
	pass


class DevelopmentConfig(Config):
	DEBUG = True

	HOST_NAME = "localhost"
	DB_NAME = "postgres"
	DB_USERNAME = "postgres"
	DB_PASSWORD = "admin"
	# HOST_NAME = "ec2-54-246-90-26.eu-west-1.compute.amazonaws.com"
	# DB_NAME = "d55v7qh9k51mqu"
	# DB_USERNAME = "wisaevtuesximp"
	# DB_PASSWORD = "7bd99538dc7ddaae24dd9f0ed6047b4f4c87d2320d6efb7403cedd21c5d5d914"
	DB_PORT = 5432

	SESSION_COOKIE_SECURE = False
