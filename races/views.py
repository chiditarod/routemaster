from django.template import Context, loader
from django.http import HttpResponse
from races.models import Race

from ometa import RaceBuilder

# consult:
# https://docs.djangoproject.com/en/dev/intro/tutorial03/#philosophy

def build_race(request):
    r = RaceBuilder()
    (race, output) = r.mungeRace("Chiditarod VII")
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

