# Django Site Template

Status: **Built with Django v1.10**




## Overview

This template was created to address the initial difficulty in transitioning a new project created with Django's `startproject` command into a project ready to deploy to a production server. Throughout this template and documentation, the project name is `djangotemplate`, and the domain name is the fictitious `djangotemplate.tech`. Change this for your project.

Note that this template has **only been tested on Python 3.4.x on a Debian-based system**. I have no plans to support Python 2.x or Windows, but if you find issues on other Linux distros, I'd be willing to adapt my template as needed.

The first commit of this repo was made immediately after running the following commands:

```
\t=djangotemplate
mkdir $PROJECT && cd $PROJECT
virtualenv --python=python3 . && source bin/activate
pip install django
django-admin startproject $PROJECT
cd $PROJECT && python manage.py startapp sampleapp && cd ..
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
* `./m`: A bash script to run `src/manage.py` without requiring you to activate the venv first, and without requiring the current directory to be the venv. It also passes the proper `--settings` parameter by analyzing the venv directory name to know which settings file to use (ex: `project_dev` will trigger the use of `--settings system.settings.development`).
* `./fixattr`: A simple bash script to run `chmod +x` on those files that should be executable, such as `./m`. I created this because file permissions get messed up by some text editors when editing your code on a remote Windows computer through a samba share.
* `./devserver`: Just a shortcut to running `python src/manage.py runserver 0.0.0.0:8000 --settings system.settings.development`.
* `./m generate_configs`: A custom Django management command to generate some config files from templates, allowing you to have slightly different configs for production and staging environments. Define which configs should be dynamically created by adding `DYNAMIC_CONFIGS` to your settings file.
* `./m rotate_secret_key`: A custom Django management command to rotate the `SECRET_KEY` found in `src/system/settings/secretkey.txt`. This allows you to keep your secret key out of source control without manually editing your settings file.

Throughout this documentation, I've used a `$PROJECT` variable to refer to the `djangotemplate-dev`, `djangotemplate-staging`, or `djangotemplate` as much as possible to make it easy for you to copy and paste these commands right into your terminal after adjusting `$PROJECT` to your own project name.




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
PROJECT=djangotemplate-dev
mkdir $PROJECT && cd $PROJECT
```

Then clone this repository (must be done first, while the directory is still empty):
```
git clone https://github.com/securedirective/django-site-template.git ./
```

Then run these commands to initialize the venv:
```
virtualenv --python=python3 . && source bin/activate
pip install -r requirements.txt
```

Initialize the database
```
./m migrate
```

At this point, you should be able to run Django's internal development server using another useful shortcut script.
```
./devserver
```

If you load `http://localhost:8000`, the sample home page should show that you are using the 'development' settings file, and the next line should be green since Django is serving the static content itself.




### Adapt to Your Project

If you would like to start a clean repository, so the commits of this template don't show up in your own commit log, do this:
```
rm -rf ./.git
git init
```

Now, search for any references to `djangotemplate` or `dt`, and replace with the names of your project:
```
grep -RIn -e djangotemplate -e dt --exclude=README.md --exclude-dir=".git" --exclude-dir="bin" --exclude-dir="include" --exclude-dir="lib" --exclude-dir="__pycache__" *
```

You may also want to remove the `README.md` so you can start your own:
```
rm README.md
```

At this point, you should commit these changes before you go any further:
```
git add -A
git commit -m "Initial commit, based on django-site-template"
```

If you use Github for your source control, you'll probably want to add/change your remote link and push your changes to the server:
```
git remote add origin https://github.com/<your_repo>.git
git push --set-upstream origin master
```




### Production/Staging

The production/staging environments are configured differently from the development environment:
* Start the website using systemd: `systemctl start $PROJECT`.
* Reload the server by modifying the `reload` file: `touch reload`.
* Static (/static) and user-uploaded media (/media) are served by nginx.
* Databases are configured separately (`production.sqlite3` and `staging.sqlite3` by default), so it's easy to test things out on a copy of the live website that you can totally trash if needed.
* Restricts host names with the ALLOWED_HOSTS setting. Note that nginx also does this.
* DEBUG is False.
* Access the production site at `http://<domain>:80/` and the staging site at `http://<domain>:81/`. You can use iptables as needed to restrict access to this site to only active developers.
* Access the secure version of the production site at `http://<domain>:443/` and the staging site at `http://<domain>:444/`.
* Any errors from the systemd service or the uWSGI server will go to the systemd journal (`journalctl -u $PROJECT`). Any errors from Django itself will output through nginx (`/var/log/nginx/$PROJECT-error.log`).

As you can see, the production and staging sites are as identical as they can be. They should only differ in the following ways:
* The systemd service files for production and staging cannot have the same name, even if they are in different directories. Because systemd uses the symlink target's name as the internal service name, systemd will see them as the same service and won't let both run at the same time.
* Some files, such as the nginx config, require absolute paths and must be changed to point to the venv in use.
* Port numbers differ slightly so the same domain name can be used.

My custom `./m generate_configs` command will dynamically create those configs that differ between staging and production, so you don't have to do it manually. Simply edit the `src/system/settings/nginx.conf.tmpl` and `src/system/settings/uwsgi.service.tmpl` files and run `./m generate_configs` to generate the files.

Now, to actually setup your staging environment...

Create a new staging environment and initialize it like you did with the development environment:
```
PROJECT=djangotemplate-staging
mkdir $PROJECT && cd $PROJECT
```

Instead of cloning this template as your starting point, though, clone your own repository so it includes any changes you've made there:
```
git clone <div_environment> ./
```

Finish the initialize:
```
virtualenv --python=python3 . && source bin/activate
pip install -r requirements.txt
```

Initialize the `secretkey.txt` file to hold Django's secret key outside of source control:
```
echo null > src/system/settings/secretkey.txt
./m rotate_secret_key
```

Initialize the database with the latest information from the models:
```
./m migrate
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
PROJECT=djangotemplate-staging
VENV=/home/dt/$PROJECT
ln -sf $VENV/$PROJECT.conf /etc/nginx/sites-available/$PROJECT.conf
ln -sf /etc/nginx/sites-available/$PROJECT.conf /etc/nginx/sites-enabled/$PROJECT.conf
ln -sf $VENV/$PROJECT.service /etc/systemd/system/$PROJECT.service
systemctl daemon-reload
systemctl start $PROJECT
systemctl reload nginx
```




## Troubleshooting




### Error Logs

When troubleshooting errors, it is vital you know where the logs are stored. Any errors with the systemd service or the uWSGI server will go to the systemd journal and can be accessed by running `systemctl status $PROJECT` or `journalctl -u $PROJECT`. You can have a running log on the screen with `journalctl -f -u $PROJECT`.

Any errors from nginx will go to `/var/log/nginx/$PROJECT-error.log`. Keep a running log on the screen with `tail -f /var/log/nginx/$PROJECT-error.log`. Non-error access is also logged by default to `/var/log/nginx/$PROJECT-access.log`, except for the `/static` and `/media` directories.




### Communication Paths

Run everything below from within the virtual environment...

**Test your Django site**
```
./devserver
````

Accessing your site on port 8000 should show the sample website. This tests the following path: `Client <-> VENV[ HTTP port 8000 <-> Django/DEV ]`

**Test uWSGI by itself**
```
uwsgi --http=:8000 --wsgi-file=uwsgi-test.py
````

Accessing your site on port 8000 should show "uWSGI Test successful". This tests the following path: `Client <-> VENV[ HTTP port 8000 <-> uWSGI <-> Python ]`

**Test Django and uWSGI together**
```
uwsgi --http=:8000 --chdir=./src --module=system.wsgi
````

Accessing your site on port 8000 should show the sample website (static files will be broken, since the production config doesn't host those). This tests the following path: `Client <-> VENV[ `HTTP port 8000 <-> uWSGI <-> Django/WSGI ]

**Test nginx by itself**
```
systemctl start nginx
````

Accessing your site on port 80 should show nginx's default page when a site is not configured. This tests the following path: `Client <-> HTTP port 80 <-> nginx`

**Test nginx and uWSGI together**
```
systemctl start nginx
uwsgi --socket=uwsgi.sock --chmod-socket=666 --wsgi-file=uwsgi-test.py
````

Accessing your site on port 80 should show the sample website. This tests the following path: `Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Python ]`

**Test nginx with Django**
```
systemctl start nginx
./m collectstatic --link
uwsgi --chdir=./src --socket=../uwsgi.sock --chmod-socket=666 --module=system.wsgi
````

Accessing your site on port 80 should show the sample website with static files working. This tests the following path: `Client <-> HTTP port 80 <-> nginx <-> VENV[ Unix Socket uwsgi.sock <-> uWSGI <-> Django/WSGI ]`




## Self-signed Certificate

In case you need to create/recreate a self-signed certificate for testing purposes, here's how:
```
mkdir ssl_keys && cd ssl_keys
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out demo.csr  # Enter djangotemplate.tech as the CN, leave others blank
openssl x509 -req -days 365 -in demo.csr -signkey server.key -out demo.crt
```

Then add this to your `src/system/settings/nginx.conf.tmpl`:
```
ssl_certificate       {{ settings.VENV_DIR }}/ssl_keys/demo.crt;
ssl_certificate_key   {{ settings.VENV_DIR }}/ssl_keys/server.key;
```

Lastly, add `HTTPS_ENABLED = True` to `src/system/settings/production.py` and regenerate the config files:
```
./m generate_configs
```
