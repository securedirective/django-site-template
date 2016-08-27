from .base import *

DEBUG = False

# Import key from an external file, so it doesn't get included in version control
# If you have generate_secret_key installed, you can regenerate a new one with this: python manage.py generate_secret_key system/settings/secretkey.txt
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'secretkey.txt')) as f:
	SECRET_KEY = f.read().strip()

# Restrict host/domain names
ALLOWED_HOSTS = ['.djangotemplate.tech']
