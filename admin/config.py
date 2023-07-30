from os import environ, getenv

DEBUG = bool(environ.get('DEBUG', True))
DB_URL = environ.get('DB_URL', 'sqlite:///alfred.sqlite')

SECRET = getenv('ALFRED_SECRET', '1234567890')
AUTH0_CLIENT_ID = getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = getenv('AUTH0_DOMAIN')
