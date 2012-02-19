from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.core.exceptions import ObjectDoesNotExist

from races.models import Race, Route
# TODO: move this into the race app
from ometa import RaceBuilder

# consult:
# https://docs.djangoproject.com/en/dev/intro/tutorial03/#philosophy

def build_race(request, race_id):
    r = RaceBuilder()
    (race, output) = r.buildRoutesForRace(race_id)
    return output

def index(request):
    return HttpResponse("Index Page")

def list_races(request):
    race_list = Race.objects.all()
    t = loader.get_template('races/index.html')
    c = Context({
        'race_list': race_list,
    })
    return HttpResponse(t.render(c))
    # shortcut: return render_to_response('races/index.html', {'race_list': race_list})


def race_detail(request, race_id):
    error = None
    try:
        race = Race.objects.get(id=race_id)
        if not race:
            error = 'notfound'
            return render_to_response('races/race_detail.html', {'error': error, 'race_id': race_id})
        else:
            return render_to_response('races/race_detail.html', {'race': race})
    except DoesNotExist, e:
        error = 'notfound'
        return render_to_response('races/race_detail.html', {'error': error, 'race_id': race_id})
    except Exception, e:
        raise e

def add_route_capacity(request, route_id):
    """Calculate the capacity of a single route.  Slated for removal."""
    route = Route.objects.get(id=route_id)
    r = RaceBuilder()
    return HttpResponse(r.addCapacityToRoute(route))
    

def add_route_capacities(request, race_id):
    """Calculate capacities for all routes in a race."""
    race = Race.objects.get(id=race_id)
    if race.routes is None:
        error = 'no-routes'
        return render_to_response('races/add_route_capacities.html', {'error': error, 'race_id': race_id})
    
    r = RaceBuilder()
    count = r.addRouteCapacities(race)
    return render_to_response('races/add_route_capacities.html', {'count': count, 'race': race})


def find_unique_routes(request, race_id):
    """Find all unique routes that don't overlap checkpoint/positions"""
    race = Race.objects.get(id=race_id)
    if race.routes is None:
        error = 'no-routes'
        return render_to_response('races/find_unique_routes.html', {'error': error, 'race_id': race_id})
    
    r = RaceBuilder()
    used_routes, deferred_routes = r.findUniqueRoutes(race)
    return render_to_response('races/find_unique_routes.html', {'used_routes': used_routes, 'deferred_routes': deferred_routes, 'race': race})

