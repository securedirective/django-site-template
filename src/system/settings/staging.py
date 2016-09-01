from .production import *
_CONFIG_FILE = "staging"

# Override database setting
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'staging.sqlite3'),
	},
}
