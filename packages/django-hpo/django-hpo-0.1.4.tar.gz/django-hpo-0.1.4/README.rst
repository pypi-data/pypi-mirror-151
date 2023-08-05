===============
DJANGO HPO
===============

Alpha: DO NOT USE IN PRODUCTION
HPO is a Django app that allows to browse HPO Onthology https://hpo.jax.org/app/

Quick start
-----------

1. Add "hpo" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'hpo',
    ]

2. Run ``python manage.py migrate`` to create the models.

3. Run ``python manage.py import_hpo`` to populate your database.
