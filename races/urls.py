from django.conf.urls.defaults import *

#from views import *
#from races.views import *

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('races.views',
    (r'^$', 'list_races'),
    (r'^(\d+)/?$', 'race_detail'),
    (r'^build/(\d+)/?$', 'build_race'),
    (r'^add-route-capacity/(\d+)/?$', 'add_route_capacity'),
    (r'^add-route-capacities/(\d+)/?$', 'add_route_capacities'),
    (r'^find-unique-routes/(\d+)/?(\d+)?/?$', 'find_unique_routes'),
    (r'^delete-routes-in-race/(\d+)/?$', 'delete_routes_in_race'),
    (r'^rarity-tree/(\d+)/?$', 'rarity_tree'),
)