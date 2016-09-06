from django.core.management.base import BaseCommand

class Command(BaseCommand):
	help = 'Generate configuration files from templates'

	def handle(self, *args, **options):
		import os
		from django.conf import settings
		from django.template import Context, Template

		# Load DYNAMIC_CONFIGS from the current settings file
		try:
			self.stdout.write("Current settings file: {}".format(settings.CONFIG_FILE_IN_USE))
		except AttributeError:
			pass
		try:
			settings.DYNAMIC_CONFIGS
		except AttributeError:
			self.stderr.write('Cannot find DYNAMIC_CONFIGS in settings file')
			return

		for config in settings.DYNAMIC_CONFIGS:
			self.stdout.write('')

			# Default directories if not specified
			try:
				if not config['template'].startswith('/'): config['template'] = os.path.join(settings.BASE_DIR, 'system', 'settings', config['template'])
				if not config['output'].startswith('/'): config['output'] = os.path.join(settings.VENV_DIR, config['output'])
			except KeyError as e:
				self.stderr.write("'template' or 'output' parameters not specified: "+repr(config))
				continue # Go on to the next config file

			# Load the template file
			file = None
			try:
				file = open(config['template'], 'r')
				contents = file.read()
				self.stdout.write("Loaded template '{}'".format(config['template']))
			except Exception as e:
				self.stderr.write("Failed to load template: {}".format(repr(e)))
				continue # Go on to the next config file
			finally:
				if file: file.close()

			# Render the template
			try:
				template = Template(contents)
				output = template.render(Context({'settings': settings}))
			except Exception as e:
				self.stderr.write("Failed to render template '{}': {}".format(config['template'], repr(e)))
				continue # Go on to the next config file

			# Output the rendered results
			file = None
			try:
				file = open(config['output'], 'w')
				file.write(output)
				self.stdout.write("Wrote output file '{}'".format(config['output']))
			except Exception as e:
				self.stderr.write("Failed to write new output file '{}': {}".format(config['output'], repr(e)))
				continue # Go on to the next config file
			finally:
				if file: file.close()
