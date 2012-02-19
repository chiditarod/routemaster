from races.models import Checkpoint, RouteLeg, Route, RouteLegNode, Race
from django.contrib import admin



class RouteLegNodeInline(admin.TabularInline):
    model = RouteLegNode
    extra = 3
    list_per_page = 500
    
class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteLegNodeInline]
    list_per_page = 500

class RouteLegAdmin(admin.ModelAdmin):
    list_per_page = 500
    list_display = ('checkpoint_a', 'checkpoint_b', 'distance')
    list_filter = ('checkpoint_a', 'checkpoint_b', 'distance')

class RouteInline(admin.TabularInline):
    model = Route
    extra = 2
    list_per_page = 200
    
class RaceAdmin(admin.ModelAdmin):
    inlines = [RouteInline]
    
#class RouteInline(admin.TabularInline):
#    model = Route
#    extra = 3

#class RaceAdmin(admin.ModelAdmin):
#    inlines = [RouteInline]


admin.site.register(Checkpoint)
admin.site.register(RouteLegNode)
admin.site.register(RouteLeg, RouteLegAdmin)
admin.site.register(Route, RouteAdmin)
#admin.site.register(Route)

admin.site.register(Race, RaceAdmin)
