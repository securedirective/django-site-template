project_name = 'djangotemplate'
domain_name = project_name + '.tech'

unix_user = 'dt'
unix_group = 'dt'

import os
is_staging = os.path.dirname(os.path.abspath(__file__)).endswith('-staging')
print('Generating config files for ' + ['PRODUCTION','STAGING'][is_staging] + ' environment')

if is_staging:
	venv = '/home/'+unix_user+'/'+project_name+'-staging'
	renders = [
		# nginx config for /etc/nginx/sites-available
		{ 'output': 'nginx.conf',
			'template': 'confgen_nginx.tmpl',
			'venv': venv,
			'domain': domain_name,
			'port': 81,
			'ssl': False,
			'ssl_port': 444,
			'ssl_key_bundle': venv + '/keys/fullchain.pem',
			'ssl_private_key': venv + '/keys/privkey.pem',
		},

		# systemd service file for /ecc/systemd/system
		{ 'output': 'uwsgi.service',
			'template': 'confgen_uwsgi.tmpl',
			'venv': venv,
			'unix_user': unix_user,
			'unix_group': unix_group,
			'settings_override': 'system.settings.staging',
		},
	]

else:
	venv = '/home/'+unix_user+'/'+project_name
	renders = [
		# nginx config for /etc/nginx/sites-available
		{ 'output': 'nginx-production.conf',
			'template': 'confgen_nginx.tmpl',
			'venv': venv,
			'domain': domain_name,
			'port': 80,
			'ssl': True,
			'ssl_port': 443,
			'key_path': '/etc/letsencrypt/live/'+domain_name,
			'ssl_key_bundle': '/etc/letsencrypt/live/'+domain_name+'/fullchain.pem',
			'ssl_private_key': '/etc/letsencrypt/live/'+domain_name+'/privkey.pem',
			'ssl_trusted_ca_cert': '/etc/letsencrypt/live/'+domain_name+'/chain.pem',
		},

		# systemd service file for /ecc/systemd/system
		{ 'output': 'uwsgi-production.service',
			'template': 'confgen_uwsgi.tmpl',
			'venv': venv,
			'unix_user': unix_user,
			'unix_group': unix_group,
		},
	]
