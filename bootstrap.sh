#!/bin/sh
`which python3` -m venv .
./bin/pip install -r requirements.txt
./bin/buildout $*
echo "run plone with: b5 plone"