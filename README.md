
h3. To activate your virtualenv environment

$ cd path/to/routemaster/repo
$ . ~/.python/Virtualenvs/routemaster/bin/activate 

h3. Run Dev Server

$ cd path/to/routemaster
Activate the virtualenv environment
$ python manage.py runserver

h3. Useful URLs

http://localhost:8000/admin     - Configure the races, checkpoints, etc
http://localhost:8000/races     - Run the calculations

h3. Run Local Django Console

$ cd path/to/routemaster
Activate the virtualenv environment
$ python manage.py shell
>>> from django.conf import settings
>>> print settings.<tab>

h3. Users
devin / mush




