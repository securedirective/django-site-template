#!/usr/bin/env python

from django.template.loader import render_to_string

# See https://docs.djangoproject.com/en/1.10/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage
if __name__ == '__main__':
	import os
	import django
	from django.conf import settings
	settings.configure(
		DEBUG=True,
		TEMPLATES = [{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [os.path.dirname(os.path.abspath(__file__))],
		}],
	)
	django.setup()

# Create your views here.
from confgen_conf import *

for outputfile, context in output_files.items():
	print('\nGenerating ' + outputfile + '...')

	if not 'template' in context:
		print('Template file not specified: ' + str(context))
		continue

	try:
		output = render_to_string(context['template'], context)
	except Exception as e:
		print('Error rendering template '+context['template']+': ' + str(e))

	file = None
	try:
		file = open(outputfile, 'w')
		file.write(output)
		print('Done')
	except Exception as e:
		print('Error writing output: ' + str(e))
	finally:
		if file: file.close()
