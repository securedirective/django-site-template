# Django Site Template

Status: **Built with Django v1.10**




## Overview

This template was created to address the initial difficulty in transitioning a new project created with Django's `startproject` command into a project ready to deploy to a production server. Throughout this template and documentation, the project name is `djangotemplate`, and the domain name is the fictitious `djangotemplate.tech`. Change this for your project.

The first commit of this repo was made immediately after running the following commands:

```
mkdir djangotemplate; cd djangotemplate
virtualenv --python=python3 .
source bin/activate
pip install django
django-admin startproject djangotemplate
cd djangotemplate; python manage.py startapp sampleapp
```

This way, when Django updates to a new version, you can follow the same steps and compare the result to the first commit to see exactly what Django may have changed about their default project template.

From that first commit, the directory structure was changed to make things less confusing. By default, if you start a blank project, you'd end up with a directory tree like this:

* djangotemplate/ (your virtual environment root)
  * djangotemplate/ (Django's root)
    * djangotemplate/ (the primary app)
      * settings.py
      * urls.py
      * wsgi.py
    * manage.py

With this template, I've named Django's root as `src` to distinguish your source code from all the deployment and maintenance scripts you accumulate in the virtual environment root. For consistency across projects, I've also renamed Django's initial app to `system`. Lastly, to reduce code duplication, I've split the settings file into three sub-files. This results in the following directory tree:

* djangotemplate/ (your virtual environment root)
  * src/ (Django's root)
    * system/ (the primary app)
      * settings/
        * base.py
        * development.py (imports from base.py)
        * production.py (imports from base.py)
        * staging.py (imports from production.py)
      * urls.py
      * wsgi.py
    * manage.py
  * bin/
  * lib/
  * include/
  * [deployment/maintenance scripts]

On top of that basic concept, I've added many tools to ease the deployment of a secure website. Yes, all of this is a matter of personal preference. Feel free to fork it.

<Describe helper scripts>

Lastly, note that this template has **only been tested on Python 3.4.x**




## How to Use

This template is designed to be used within a Python [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (venv) to keep everything self-contained. It is recommended that the virtual environment's root is also your git repo's root, with a `.gitignore` configured to exclude the `bin`, `lib`, and `include` directories. Keep any sensitive information (keys, passwords) in their own files that can be excluded from the repo.




### Initial Setup of Development Environment

The development environment obviously has some unique characteristics, compared with the production/staging environments, to make things easy to work with:
* Run the server with `./devserver`. This will launch Django's internal server which hosts both your application and all static files.
* Reload the server by hitting Ctrl+C and re-running `./devserver`, but this rarely will be necessary since Django monitors source files for changes and reloads within seconds of seeing any.
* Static content is served by Django itself, so no need to call `collectstatic`
* Uses SQLite to store data in `development.sqlite3`.
* Does not restrict host names with the ALLOWED_HOSTS setting.
* DEBUG is True by default.
* Access at `http://<IP>:8000/`.
* Has no secure version of the site.
* Django's server will show any runtime errors in the console rather than logging them to a file.

First, create a new directory for your virtual environment and `cd` inside it:
```
mkdir djangotemplate-dev
cd djangotemplate-dev
```

Then clone this repository (must be done first, while the directory is still empty):
```
git clone https://github.com/securedirective/django-site-template.git ./
```

If you want to start a clean repository instead of working from this one, then run this instead:
```
git clone --depth=1 https://github.com/securedirective/django-site-template.git ./
rm -rf ./.git
git init
```

Then run these commands to initialize the venv:
```
virtualenv --python=python3 .
source bin/activate
pip install -r requirements.txt
```

Initialize the database
```
./m migrate
```

This is a perfect example of how my `m` shortcut script makes administration tasks much easier. Since the production settings file is the default (for safety), this is what you'd have to type if you didn't have the shortcut:
```
python src/manage.py migrate --settings system.settings.development
```

At this point, you should be able to run Django's internal development server using another useful shortcut script.
```
./devserver
```

If you load `http://localhost:8000`, the sample home page should show that you are using the 'development' settings file, and the next line should be green since Django is serving the static content itself.

If all is working adapt the project to your needs by searching for any references to `djangotemplate` or `dt` and replace with the names of your project. Then commit that to the repo
```
grep -Rn -e djangotemplate -e dt --exclude-dir=".git" --exclude-dir="bin" --exclude-dir="include" --exclude-dir="lib" --exclude-dir="__pycache__" *
git commit -a -m "<description>"
```




### Production/Staging

The production/staging environments are configured differently from the development environment:
* Start the website using systemd: `systemctl start djangotemplate` or `systemctl start djangotemplate-staging`.
* Reload the server by modifying the `reload` file: `touch reload`.
* Static (/static) and user-uploaded media (/media) are served by nginx.
* Databases are configured separately (`production.sqlite3` and `staging.sqlite3` by default), so it's easy to test things out on a copy of the live website that you can totally trash if needed.
* Restricts host names with the ALLOWED_HOSTS setting. Note that nginx also does this.
* DEBUG is False.
* Access the production site at `http://<domain>:80/` and the staging site at `http://<domain>:81/`. You can use iptables as needed to restrict access to this site to only active developers.
* Access the secure version of the production site at `http://<domain>:443/` and the staging site at `http://<domain>:444/`.
* Any errors from the systemd service or the uWSGI server will go to the systemd journal (`journalctl -u djangotemplate` or `journalctl -u djangotemplate-staging`). Any errors from Django itself will output through nginx (`/var/log/nginx/djangotemplate-error.log`).

As you can see, the production and staging sites are as identical as they can be. They should only differ in the following ways:
* The systemd service files for production and staging cannot have the same name, even if they are in different directories. Because systemd uses the symlink target's name as the internal service name, systemd will see them as the same service and won't let both run at the same time.
* Some files, such as the nginx config, require absolute paths and must be changed to point to the venv in use.
* Port numbers differ slightly so the same domain name can be used.

I've added a custom Django management command `generate_configs` to dynamically create those configs that differ between staging and production, so you don't have to do it manually. Simply edit the `src/system/settings/nginx.conf.tmpl` and `src/system/settings/uwsgi.service.tmpl` files and run `./m generate_configs` to generate the files. See below for more information.

Now, to actually setup your staging environment (the steps are the same for the production environment)...

Create a new `djangotemplate-staging` directory and initialize it like you did with the development environment:
```
mkdir djangotemplate-staging
cd djangotemplate-staging
```

Instead of cloning this template as your starting point, though, clone from your development environment so it includes any changes you've made there:
```
git clone <dev_environment> ./
```

Initialize the `secretkey.txt` file to hold Django's secret key outside of source control:
```
./m rotate_secret_key
```

Initialize the config files that must be dynamically created:
```
./m generate_configs
```

Run Django's deployment check. It may complain about things that the `ssl.conf` will take care of, so take it with a grain of salt:
```
./m check --deploy
```

Collect static files from your various apps and packages into one directory for nginx to server from:
```
./m collectstatic --link
```

Symlink the dynamic configs to the appropriate places and start the uWSGI server (you'll have to run these as root):
```
venv=/home/dt/djangotemplate-staging
ln -sf $venv/djangotemplate-staging.conf /etc/nginx/sites-available/djangotemplate-staging.conf
ln -sf /etc/nginx/sites-available/djangotemplate-staging.conf /etc/nginx/sites-enabled/djangotemplate-staging.conf
ln -sf $venv/djangotemplate-staging.service /etc/systemd/system/djangotemplate-staging.service
systemctl daemon-reload
systemctl start djangotemplate-staging
systemctl reload nginx
```

For your production environment, do the same thing without the `-staging` prefixes:
```
venv=/home/dt/djangotemplate
ln -sf $venv/djangotemplate.conf /etc/nginx/sites-available/djangotemplate.conf
ln -sf /etc/nginx/sites-available/djangotemplate.conf /etc/nginx/sites-enabled/djangotemplate.conf
ln -sf $venv/djangotemplate.service /etc/systemd/system/djangotemplate.service
systemctl daemon-reload
systemctl start djangotemplate
systemctl reload nginx
```




### Setup a free SSL certificate from Let's Encrypt

`certbot certonly --standalone -d djangotemplate.tech -d www.djangotemplate.tech`

Create a self-signed certificate:




## Troubleshooting




### Error Logs

When troubleshooting errors, it is vital you know where the logs are stored. Any errors with the systemd service or the uWSGI server will go to the systemd journal and can be accessed by running `systemctl status djangotemplate` or `journalctl -u djangotemplate`. You can have a running log on the screen with `journalctl -f -u djangotemplate`.

Any errors from nginx will go to `/var/log/nginx/djangotemplate-error.log`. Keep a running log on the screen with `tail -f /var/log/nginx/djangotemplate-error.log`. Non-error access is also logged by default to `/var/log/nginx/djangotemplate-access.log`, except for the `/static` and `/media` directories.




### Communication Paths

Run everything below from within the virtual environment:
`cd /var/www/djangotemplate_venv; source bin/activate`

Test your Django site: Client <-> VENV[ HTTP port 8000 <-> Django/DEV ]
`python src/manage.py runserver 0.0.0.0:8000 --settings system.settings.development`
Accessing http://www.djangotemplate.tech:8000 should show the sample website

Test uWSGI by itself: Client <-> VENV[ HTTP port 8000 <-> uWSGI <-> Python ]
`uwsgi --http=:8000 --wsgi-file=uwsgi-test.py`
Accessing http://www.djangotemplate.tech:8000 should show "uWSGI Test successful"

Test Django and uWSGI together: Client <-> VENV[ HTTP port 8000 <-> uWSGI <-> Django/WSGI ]
`uwsgi --http=:8000 --chdir=./src --module=system.wsgi`
Accessing http://www.djangotemplate.tech:8000 should show the sample website (static files will be broken, since the production config doesn't host those)

Test nginx by itself: Client <-> HTTP port 80 <-> nginx
`systemctl start nginx`
Accessing http://www.djangotemplate.tech should show nginx's default page when a site is not configured

Test nginx and uWSGI together: Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Python ]
`systemctl start nginx`
`uwsgi --socket=uwsgi.sock --chmod-socket=666 --wsgi-file=uwsgi-test.py`
Accessing http://www.djangotemplate.tech should show the sample website

Test nginx with Django: Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Django/WSGI ]
`systemctl start nginx`
`python src/manage.py collectstatic -c -l`
`uwsgi --chdir=./src --socket=../uwsgi.sock --chmod-socket=666 --module=system.wsgi`
Accessing http://www.djangotemplate.tech should show the sample website with static files working




## Self-signed Certificate

In case you need to create/recreate a self-signed certificate for testing purposes, here's how:
```
openssl genrsa -des3 -out server.key 2048
openssl req -new -key server.key -out server.csr
mv server.key server.key.org
openssl rsa -in server.key.org -out server.key
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
del server.key.org
```
