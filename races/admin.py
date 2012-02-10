from races.models import Checkpoint, RouteLeg, Route, Node, Race
from django.contrib import admin


class RouteInline(admin.TabularInline):
    model = Route
    extra = 3

class NodeInline(admin.TabularInline):
    model = Node
    extra = 3

class RaceAdmin(admin.ModelAdmin):
    inlines = [RouteInline]

class RouteAdmin(admin.ModelAdmin):
    inlines = [NodeInline]

admin.site.register(Checkpoint)
admin.site.register(RouteLeg)
admin.site.register(Route, RouteAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Node)
