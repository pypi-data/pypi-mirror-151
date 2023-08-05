FROM ubuntu:focal as app
MAINTAINER sre@edx.org


# Packages installed:

# language-pack-en locales; ubuntu locale support so that system utilities have a consistent
# language and time zone.

# python; ubuntu doesnt ship with python, so this is the python we will use to run the application

# python3-pip; install pip to install application requirements.txt files

# libmysqlclient-dev; to install header files needed to use native C implementation for
# MySQL-python for performance gains.

# libssl-dev; # mysqlclient wont install without this.

# python3-dev; to install header files for python extensions; much wheel-building depends on this

# gcc; for compiling python extensions distributed with python packages like mysql-client

# If you add a package here please include a comment above describing what it is used for
# RUN apk update && apk add git

RUN apt-get update && apt-get -qy install --no-install-recommends \
 language-pack-en \
 locales \
 python3.8 \
 python3-pip \
 python3.8-venv \
 libmysqlclient-dev \
 libssl-dev \
 python3-dev \
 gcc \ 
 make \
 git

# delete apt package lists because we do not need them inflating our image
RUN rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

ARG APP_USER_ID=1000
RUN useradd --home-dir /app --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

ARG TOKEN
# RUN git config --global url."https://${TOKEN}:@github.com/".insteadOf "https://github.com/"

RUN mkdir /app/edx_key_terms_api
RUN git clone https://${TOKEN}:@github.com/cucwd/edx_key_terms_api --branch {{ CUCWD_CURRENT_RELEASE }} --depth 1 /app/edx_key_terms_api
WORKDIR /app/edx_key_terms_api

RUN python -m venv /app/venv
ENV PATH /app/venv/bin:${PATH}
RUN pip install setuptools==44.1.0 pip==20.3.4 wheel==0.37.0
RUN pip install -r requirements/production.txt

EXPOSE 18500
# RUN useradd -m --shell /bin/false app

# WORKDIR /edx/app/edx_key_terms_api

# Copy the requirements explicitly even though we copy everything below
# this prevents the image cache from busting unless the dependencies have changed.
# COPY requirements/production.txt /edx/app/edx_key_terms_api/requirements/production.txt

# Dependencies are installed as root so they cannot be modified by the application user.
# RUN pip install -r requirements/production.txt

# RUN mkdir -p /edx/var/log

# Code is owned by root so it cannot be modified by the application user.
# So we copy it before changing users.
# USER app

# Gunicorn 19 does not log to stdout or stderr by default. Once we are past gunicorn 19, the logging to STDOUT need not be specified.
CMD gunicorn --workers=2 --name edx_key_terms_api -c /edx/app/edx_key_terms_api/edx_key_terms_api/docker_gunicorn_configuration.py --log-file - --max-requests=1000 edx_key_terms_api.wsgi:application

# This line is after the requirements so that changes to the code will not
# bust the image cache
# COPY . /edx/app/edx_key_terms_api

# FROM app as newrelic
# RUN pip install newrelic
# CMD newrelic-admin run-program gunicorn --workers=2 --name edx_key_terms_api -c /edx/app/edx_key_terms_api/edx_key_terms_api/docker_gunicorn_configuration.py --log-file - --max-requests=1000 edx_key_terms_api.wsgi:application
