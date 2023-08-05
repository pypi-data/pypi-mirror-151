# giant-social-links

A small reuseable django app that allows social media links to be added via the admin page of your django site.

This will include the basic formatting and functionality such as model creation via the admin.

Supported Django versions:

    Django 2.2, 3.2

Supported django CMS versions:

    django CMS 3.8, 3.9

## Installation and set up

In the INSTALLED_APPS of your settings file add "giant_social_links" and below "cms" ensure "easy_thumbnails" and "filer" are present. It is also required that you use the giant-plugins & giant-mixins apps.

A context processor is given by default so your Social links can be accessed anywhere on the site by rendering the template variable:

    {{ social_media_links }}

Which will only show the enabled links. Feel free to override this with a custom context processor.

# Local development
## Getting setup

To get started with local development of this library, you will need access to poetry (or another venv manager). You can set up a virtual environment with poetry by running:

    $ poetry shell

Note: You can update which version of python poetry will use for the virtualenv by using:

    $ poetry env use 3.x

and install all the required dependencies (seen in the pyproject.toml file) with:

    $ poetry install

## Management commands

As the library does not come with a manage.py file we need to use django-admin instead. However, we will need to set our DJANGO_SETTINGS_MODULE file in the environment. You can do this with:

    $ export DJANGO_SETTINGS_MODULE=settings

From here you can run all the standard Django management commands such as django-admin makemigrations.
Testing

This library uses Pytest in order to run its tests. You can do this (inside the shell) by running:

    $ pytest -v

where -v is to run in verbose mode which, while not necessary, will show which tests errored/failed/passed a bit more clearly.
Preparing for release

In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the pyproject.toml. This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.
# Publishing

Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.

    $ `poetry build`

will package the project up for you into a way that can be published.

    $ `poetry publish`

will publish the package to PyPi. You will need to enter the company username (Giant-Digital) and password for the account which can be found in the company password manager
