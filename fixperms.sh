#!/bin/bash

if [[ $EUID -ne 0 ]]; then
	echo "This script should be run as root" 1>&2
fi

dir="$(dirname $0)"
echo "Setting all files under $dir to www-data:www-data..."
chown -v -R www-data:www-data "$dir" | grep -v retained

echo "Verifying executable scripts have +x..."
chmod +x $dir/fixperms.sh
chmod +x $dir/rundevserver.sh
chmod +x $dir/*/manage.py

exit 0
