# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['giant_faqs', 'giant_faqs.migrations', 'giant_faqs.tests']

package_data = \
{'': ['*'],
 'giant_faqs': ['templates/*',
                'templates/faqs/*',
                'templates/faqs/_components/*']}

install_requires = \
['giant-mixins', 'giant-plugins']

setup_kwargs = {
    'name': 'giant-faqs',
    'version': '0.1.5',
    'description': 'A small reusable package that adds a FAQ app to a project',
    'long_description': '# Giant-FAQs\n\nA small reusable package that adds a \'Frequently Asked Questions\' app to a django site.\n\nThis will include the basic formatting and functionality such as model creation via the admin.\n\nSupported Django versions:\n\n    Django 2.2, 3.2\n\nSupported django CMS versions:\n\n    django CMS 3.8, 3.9\n\n## Installation and set up\n\nIn the INSTALLED_APPS of your settings file add "giant_faqs" and below "cms" ensure "easy_thumbnails" is present. For use of the RichText plugin needed for the answer entry field on the model, it is required that you use the giant-plugins app.\n\nThere is an optional search bar which can be removed from the top of the index template by adding \n    \n    FAQ_SEARCH = False\n\nto your project\'s settings.\n\n## Sitemap\n\nIn order to add published articles to your sitemap, import the sitemaps file and add it to your sitemaps dict. This is usually contained within the main urls.py file.\n\n## URLs\n\nIt is recommended that the application be added to a CMS page via the apphook. However, if you wish to hardcode the URL, you can do so by adding the following to your main urls.py file:\n\n\n    path("faqs/", include("giant_faqs.urls"), name="faqs"),\n\nIf you want to customize the urls to include a different path and/or templates, first you must import from giant_faqs import views as faqs_views in core.urls and then you could add the following:\n\n    path("faqs/", faqs_views.FAQIndex.as_view(template_name="faqs/index.html"), name="index"),\n\n\n\n# Local development\n## Getting setup\n\nTo get started with local development of this library, you will need access to poetry (or another venv manager). You can set up a virtual environment with poetry by running:\n\n    $ poetry shell\n\nNote: You can update which version of python poetry will use for the virtualenv by using:\n\n    $ poetry env use 3.x\n\nand install all the required dependencies (seen in the pyproject.toml file) with:\n\n    $ poetry install\n\n## Management commands\n\nAs the library does not come with a manage.py file we need to use django-admin instead. However, we will need to set our DJANGO_SETTINGS_MODULE file in the environment. You can do this with:\n\n    $ export DJANGO_SETTINGS_MODULE=settings\n\nFrom here you can run all the standard Django management commands such as django-admin makemigrations.\nTesting\n\nThis library uses Pytest in order to run its tests. You can do this (inside the shell) by running:\n\n    $ pytest -v\n\nwhere -v is to run in verbose mode which, while not necessary, will show which tests errored/failed/passed a bit more clearly.\nPreparing for release\n\nIn order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the pyproject.toml. This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.\n# Publishing\n\nPublishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.\n\n    $ `poetry build`\n\nwill package the project up for you into a way that can be published.\n\n    $ `poetry publish`\n\nwill publish the package to PyPi. You will need to enter the company username (Giant-Digital) and password for the account which can be found in the company password manager\n\n',
    'author': 'Domchap90',
    'author_email': 'dominic.chaple@giantdigital.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/giantmade/giant-faqs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
