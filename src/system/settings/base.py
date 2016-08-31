"""
Django settings for djangotemplate project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VENV_DIR = os.path.dirname(BASE_DIR)


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_generate_secret_key',

	'sampleapp',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, "system", "templates")],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'system.wsgi.application'

PREPEND_WWW = True


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	# SQLite backend
	# https://docs.djangoproject.com/en/1.10/ref/databases/#sqlite-notes
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(VENV_DIR, 'development.sqlite3'),
	},
	# MySQL/MariaDB backend (must also install the mysqlclient pip package)
	# https://docs.djangoproject.com/en/1.10/ref/databases/#mysql-notes
	# 'default': {
	# 	'ENGINE': 'django.db.backends.mysql',
	# 	'NAME': 'djangotemplate',
	# 	'USER': 'sampleuser',
	# 	'PASSWORD': 'samplepass',
	# 	'HOST': '127.0.0.1',
	# 	'PORT': '5432',
	# },
	# PostgreSQL backend (must also install python-psycopg2)
	# https://docs.djangoproject.com/en/1.10/ref/databases/#postgresql-notes
	# 'default': {
	# 	'ENGINE': 'django.db.backends.postgresql',
	# 	'NAME': 'djangotemplate',
	# 	'USER': 'sampleuser',
	# 	'PASSWORD': 'samplepass',
	# 	'HOST': '127.0.0.1',
	# 	'PORT': '5432',
	# },
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Base URL to use for static files when {% static '<file>' %} is used
STATIC_URL = '/static/'
# Location to collect static files to when the collectstatic command is run
STATIC_ROOT = os.path.join(VENV_DIR, "collected_static")
STATICFILES_DIRS = (
	# Include the static directory in the list of directories that 'python manage.py collectstatic'
	#     copies files from (each app's static directory is already included by default)
	os.path.join(BASE_DIR, "system", "static"),
)

# Base URL to use for media files; access from templates with {{ MEDIA_URL }} if django.template.context_processors.media is configured
MEDIA_URL = '/media/'
# Location to hold user-uploaded files
MEDIA_ROOT = os.path.join(VENV_DIR, "uploaded_media")

_CONFIG_FILE = "base"
