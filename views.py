from django.http import HttpResponse, Http404
#from django.template.loader import  get_template
#from django.template import Context
from django.shortcuts import render_to_response
import datetime

import routemaster.functions

# pseudocode

#def doit(request):

#    gather variables:
#        max distance of any 1 leg (default: 0 = no distance)
#        # of checkpoints to use in race
#        max total distance
        # of teams racing
        # of people per team

#        for each checkpoint:
#            name
#            addy
#            capacity
#
#
#
#

def hello(request):
    return HttpResponse("Hello world")

def homepage(request):
    return HttpResponse("Homepage")


def current_datetime(request):
    now = datetime.datetime.now()
    #t = get_template('current_datetime.html')
    #html = t.render(Context({'current_date': now}))
    #return HttpResponse(html)
    return render_to_response('current_datetime.html', {'current_date': now})


def hours_ahead(request, offset):
#    try:
#        offset = int(offset)
#    except ValueError:
#        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

#
#def delete(self):
#    # Delete the account
#
#delete.alters_data = True
