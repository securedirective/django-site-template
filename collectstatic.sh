#!/bin/bash

# Change to venv directory
dir=$(dirname $0)
cd $dir

# Activate venv if not already
if [ "$VIRTUAL_ENV" = "" ]; then
	source bin/activate
	echo "Activated virtual environment $dir"
fi

# Collect all static files into the main collected_static directory
r="python src/manage.py collectstatic -c -l"
echo "$r ..."; $r
