#!/bin/bash

HOST="sumin@suminb.com"

# Delete .pyc files
rm -rf $(find . -name "*.pyc")

# Deploy files
rsync -azP -e ssh * $HOST:webapps/hallucination/repo

read -p "Restart the server? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
	echo "Restarting the server..."
	ssh $HOST 'webapps/hallucination/apache2/bin/restart'
fi
