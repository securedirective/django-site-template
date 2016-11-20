### Communication Paths ###

Run everything below from within the virtual environment...

**Test your Django site**
```
$> src/devserver
```

Accessing your site on port 9000 should show the sample website. This tests the following path: `Client <-> VENV[ HTTP port 9000 <-> Django/DEV ]`

**Test uWSGI by itself**
```
$> uwsgi --http=:9000 --wsgi-file=uwsgi-test.py
```

Accessing your site on port 9000 should show "uWSGI Test successful". This tests the following path: `Client <-> VENV[ HTTP port 9000 <-> uWSGI <-> Python ]`

**Test Django and uWSGI together**
```
$> uwsgi --http=:9000 --chdir=./src --module=system.wsgi
```

Accessing your site on port 9000 should show the sample website (static files will be broken, since the production config doesn't host those). This tests the following path: `Client <-> VENV[ `HTTP port 9000 <-> uWSGI <-> Django/WSGI ]

**Test nginx by itself**
```
#> systemctl start nginx
```

Accessing your site on port 80 should show nginx's default page when a site is not configured. This tests the following path: `Client <-> HTTP port 80 <-> nginx`

**Test nginx and uWSGI together**
```
#> systemctl start nginx
$> uwsgi --socket=uwsgi.sock --chmod-socket=666 --wsgi-file=uwsgi-test.py
```

Accessing your site on port 80 should show the sample website. This tests the following path: `Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Python ]`

**Test nginx with Django**
```
#> systemctl start nginx
$> src/m collectstatic --link
$> uwsgi --chdir=./src --socket=../uwsgi.sock --chmod-socket=666 --module=system.wsgi
```

Accessing your site on port 80 should show the sample website with static files working. This tests the following path: `Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Django/WSGI ]`




## Self-signed Certificate ##

In case you need to create/recreate a self-signed certificate for testing purposes, here's how:
```
$> mkdir ssl_keys && cd ssl_keys
$> openssl genrsa -out server.key 2048
$> openssl req -new -key server.key -out demo.csr  # Enter djangotemplate.tech as the CN, leave others blank
$> openssl x509 -req -days 365 -in demo.csr -signkey server.key -out demo.crt
```

Then add this to your `src/system/settings/nginx.conf.tmpl`:
```
ssl_certificate       {{ settings.CONF_DIR }}/secret/server.crt;
ssl_certificate_key   {{ settings.CONF_DIR }}/secret/server.key;
```

Lastly, add `HTTPS_ENABLED = True` to `src/system/settings/production.py` and regenerate the config files:
```
$> src/m generateconfigs
```
