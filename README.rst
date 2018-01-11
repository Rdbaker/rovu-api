===============================
Rovu API
===============================

Join friends and events.


Quickstart
----------

First, run the following commands to bootstrap your environment.


::

    git clone https://github.com/rdbaker/rovu
    cd rovu
    pip install -r requirements/dev.txt
    npm install
    npm run dev
    python manage.py server

You will see a pretty welcome screen.

Once you have installed PostgreSQL, run the following to create your app's database tables and perform the initial migration:

::

    createuser -s rovu -W  # enter rovu123 as the password
    createdb rovu
    createdb rovu_test
    python manage.py db upgrade
    python manage.py server



Deployment
----------

In your production environment, make sure the ``ROVU_ENV`` environment variable is set to ``"prod"``.


Shell
-----

To open the interactive shell, run ::

    python manage.py shell

By default, you will have access to ``app``, ``db``, and the ``models``.


Running Tests
-------------

To run all tests, run ::

    python manage.py test


Migrations
----------

Whenever a database migration needs to be made. Run the following command:
::

    python manage.py db migrate

This will generate a new migration script. Then run:
::

    python manage.py db upgrade

To apply the migration.

For a full migration command reference, run ``python manage.py db --help``.
