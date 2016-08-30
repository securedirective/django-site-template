#!/bin/bash

# Change to venv directory
dir=$(dirname $0)
cd $dir

# Activate venv if not already
if [ "$VIRTUAL_ENV" = "" ]; then
	source bin/activate
	echo "Activated virtual environment $dir"
fi

# Run the development server
# Unless --nostatic is specified, static files will be served as well
r="python src/manage.py runserver 0.0.0.0:8000 --settings system.settings.development"
echo "$r ..."; $r
