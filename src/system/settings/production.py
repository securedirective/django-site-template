from .base import *
_CONFIG_FILE = "production"

DEBUG = False

# Import key from an external file, so it doesn't get included in version control
# If you have generate_secret_key installed, you can regenerate a new one with this: python manage.py generate_secret_key system/settings/secretkey.txt
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secretkey.txt')) as f:
	SECRET_KEY = f.read().strip()

# Restrict host/domain names
ALLOWED_HOSTS = ['.djangotemplate.tech']

# Various settings needed to fix warnings from python manage.py check --settings system.settings.production --deploy
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
