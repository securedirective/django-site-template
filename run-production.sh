#!/bin/bash

# Change to venv directory
dir=$(dirname $0)
cd $dir

# Activate venv if not already
if [ "$VIRTUAL_ENV" = "" ]; then
	source bin/activate
	echo "Activated virtual environment $dir"
fi

# Run the uWSGI server
r="uwsgi --ini uwsgi.ini"
echo "$r ..."; $r
