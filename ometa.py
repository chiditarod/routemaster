"""
ometa.py

Created by Devin Breen on 2012-02-08.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

#from django.http import HttpResponse, Http404
#from django.template.loader import  get_template
#from django.template import Context
#from django.shortcuts import render_to_response
#import datetime

from races.models import RouteLeg, Race, Checkpoint, RouteLegNode, Route

class RaceBuilder(object):
    """Primary class for building a race"""
#    def __init__(self, arg):
#        super(RaceBuilder, self).__init__()
#        self.arg = arg
        
    def buildRace(self, race):
        """main function to build an entire race, given a start and finish point."""
    
        # start building routes using each potential routeleg
        print 'building race for %s.  finding all checkpoints starting at %s' % (race.name, race.checkpoint_start)
        potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name)  

        print 'found %i potential legs' % len(potential_legs)
        
        for routeleg in potential_legs:
            route = self.buildRoute(race, routeleg)
            if route:
                race.routes.append(route)


    def buildRoute(self, race, routeleg, route = None):
        """docstring for buildRoute"""    
        # ------------------------------------------
        # checks of a bad routeleg:
    
        print 'buildRoute: %s' % routeleg
    
        # routeleg distance > max_leg_distance
        if (routeleg.distance > race.max_leg_distance):
            print "%d length > max leg distance %s" % (routeleg.distance, race.max_leg_distance)
            return None
                
        # additional operations if this route already has at least one routeleg
        if route:
            print 'route exists'
            
            # if adding routeleg makes the total distance too far
            if route.distanceThusFar + routeleg.distance > race.max_race_distance:
                print "%s will make race > max race distance %d" % (routeleg, race.max_race_distance)
                return None
            
            # checkpoint_b = finish, and numcheckpoints+1 != total
            if (routeleg.checkpoint_b == race.checkpoint_finish) and (route.routelegs.count() + 1 != race.checkpoint_qty):
                print '%s is the finish line, but there is only %i checkpoints so far in this route.' % (routeleg.checkpoint_b.name, len(route.routelegs))
                return None
        
            # checkpoint_b already used
            for r in route.routelegs:
                print '%s is already in use in this route.' % routeleg.checkpoint_b.name
                if r.checkpoint_b is routeleg.checkpoint_b:
                    return None
        else:
            # instantiate a new route
            route = Route()
            route.name = 'Route %s' % (race.routes.count() + 1)
            route.checkpoint_start = race.checkpoint_start
            route.checkpoint_finish = race.checkpoint_finish
            route.valid = False
            print 'building new route: %s' % route.name
            route.save()
            
        # ---------------------------------------------
        # all tests pass. what next?

        # add this routeleg to our route
        print 'appending routeleg %s onto our route' % routeleg
        
        route.routelegs.add(routeleg)

        # get all potential routelegs with our current checkpoint b as their checkpoint a
        print 'querying for all routelegs starting with %s' % routeleg.checkpoint_b.name
        potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % routeleg.checkpoint_b.name)  
    
        # loop through all potential routelegs.  If we get back a route, then return it.
        for r in potential_legs:
            print 'trying to build route for %s' % r.name
            route = self.buildRoute(race, r, route)
            if route is not None:
                return route
