from django.core.management.base import BaseCommand
import os
import string

class Command(BaseCommand):
	help = 'Generate or regenerate the contents of secretkey.txt'

	def add_arguments(self, parser):
		parser.add_argument(
			'--force',
			action='store_true',
			dest='force',
			default=False,
			help='Replace the existing key without prompting'
		)

	def handle(self, *args, **options):
		# Determine where to write the key
		from django.conf import settings
		key_dir = os.path.join(settings.BASE_DIR, 'system', 'settings')
		key_file = os.path.join(key_dir, 'secretkey.txt')

		# If the file exists and already has contents, then only replace if --force argument was given
		try:
			existing_key = open(key_file).read().strip()
			if existing_key and not options['force']:
				self.stdout.write("EXISTING SECRET KEY: {}".format(existing_key))
				if input("Replace this with a new key? [Y/N] ").upper() != 'Y':
					return
		except FileNotFoundError:
			# No key file found, so we're safe to create a new one without prompting
			pass

		# Generate new key
		import random
		char_list = string.ascii_letters + string.digits + string.punctuation
		generated_key = ''.join([random.SystemRandom().choice(char_list) for _ in range(50)])
		self.stdout.write("NEW SECRET KEY:      {}".format(generated_key))

		# Write new key to file
		secret = open(key_file, 'w')
		secret.write(generated_key)
		secret.close()
		self.stdout.write("Written to {}".format(key_file))
