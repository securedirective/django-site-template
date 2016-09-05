from .base import *

CONFIG_FILE_IN_USE = os.path.splitext(os.path.basename(__file__))[0]

DEBUG = True

# Must have some key, so we'll just use bogus one
SECRET_KEY = '00000000000000000000000000000000000000000000000000'

# Restrict host/domain names (ignored if DEBUG=True)
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
	# SQLite backend
	# https://docs.djangoproject.com/en/1.10/ref/databases/#sqlite-notes
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'development.sqlite3'),
	},
}
