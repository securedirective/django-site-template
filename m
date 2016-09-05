#!/bin/bash

# Shortcut to running src/manage.py, using the appropriate settings file for the current virtual environment

# Get the virtual environment path, regardless of current directory
venv=$(realpath $(dirname $0))

# Make an educated guess of which settings file we should use
if [[ $venv == *"staging" ]] || [[ $venv == *"stag" ]]; then
	settings="system.settings.staging"
elif [[ $venv == *"development" ]] || [[ $venv == *"dev" ]]; then
	settings="system.settings.development"
else
	settings="system.settings.production"
fi

# Build a command string
cmd="$venv/bin/python $venv/src/manage.py $* --settings=$settings"
echo -e "\E[32mRunning the following command:\n$cmd\E[0m"
echo

# Run it
$cmd
