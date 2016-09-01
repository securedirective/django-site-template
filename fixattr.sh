#!/bin/bash

dir="$(dirname $0)"
echo "Verifying executable scripts have +x..."
chmod +x $dir/*.sh
chmod +x $dir/confgen.py
chmod +x $dir/*/manage.py

exit 0
