
# Routemaster
Route generator software for Chiditarod.
It mostly works.


# To Install
Read [INSTALL.md](https://bitbucket.org/ometa/routemaster/src/tip/INSTALL.md)



# Helpful things
### Useful URLs
- http://localhost:8000/admin     - Configure the races, checkpoints, etc
- http://localhost:8000/races     - Run the calculations

### To activate your virtualenv environment

    $ cd path/to/routemaster/repo
    $ . ~/.python/Virtualenvs/routemaster/bin/activate 

### How to install a new pip module

    $ bin/pip-install

### Run Dev Server

    $ cd path/to/routemaster
Activate the virtualenv environment
    $ python manage.py runserver

### Run Local Django Console

    $ cd path/to/routemaster
Activate the virtualenv environment
    $ python manage.py shell
    >>> from django.conf import settings
    >>> print settings.<tab>

### Users
devin / mush




