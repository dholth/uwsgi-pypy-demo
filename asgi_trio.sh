#!/bin/sh
redis-server &

. ~/opt/pypy3/bin/activate
pip install starlette trio trio-asyncio asyncio-redis
cd ~/opt/uwsgi
./plugins/cffi/triotest.sh