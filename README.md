# Django Site Template #

Status: **Built with Django v1.10**




## Overview ##

This template was created to address the initial difficulty in transitioning a new project created with Django's `startproject` command into a project ready to deploy to a production server. Throughout this template and documentation, the project name is `djangotemplate`, and the domain name is the fictitious `djangotemplate.tech`. Change this for your project.

Note that this template has **only been tested on Python 3.4.x on a Debian-based system**. I have no plans to support Python 2.x or Windows, but if you find issues on other Linux distros, I'd be willing to adapt my template as needed.

The first commit of this repo was made immediately after running the following commands:

```
$> PROJECT=djangotemplate
$> mkdir $PROJECT && cd $PROJECT
$> virtualenv --python=python3 .venv && . .venv/bin/activate
$> pip install --upgrade pip
$> pip install django
$> django-admin startproject $PROJECT
$> cd $PROJECT && python manage.py startapp sampleapp && cd ..
```

This way, when Django updates to a new version, you can follow the same steps and compare the result to the first commit to see exactly what Django may have changed about their default project template.

From that first commit, the directory structure was changed to make things less confusing. By default, if you start a blank project, you'd end up with a directory tree like this:

* djangotemplate/ (your root directory)
  * .venv
  * djangotemplate/ (Django's root)
    * djangotemplate/ (the primary app)
      * settings.py
      * urls.py
      * wsgi.py
    * manage.py

With this template, I've named Django's root as `src` to distinguish it as the source-controlled portion of the files. For consistency across projects, I've also renamed Django's initial app to `system`. To reduce code duplication, I've split the settings file into three sub-files. Next, the `conf` directory was added for all the non-Django configuration, and the `data` directory was added for the database, log files, static and media files, etc. This results in the following directory tree:

* djangotemplate/ (your root directory)
  * .venv
  * conf
  * data
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
    * [deployment/maintenance scripts]

On top of that basic concept, I've added many tools to ease the deployment of a secure website. Yes, all of this is a matter of personal preference. Feel free to fork it.
* `src/m`: A bash script to run `src/manage.py` using the appropriate settings file (development, staging, production). It knows which one by checking the contents of `conf/whichenv.txt`.
* `src/fixattr`: A simple bash script to run `chmod +x` on any file that starts with a "shebang" (#!), as those file should be executable. I created this because file permissions get messed up by some text editors when editing your code on a remote Windows computer through a samba share.
* `src/devserver`: Just a shortcut to running `python src/manage.py runserver 0.0.0.0:9000 --settings system.settings.development`.
* `src/collectstatic`: Just a shortcut to running `python src/manage.py collectstatic` that will create symlinks instead of copies of your static files.
* `src/uwsgiserver`: Starts the uWSGI server. This is useful for testing if you don't have a systemd service set up yet, to start uWSGI at boot.
* `src/whichenv`: Used by the other scripts to read the contents of `conf/whichenv.txt`.

This project template has several of my own extensions installed as well:
* `src/m generateconfigs`: A custom Django management command to generate some config files from templates, allowing you to have slightly different configs for production and staging environments. Define which configs should be dynamically created by editing `conf/dynamic_configs.conf`.
* `src/m rotatesecretkey`: A custom Django management command to rotate the `SECRET_KEY` found in `conf/secret/secretkey.txt`. This allows you to keep your secret key out of source control.
* `src/m maintmode`: A custom Django management command to toggle maintenance mode on and off.

Throughout this documentation, I've used a `$PROJECT` variable to refer to your project name (`djangotemplate` in this case) as much as possible to make it easy for you to copy and paste these commands right into your terminal after adjusting `$PROJECT` to your own project name.




## How to Use ##

This template is designed to be used within a Python [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) (venv) to keep everything self-contained. It is recommended that the virtual environment's root is also your git repo's root, with a `.gitignore` configured to exclude the `bin`, `lib`, and `include` directories. Keep any sensitive information (keys, passwords) in their own files that can be excluded from the repo.




### Initial Setup of Development Environment ###

The development environment obviously has some unique characteristics, compared with the production/staging environments, to make things easy to work with:
* Run the server with `src/devserver`. This will launch Django's internal server which hosts both your application and all static files.
* Reload the server by hitting Ctrl+C and re-running `src/devserver`, but this rarely will be necessary since Django monitors source files for changes and reloads within seconds of seeing any.
* Static content is served by Django itself, so no need to call `src/collectstatic`.
* Uses SQLite to store data in `development.sqlite3`.
* DEBUG is True by default.
* Access at `http://<IP>:9000/`.
* Has no SSL version of the site.
* Django's server will show any runtime errors in the console rather than logging them to a file.
* Outgoing emails will be saved to `data/emails` instead of actually being sent.

First, create a new directory for your virtual environment and `cd` inside it:
```
$> PROJECT=djangotemplate
$> mkdir $PROJECT-dev && cd $PROJECT-dev
```

Then copy this template in without the commit history (since you'll be starting your own repo anyway):
```
$> git clone --depth=1 https://github.com/securedirective/django-site-template.git ./
$> rm -rf .git
```

Initialize the venv:
```
$> virtualenv --python=python3 .venv && . .venv/bin/activate
$> pip install --upgrade pip
```

Some of the packages listed in `requirements.txt` aren't hosted on [PyPi](https://pypi.python.org/pypi) yet, so you'll have to download these yourself:
```
$> mkdir custom-packages
$> git clone https://github.com/securedirective/django-generate-dynamic-configs.git custom-packages/django-generate-dynamic-configs
$> git clone https://github.com/securedirective/django-maint-mode-toggle.git custom-packages/django-maint-mode-toggle
$> git clone https://github.com/securedirective/django-rotate-secret-key.git custom-packages/django-rotate-secret-key
```

Now you can install them all into the virtual environment:
```
$> pip install -r requirements.txt
```

Since the deployment scripts use `conf/whichenv.txt` to determine which environment is in use, initialize that file now:
```
$> echo -n 'development' > conf/whichenv.txt
```

Initialize the database:
```
$> src/m migrate
```

Note: As of Django 1.10.3, ALLOWED_HOSTS is required even when DEBUG=True. This will cause Django to refuse the connection (DisallowedHost error) unless tho domain name requested is contained in the ALLOWED_HOSTS list. Use your `hosts` file or modify the ALLOWED_HOSTS setting as needed for your development environment.

At this point, you should be able to run Django's internal development server using another useful shortcut script.
```
$> src/devserver
```

If you load `http://localhost:9000`, the sample home page should show that you are using the 'development' settings file, and the next line should be green since Django is serving the static content itself. That's it!




### Port Tunneling ###

If you aren't doing your development on your local machine, there is still a relatively easy way to access the development server without exposing it to the internet. [PuTTY](http://www.putty.org/) and [KiTTY](http://kitty.9bis.net/) both have a port tunneling feature that forwards all requests sent to **your** `127.0.0.1:<port>` to the **remote server's** `127.0.0.1:<port>` as if you were on the remote server accessing it there.

To use this with PuTTY or KiTTY, fill out the usual host and port, but before connecting, go into the *Connection > SSH > Tunnels* section of the profile and add `L9000 127.0.0.1:9000`. Now, as long as you have the console window open and logged in, the tunnel will be enabled.




### Adapt to Your Project ###

This template starts in a working state, with a home page showing if static files are being served and a sample application that shows if URLs are being generated properly at runtime.

But you'll probably want to change our `djangotemplate` project name to one more applicable to your own project:
```
$> grep -RIn -e djangotemplate --exclude=*.md --exclude-from=.gitignore
```

Also remove `.gitignore` and put `.gitignore.yours` in its place:
```
$> mv .gitignore.yours .gitignore
```

If you'd like to remove the `sampleapp` as well, before creating your first commit, do this:
```
$> rm -rf src/sampleapp
$> grep -RIl -e sampleapp --exclude=*.md --exclude-dir=.git --exclude-from=.gitignore | xargs -d '\n' sed -i '/sampleapp/d'
```

At this point, you should commit these changes before you go any further:
```
$> git init
$> git add -A
$> git commit -m "Initial commit, based on django-site-template"
```

If you use Github for your source control, you'll probably want to add/change your remote link and push your changes to the server:
```
$> git remote add origin https://github.com/<your_repo>.git
$> git push --set-upstream origin master
```




### Production/Staging ###

The production/staging environments are configured differently from the development environment:
* Start the website using systemd: `systemctl start $PROJECT-staging` or `systemctl start $PROJECT-production`.
* Reload the server by modifying the modifying the reload file: `touch data/uwsgi.reload`.
* Static and user-uploaded media are served by nginx instead of Django.
* Databases are configured separately (`production.sqlite3` and `staging.sqlite3` by default), so it's easy to test things out on a copy of the live website that you can totally trash if needed. This also allows you to use a separate DBMS and still use SQLite for the development environment.
* DEBUG is False.
* Access the production site at `http://<domain>:80/` and the staging site at `http://<domain>:81/`. You can use iptables as needed to restrict access to this site to only active developers.
* Access the secure version of the production site at `http://<domain>:443/` and the staging site at `http://<domain>:444/`.
* Any errors from the systemd service or the uWSGI server will go to the systemd journal (`journalctl -u $PROJECT-staging`). Any errors from Django itself will output through nginx (`/var/log/nginx/$PROJECT-staging-error.log`).

The production and staging sites are as identical to each other as they can be. The custom `src/m generateconfigs` command will dynamically create the configs in each environment as needed for this, so you don't have to do it manually. The result should only differ in the following ways:
* Some files, such as the nginx config, require absolute paths and must be changed to point to the venv in use.
* Port numbers differ slightly so the same domain name can be used.
* The systemd service files for production and staging cannot have the same name, even if they are in different directories. Because systemd uses the symlink target's name as the internal service name, systemd will see them as the same service and won't let both run at the same time.

Now, to actually setup your staging environment...

Create a new staging environment and initialize it like you did with the development environment. But clone your own repo, of course, instead of the template:
```
$> PROJECT=djangotemplate
$> mkdir $PROJECT-staging && cd $PROJECT-staging
$> git clone <div_environment> ./
```

Continue on with the same commands for the venv initialization and package installation, but specify a different environment in use:
```
$> echo -n 'staging' > conf/whichenv.txt
```

Create a new random secret key:
```
$> src/m rotatesecretkey
```

Initialize the database:
```
$> src/m migrate
```

Initialize any config files that must be dynamically created:
```
$> src/m generateconfigs
```

Run Django's deployment check. It may complain about things that the `ssl.conf` will take care of, so take it with a grain of salt:
```
$> src/m check --deploy
```

Collect static files from your various apps and packages into one directory for nginx to server from:
```
$> src/collectstatic
```

Run the uWSGI server:
```
$> tail -f data/uwsgi.log &
$> src/uwsgiserver &
```

It is up to you to copy/symlink `conf/generated/nginx.conf` in and start the uwsgi server using systemd or a similar launcher. This procedure can vary widely, so is not covered in these instructions.
