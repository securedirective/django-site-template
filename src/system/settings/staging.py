from .production import *

CONFIG_FILE_IN_USE = os.path.splitext(os.path.basename(__file__))[0]

# Override database setting
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'staging.sqlite3'),
	},
}
