#from django.http import HttpResponse, Http404
#from django.template.loader import  get_template
#from django.template import Context
#from django.shortcuts import render_to_response
#import datetime

from races.models import RouteLeg, Race, Checkpoint, Node, Route

startCheckpoint = Checkpoint.objects.get(name="Minimonk")
endCheckpoint = Checkpoint.objects.get(name="Bottom Lounge")

# TODO: This should be called somewhere else.
buildrace(startCheckpoint, endCheckpoint)

# main function to build an entire race, given a start and finish point.
def buildrace(start, finish):
    # instantiate a new race object
    race = Race()

    # TODO: abstract into config for each race
    numLegs = 5

    # start building routes using each potential routeleg
    potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % start.name)  
    for routeleg in potential_legs:
        # basic checks of a bad routeleg:

        # if the next checkpoint is the finish, but we don't have the full number of checkpoints in the route, fail
        if (routeleg.checkpoint_b = endCheckpoint) and (route.routelegs.count < race.max_checkpoints):
            # continue for loop
        # If checkpoint_b has already been used:
            # continue


        route = buildRoute(race, route, routeleg)
        if route:
            race.
 
def buildRoute(race, routeleg, route = null):
        totalDistance = routeleg.distance + route.
        
        # if this routeleg makes the total distance too far
        if sum of this route distance so far > race.max_race_distance:
            return None
        # if this routeleg is bigger than the programmed maximum leg distance
        if routeleg.distance > race.max_leg_distance:
            return None

        if routeleg.checkpoint_b =  and route.routelegs.count = race.max_checkpoints:
            return 


    for routeleg in (all routelegs with a = starting line)
        set order
        add routeleg to race
        Race = addRouteLeg(race)
    
    




