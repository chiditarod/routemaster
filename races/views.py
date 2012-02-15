from django.template import Context, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response


from races.models import Race
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
    except Exception, e:
        raise e
