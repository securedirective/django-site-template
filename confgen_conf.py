project_name = 'djangotemplate'
domain_name = 'djangotemplate.tech'

unix_user = 'dt'
unix_group = 'dt'

import os
is_staging = os.path.dirname(os.path.abspath(__file__)).endswith('-staging')
print('Generating config files for ' + ['PRODUCTION','STAGING'][is_staging] + ' environment')

if not is_staging:
	# PRODUCTION SETTINGS
	venv = '/home/'+unix_user+'/'+project_name
	output_files = {
		# nginx config for /etc/nginx/sites-available
		project_name+'.conf': {
			'template': 'confgen_nginx.tmpl',
			'venv': venv,
			'project': project_name,
			'domain': domain_name,
			'port': 80,
			'ssl': False,
			'ssl_port': 443,
		},

		# systemd service file for /ecc/systemd/system
		project_name+'.service': {
			'template': 'confgen_uwsgi.tmpl',
			'venv': venv,
			'user': unix_user,
			'group': unix_group,
		},
	}

else:
	# STAGING SETTINGS
	venv = '/home/'+unix_user+'/'+project_name+'-staging'
	output_files = {
		# nginx config for /etc/nginx/sites-available
		project_name+'-staging.conf': {
			'template': 'confgen_nginx.tmpl',
			'venv': venv,
			'project': project_name+'-staging',
			'domain': domain_name,
			'port': 81,
			'ssl': False,
			'ssl_port': 444,
		},

		# systemd service file for /ecc/systemd/system
		project_name+'-staging.service': {
			'template': 'confgen_uwsgi.tmpl',
			'venv': venv,
			'user': unix_user,
			'group': unix_group,
			'settings_override': 'system.settings.staging',
		},
	}
