#!/bin/sh
# run the example application in uwsgi + pypy
~/opt/pypy3/bin/pip install -r requirements.txt
authbind --deep ~/opt/uwsgi/uwsgi uwsgi.ini --touch-reload=app.py