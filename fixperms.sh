#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script should be run as root" 1>&2
fi

dir="$(dirname $0)"
echo "Verifying executable scripts have +x..."
chmod +x $dir/*.sh
chmod +x $dir/*/manage.py

exit 0
