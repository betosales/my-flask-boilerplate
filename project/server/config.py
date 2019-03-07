<<<<<<< HEAD
# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
=======
import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://rsales:4br4c4d4br4@localhost/'
database_name = 'poc_login'
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
<<<<<<< HEAD
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONNECTION_URL = os.getenv('CONNECTION_URL')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = CONNECTION_URL + DATABASE_NAME
    BCRYPT_LOG_ROUNDS = 13
=======
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
<<<<<<< HEAD
=======
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = BaseConfig.SQLALCHEMY_DATABASE_URI + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    BCRYPT_LOG_ROUNDS = 4
=======
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009


class ProductionConfig(BaseConfig):
    """Production configuration."""
<<<<<<< HEAD
    DEBUG = False
=======
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql:///example'
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009
