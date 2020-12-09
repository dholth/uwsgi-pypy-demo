# uwsgi + cffi devcontainer

Demonstration of uwsgi + pypy + cffi plugin.

Visual Studio Code can automatically build and connect to a Docker container using the included `.devcontainer` folder. See https://code.visualstudio.com/docs/remote/containers

You could also build the container manually from `.devcontainer\Dockerfile`, and bind mount this directory into the container.

## After connecting to the container

Start app.

    ./uwsgi.sh

Visit http://localhost/ to see the Mandelbrot set.

Activate the pypy virtual environment if vscode hasn't done it automatically.
Otherwise, `$ python` will run CPython:

    . ~/opt/pypy3/bin/activate

## Edit the cffi plugin's source code

This plugin is almost entirely written in Python using the [cffi embedding interface](https://cffi.readthedocs.io/en/latest/embedding.html).

In the container, open a new VSCode window on the uwsgi folder:

    code ~vscode/opt/uwsgi

Look at the `plugins/cffi` folder. For example `plugins/cffi/cffi_init.py` defines the WSGI request handler (`def uwsgi_cffi_request(wsgi_req)`); `cffi_trio.py` and `cffi_asyncio.py` implement experimental [ASGI](https://asgi.readthedocs.io/en/latest/) handlers.

Recompile the plugin:

    ~/opt/pypy3/bin/python uwsgiconfig.py -p plugins/cffi nolang`

> **WARNING** Any changes you make to `~/opt/` will be lost if you rebuild or destroy the container.
