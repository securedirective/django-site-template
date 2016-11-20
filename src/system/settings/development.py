from .base import *
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# Debug mode will help troubleshoot errors
DEBUG = True

# Custom settings for dynamically-generated config files
PROJECT_NAME = PROJECT_NAME+'-development'

# Must have some key, so we'll just use bogus one
SECRET_KEY = '00000000000000000000000000000000000000000000000000'

# Specify the domain names Django will respond to
ALLOWED_HOSTS = [
	'localhost', '127.0.0.1',   # Access from same machine
	'192.168.224.102',
]

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
	# SQLite backend
	# https://docs.djangoproject.com/en/1.10/ref/databases/#sqlite-notes
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(DATA_DIR, 'development.sqlite3'),
	},
}

# Save emails to files instead of actually sending them
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(DATA_DIR, 'emails')
