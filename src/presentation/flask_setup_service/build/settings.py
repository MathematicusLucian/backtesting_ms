# -*- coding: utf-8 -*-
import os

class Config(object):
    APPNAME = 'MDI API'
    SUPPORT_EMAIL = ''
    VERSION = '1.0.0'
    APPID = 'mdi_docker'
    SECRET_KEY = os.urandom(24)
    TESTING = False

class DevConfig(Config):
    DEBUG = True
    FLASK_ENV='development'
    PROFILE = True

class QAConfig(Config):
    DEBUG = False
    FLASK_ENV='qa'
    STAGING = True
    TESTING = True

class ProdConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    STAGING = False

config = {
    'development': DevConfig,
    'testing': QAConfig,
    'production': ProdConfig,
    'default': DevConfig
}
