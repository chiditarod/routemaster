
# Routemaster
Route generator software for Chiditarod.
It mostly works. This code is like an old couch. When you sit
down, at first it's kind of old and dusty. But it serves it's purpose.
Basically it is a traveling salesman solver.  There is a starting line, a
finish line, and a configurable amount of checkpoints in-between. You
first add the various checkpoints, add the distances between them all, set a few params like # of teams,
the # of checkpoints, etc, then hit go, and it figures out the best routes.

The codebase is written in [Python](https://www.python.org/), and it uses an old version of the [Django](https://www.djangoproject.com/) web framework.

## To Install
Read [INSTALL.md](https://github.com/chiditarod/routemaster/blob/master/INSTALL.md)

## Usage

1. Activate the python virtual environment

        cd path/to/routemaster/repo
        . ~/.python/Virtualenvs/routemaster/bin/activate 

1. Run Locally

        python manage.py runserver

1. Visit URLs

    - http://localhost:8000/admin     - Configure the races, checkpoints, etc
    - http://localhost:8000/races     - Run the calculations

## TODO
Rewrite this in something fun.

## etc

### How to install a new pip module

    $ bin/pip-install

### Run Local Django Console
```bash
cd path/to/routemaster
python manage.py shell
```

#### print settings
```python
from django.conf import settings
print settings.<tab>
```

### Users
devin / mush
