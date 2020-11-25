from os import environ

name = 'Thermo Ai Central Server',
version = '3.0.0',
description = 'Source code for the Thermo Ai Central Server use Blueprints in Flask.',
long_description = "long_description",
long_description_content_type = 'text/markdown',
url = 'https://git.javis.vn/thermal-detection/thermo-ai-central-server.git',
classifiers = ['Programming Language :: Python :: 3.8', ],
keywords = 'Flask Flask-Assets Blueprints',
packages = "find_packages()",
install_requires = ['Flask',
                    'Flask_assets'],
entry_points = {
    'console_scripts': [
        'install=wsgi:__main__',
    ],
}


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret!'
    FLASK_ENV = environ.get('FLASK_ENV')

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = environ.get('STATIC_FOLDER')
    TEMPLATES_FOLDER = environ.get('TEMPLATES_FOLDER')
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    """Base config vars."""

    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')

    # db_engine = db.create_engine(CONF["database"]["connection"])
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
