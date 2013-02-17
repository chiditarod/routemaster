
.h3 Installation
(from: http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/)

$ brew install python --with-brewed-openssl
$ pip install virtualenv
$ mkdir ~/.python/Virtualenvs
$ vim ~/.bashrc # add the lines below.

  # virtualenv should use Distribute instead of legacy setuptools
  export VIRTUALENV_DISTRIBUTE=true
  # Centralized location for new virtual environments
  export PIP_VIRTUALENV_BASE=$HOME/.python/Virtualenvs
  # pip should only run if there is a virtualenv currently activated
  export PIP_REQUIRE_VIRTUALENV=true
  # cache pip-installed packages to avoid re-downloading
  export PIP_DOWNLOAD_CACHE=$HOME/.pip/cache

$ cd ~/.python/Virtualenvs
$ virtualenv routemaster
$ cd routemaster
$ . bin/activate
$ cd path/to/routemaster/repo
$ pip install -r Pipfile
$ python manage.py runserver

BOOSH.

