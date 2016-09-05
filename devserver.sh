#!/bin/bash

venv=$(dirname $0)
# Unless --nostatic is specified, static files will be served as well
$venv/bin/python $venv/src/manage.py runserver 0.0.0.0:8000 --settings system.settings.development
