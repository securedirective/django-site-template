#!/bin/bash

cd $(dirname $0)
echo "Verifying executable scripts have +x..."
chmod +x m
chmod +x *.sh
chmod +x */manage.py
