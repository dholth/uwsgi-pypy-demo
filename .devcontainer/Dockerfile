FROM python:3.9-buster
LABEL maintainer="Daniel Holth <dholth@gmail.com>"
ARG pypy=pypy3.7-v7.3.3-linux64.tar.bz2
ARG venv=/home/vscode/opt/pypy3
ARG user=vscode

RUN useradd -s /bin/bash -m $user

# allow user to use port 80, 443
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install --no-install-recommends authbind
RUN touch /etc/authbind/byport/80 /etc/authbind/byport/443 && \
    chown ${user} /etc/authbind/byport/* && \
    chmod u+x /etc/authbind/byport/*

# used by ASGI chat demo
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install redis

USER $user
WORKDIR /home/${user}/opt

RUN curl https://bootstrap.pypa.io/virtualenv.pyz -o virtualenv.pyz
RUN curl -SL https://downloads.python.org/pypy/${pypy} | tar -jx
RUN python virtualenv.pyz -p pypy*/bin/pypy3 ${venv}
RUN git clone https://github.com/dholth/uwsgi
RUN cd uwsgi && \
    . ${venv}/bin/activate && \
    make PROFILE=nolang && \
    python uwsgiconfig.py -p plugins/cffi nolang

EXPOSE 80
EXPOSE 443