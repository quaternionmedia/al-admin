from os import environ

DEBUG = bool(environ.get('DEBUG', True))
DB_URL = environ.get('DB_URL', 'sqlite:///alfred.sqlite')
