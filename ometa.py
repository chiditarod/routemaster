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

def getRouteLength(route):
	total = 0
	for r in route.routelegnode_set.all():
		total += r.routeleg.distance
	return total


class RaceBuilder(object):

    def buildRace(self, raceName):
        """main function to build an entire race, given a start and finish point."""
        
        race = Race.objects.get(name=raceName)
        
        # start building routes using each potential routeleg
#        print 'building race for %s.  finding all checkpoints starting at %s' % (race.name, race.checkpoint_start.name)
        potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name)  

        print 'found %i potential legs' % len(potential_legs)
        
        for routeleg in potential_legs:
            routes = self.buildRoutes(race, routeleg)
        for r in routes:
            race.routes.append(r)


    def buildRoutes(self, race, routeleg, route = None):
        """docstring for buildRoutes"""    
        print 'buildRoutes: %s' % routeleg

        # ------------------------------------------
        # checks for an inappropriate routeleg:
        
        # routeleg distance > max_leg_distance
        if (routeleg.distance > race.max_leg_distance):
            print "\tFAIL: %s length > max leg distance %s" % (routeleg.distance, race.max_leg_distance)
            return None
        else:
            print "\tPASS: %s length <= max leg distance %s" % (routeleg.distance, race.max_leg_distance)
                
        # additional operations if this route already has at least one routeleg
        if route:
            print 'route exists. depth: %s' % route.routelegs.count()
            
            # checkpoint_b can't be the starting line
            print "%s, %s" % (routeleg.checkpoint_b, race.checkpoint_start)
            if (routeleg.checkpoint_b == race.checkpoint_start):
                print '\tFAIL: %s is the starting line, that cannot be.' % routeleg.checkpoint_b.name
                return None
            
            # checkpoint_b = finish, and numcheckpoints+1 != total
            if (routeleg.checkpoint_b == race.checkpoint_finish) and (route.routelegs.count() + 1 != race.checkpoint_qty):
                print '\tFAIL: %s is the finish line, but there is only %i checkpoints so far in this route.' % (routeleg.checkpoint_b.name, len(route.routelegs))
                return None
        
            # if adding routeleg makes the total distance too far
                #            if route.distance_thus_far() + routeleg.distance > race.max_race_distance:
                #                print "\tFAIL: %s will make race > max race distance %d" % (routeleg, race.max_race_distance)
                #                return None

            # checkpoint_b already used
            for r in route.routelegnode_set.all():
                print '\tFAIL: %s is already in use in this route.' % routeleg.checkpoint_b.name
                if r.routeleg.checkpoint_b is routeleg.checkpoint_b:
                    return None

        else:
            # instantiate a new route
            route = Route()
            route.name = 'Route %s' % (race.routes.count() + 1)
            route.checkpoint_start = race.checkpoint_start
            route.checkpoint_finish = race.checkpoint_finish
            route.is_valid = False
            print '[new route] %s' % route.name
            route.save()
            
        # ---------------------------------------------
        # all tests pass. 

        # build a new routelegnode
        print '[append] %s' % routeleg
        
        node = RouteLegNode()
        node.parent_route = route
        node.routeleg = routeleg
        node.order = route.routelegs.count() + 1
        node.save()
        
        route.routelegnode_set.add(node)
        route.save()
        
        # get all potential routelegs with our current checkpoint b as their checkpoint a
        potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % routeleg.checkpoint_b.name)  
        print '[query] routelegs starting with %s: %i' % (routeleg.checkpoint_b.name, potential_legs.count())
    
        # loop through all potential routelegs.  If we get back a route, then return it.
        for r in potential_legs:
            route = self.buildRoutes(race, r, route)
            if route:
                return route
        return None


# ========================================================================================================================

    def ip(self, x, str):
        s = ''
        for i in range(x):
            s += "\t"
        print "%s%s" % (s, str)

    def mungeRace(self, raceName):
        """main function to build an entire race, given a start and finish point."""
        race = Race.objects.get(name=raceName)
        # start building routes using each potential routeleg
        print '[race] %s  [start] %s' % (race.name, race.checkpoint_start.name)
        legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name)  
        print 'found %i legs' % len(legs)
        
        race = self.munge(race, legs)
        print race


    def munge(self, race, legs, route = None):

        x = 0
        if route:
            x = route.routelegs.count()

        # iterate through all legs we were passed.
        for leg in legs:
                
            self.ip(x,"munge: %s" % leg)
            
            # check for bad distance
            if (leg.distance > race.max_leg_distance):
                self.ip(x,"\tFAIL: %s length > max leg distance %s" % (leg.distance, race.max_leg_distance))
                continue
            self.ip(x,"\tPASS: %s length <= max leg distance %s" % (leg.distance, race.max_leg_distance))

            # checkpoint_b should never be the starting line
            if (leg.checkpoint_b == race.checkpoint_start):
                self.ip(x,'\tFAIL: %s is the starting line, that can never be.' % leg.checkpoint_b.name)
                continue
            self.ip(x,"\tPASS: %s is not the starting line" % (leg.checkpoint_b.name))
                

            # additional checks for existing routes
            if route:
                numlegs = route.routelegs.count()
                self.ip(x,'\tStarting route tests.  current depth: %s' % numlegs)
                
                # checkpoint_b != finish, and numcheckpoints+1 == total qty
                if (leg.checkpoint_b != race.checkpoint_finish) and (numlegs + 1 == race.checkpoint_qty):
                    self.ip(x,'\tFAIL: %s is not the finish line, but this route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                    continue
                
                # checkpoint_b = finish, and numcheckpoints+1 != total qty
                if (leg.checkpoint_b == race.checkpoint_finish) and (numlegs + 1 != race.checkpoint_qty):
                    self.ip(x,'\tFAIL: %s is the finish line, but this route is only %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                    continue

                # if adding this leg makes the total distance too far
                if getRouteLength(route) + leg.distance > race.max_race_distance:
                    self.ip(x,"\tFAIL: %s will make race > max race distance %d" % (leg, race.max_race_distance))
                    continue
                self.ip(x,"\tPASS: %s will not make the race > max race distance %d" % (leg, race.max_race_distance))
                
                # fail if checkpoint_b is already used
                bad=False
                for r in route.routelegnode_set.all():
                    if r.routeleg.checkpoint_b == leg.checkpoint_b:
                        bad=True
                if bad:
                     self.ip(x,'\tFAIL: %s is already in use in this route.' % leg.checkpoint_b.name)
                     continue
                self.ip(x,'\tPASS: %s is not yet in use in this route.' % leg.checkpoint_b.name)


            # and if a route doesn't exist, make one and move on.
            else:
                # build new route
                route = Route()
                route.name = 'Route %s' % (race.routes.count() + 1)
                route.checkpoint_start = race.checkpoint_start
                route.checkpoint_finish = race.checkpoint_finish
                route.is_valid = False
                route.save()
                self.ip(x,'[new route] %s' % route.name)


            # if we made it this far, add a RouteLegNode to our routes list
            node = RouteLegNode()
            node.parent_route = route
            node.routeleg = leg
            node.order = route.routelegs.count() + 1
            self.ip(x,'[new node] %s [order: %s]' % (node, node.order))
            node.save()

            route.routelegnode_set.add(node)
            route.save()
            
            # ---------------------------------------------
            # winning condition.  add this route to our race object
            if (route.routelegs.count() == race.checkpoint_qty):
                if (leg.checkpoint_b == race.checkpoint_finish):
                    self.ip(x,'[ WIN ] %s' % route)
                    race.routes.add(route)
                    continue

            # ---------------------------------------------
            # ok, so we didn't win, but we have a leg that's not failing out. 
            sublegs = RouteLeg.objects.filter(checkpoint_a__name="%s" % leg.checkpoint_b.name)  
            self.ip(x,'[sublegs] found %i' % len(sublegs))

            race = self.munge(race, sublegs, route)
    
        return race
        
