# Giant-FAQs

A small reusable package that adds a 'Frequently Asked Questions' app to a django site.

This will include the basic formatting and functionality such as model creation via the admin.

Supported Django versions:

    Django 2.2, 3.2

Supported django CMS versions:

    django CMS 3.8, 3.9

## Installation and set up

In the INSTALLED_APPS of your settings file add "giant_faqs" and below "cms" ensure "easy_thumbnails" is present. For use of the RichText plugin needed for the answer entry field on the model, it is required that you use the giant-plugins app.

There is an optional search bar which can be removed from the top of the index template by adding 
    
    FAQ_SEARCH = False

to your project's settings.

## Sitemap

In order to add published articles to your sitemap, import the sitemaps file and add it to your sitemaps dict. This is usually contained within the main urls.py file.

## URLs

It is recommended that the application be added to a CMS page via the apphook. However, if you wish to hardcode the URL, you can do so by adding the following to your main urls.py file:


    path("faqs/", include("giant_faqs.urls"), name="faqs"),

If you want to customize the urls to include a different path and/or templates, first you must import from giant_faqs import views as faqs_views in core.urls and then you could add the following:

    path("faqs/", faqs_views.FAQIndex.as_view(template_name="faqs/index.html"), name="index"),



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

