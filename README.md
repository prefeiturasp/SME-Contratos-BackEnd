[![Maintainability](https://api.codeclimate.com/v1/badges/ad33daa97c71f74ad579/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Contratos-BackEnd/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/ad33daa97c71f74ad579/test_coverage)](https://codeclimate.com/github/prefeiturasp/SME-Contratos-BackEnd/test_coverage)

# SME-Contratos-BackEnd

SME COAD
========

Sistema de gestão da COORDENADORIA DE ADMINISTRAÇÃO, FINANÇAS E INFRAESTRUTURA - COAD.

License: MIT


Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy sme_coad_apps

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html





Deployment
----------

The following details how to deploy this application.
