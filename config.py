import os
import uuid

basedir = os.path.abspath(os.path.dirname(__file__))

##main configuration class for the app
##configuring mail configuration
##database configuration
class Config:
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 578
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME","yahyasaid935@gmail.com")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	MAIL_USE_TLS = True
	SQLALCHEMY_RECORD_QUERIES = True
	SECRET_KEY = uuid.uuid4().hex
	SQLALCHEMY_TRACK_MODIFICATIONS = False


	@staticmethod
	def init_app(app):
		pass


##Developement configuration to use derived from Config
##and speciliaze it with custom fields
##including set application logger
class DevelopmentConfig(Config):
	SQLALCHEMY_DATABASE_URIv= os.getenv("DEV_DATABASE") or "sqlite:///"+os.path.join(basedir,"dev_database.sqlite")
	DEBUG = True
	@staticmethod
	def init_app(app):
		import logging
		from logging import StreamHandler
		handler = StreamHandler()
		handler.setLevel(logging.DEBUG)
		app.logger.addHandler(handler)



##main config for running 
#no logger is needed here
class TestingConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DEV") or "sqlite:///"+ os.path.join(basedir,"test_database.sqlite")
	WTF_CSRF_ENABLED = False
	TESTING = True

#all config
config = {
		"development":DevelopmentConfig,
		"testing":TestingConfig

	}
