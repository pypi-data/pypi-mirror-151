keyterms plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ to easily add the key terms api to an Open edX platform.

Installation
------------

::

    pip install tutor-keyterms-api


Usage
-----

::

    tutor plugins enable keyterms

Pull the latest image for edx_key_terms_api, run::

    tutor images pull keyterms

To create the keyterms container, run::

    tutor local start

Initialize the service, create the database and run migrations, run::

    tutor local init --limit=keyterms


Configuration
-------------

- ``KEYTERMS_DOCKER_REGISTRY`` (default: ``"589371489025.dkr.ecr.us-east-2.amazonaws.com/"``)
- ``KEYTERMS_DOCKER_IMAGE`` (default: ``"{{ KEYTERMS_DOCKER_REGISTRY }}edx_key_terms_api:{{ KEYTERMS_VERSION }}"``)
- ``KEYTERMS_HOST`` (default: ``"keyterms.{{ LMS_HOST }}"``)
- ``KEYTERMS_MYSQL_DATABASE`` (default: ``"keyterms"``)
- ``KEYTERMS_MYSQL_USERNAME`` (default: ``"keyterms"``)

These values can be modified with ``tutor config save --set PARAM_NAME=VALUE`` commands.