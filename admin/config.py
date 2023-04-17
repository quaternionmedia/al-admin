from os import environ

PRODUCTION = bool(environ.get('PRODUCTION', False))
DB_URL = environ.get('DB_URL', 'sqlite:///alfred.sqlite')
