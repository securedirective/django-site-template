from .production import *
CONFIG_FILE_IN_USE = os.path.splitext(os.path.basename(__file__))[0]

# Settings for dynamically-generated config files
PROJECT_NAME = PROJECT_NAME+'-staging'
HTTP_PORT = 81
HTTPS_PORT = 444
DYNAMIC_CONFIGS = (
	{'template':'nginx.conf.tmpl',		'output':PROJECT_NAME+'.conf'},
	{'template':'uwsgi.service.tmpl',	'output':PROJECT_NAME+'.service'},
)

# Override database setting
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'staging.sqlite3'),
	},
}
