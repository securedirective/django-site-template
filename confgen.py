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

for render in renders:
	if not 'template' in render:
		print('Template file not specified; skipping this item...')
		print(render)
		continue
	if not 'output' in render:
		print('Output file not specified; skipping this item...')
		print(render)
		continue

	try:
		output = render_to_string(render['template'], render)
	except Exception as e:
		print('Error rendering template '+render['template']+':\n\t' + str(e))

	file = None
	try:
		file = open(render['output'], 'w')
		file.write(output)
		print('Generated output file: ' + render['output'])
	except Exception as e:
		print('Error writing output to '+render['output']+':\n\t' + str(e))
	finally:
		if file: file.close()
