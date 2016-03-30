
# Installation

Tested exclusively on OSX. That's just how we roll.  If you get this to work with Windows, please share the process with us by [opening an issue](https://github.com/chiditarod/routemaster/issues/new)!

    $ brew install python --with-brewed-openssl
    $ PIP_REQUIRE_VIRTUALENV=false pip install virtualenv
    $ mkdir -p ~/.python/Virtualenvs
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
    $ cd path/to/routemaster/repo
    $ . ~/.python/Virtualenvs/routemaster/bin/activate
    $ pip install -r Pipfile
    $ python manage.py runserver

### BOOSH.

gleaned from [hackercodex](http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/)

