from .base import *
_CONFIG_FILE = "development"

DEBUG = True

# Must have some key, so we'll just use bogus one
SECRET_KEY = '00000000000000000000000000000000000000000000000000'

# Restrict host/domain names (ignored if DEBUG=True)
ALLOWED_HOSTS = []
