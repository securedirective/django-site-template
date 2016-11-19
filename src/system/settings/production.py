from .base import *
CONFIG_FILE_IN_USE = get_file_name_only(__file__)  # Custom setting

# Custom settings for dynamically-generated config files
UWSGI_PORT = 9001
HTTP_PORT = 80
HTTPS_PORT = 443
HTTPS_ENABLED = True

# Never use debug mode in production
DEBUG = False

# Import key from an external file, so it doesn't get included in version control
SECRET_KEY_FILE = os.path.join(CONF_DIR, 'secret', 'secretkey.txt')
try:
	with open(SECRET_KEY_FILE, 'r') as f:
		SECRET_KEY = f.read().strip()
except:
	SECRET_KEY = '*** NOT CONFIGURED ***'
	print("WARNING: the SECRET_KEY setting has not yet been configured!")

# Specify the domain names Django will respond to
ALLOWED_HOSTS = [
  'www.' + DOMAIN_NAME,
  DOMAIN_NAME,  # This one is required for PREPEND_WWW to work
]

# If the domain name doesn't start with "www." then add it
PREPEND_WWW = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
	# SQLite backend
	# https://docs.djangoproject.com/en/1.10/ref/databases/#sqlite-notes
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'production.sqlite3'),
	},
	# MySQL/MariaDB backend (must also install the mysqlclient pip package)
	# https://docs.djangoproject.com/en/1.10/ref/databases/#mysql-notes
	# 'default': {
	# 	'ENGINE': 'django.db.backends.mysql',
	# 	'NAME': 'sampledb',
	# 	'USER': 'sampleuser',
	# 	'PASSWORD': 'samplepass',
	# 	'HOST': '127.0.0.1',
	# 	'PORT': '5432',
	# },
	# PostgreSQL backend (must also install python-psycopg2)
	# https://docs.djangoproject.com/en/1.10/ref/databases/#postgresql-notes
	# 'default': {
	# 	'ENGINE': 'django.db.backends.postgresql',
	# 	'NAME': 'sampledb',
	# 	'USER': 'sampleuser',
	# 	'PASSWORD': 'samplepass',
	# 	'HOST': '127.0.0.1',
	# 	'PORT': '5432',
	# },
}

# Various settings needed to fix warnings from python manage.py check --settings system.settings.production --deploy
if HTTPS_ENABLED:
	SESSION_COOKIE_SECURE = True
	CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True

# Security settings our ssl.conf takes care of
# X_FRAME_OPTIONS = 'DENY'
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
