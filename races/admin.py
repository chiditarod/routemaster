from races.models import Checkpoint, RouteLeg, Route, RouteLegNode, Race
from django.contrib import admin



class RouteLegNodeInline(admin.TabularInline):
    model = RouteLegNode
    extra = 3

class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteLegNodeInline]

#class RouteInline(admin.TabularInline):
#    model = Route
#    extra = 3

#class RaceAdmin(admin.ModelAdmin):
#    inlines = [RouteInline]


admin.site.register(Checkpoint)
admin.site.register(RouteLegNode)
admin.site.register(RouteLeg)
admin.site.register(Route, RouteAdmin)
#admin.site.register(Route)

admin.site.register(Race)
