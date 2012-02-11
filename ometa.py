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
from django.http import HttpResponse
from copy import deepcopy

def getRouteLength(route):
	total = 0
	for r in route.routelegnode_set.all():
		total += r.routeleg.distance
	return total



class RaceBuilder(object):

    def __init__(self):
        self.output = HttpResponse(content_type="text/plain")
    
    def ip(self, x, str):
        s = ''
        for i in range(x):
            s += "\t"
            
        self.output.write("%s%s\n" % (s, str))
        print "%s%s" % (s, str)

    def mungeRace(self, raceName):
        """main function to build an entire race, given a start and finish point."""
        race = Race.objects.get(name=raceName)
        # start building routes using each potential routeleg
        self.ip(0, '[race] %s  [start] %s' % (race.name, race.checkpoint_start.name))
        legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name)  
        self.ip(0, 'found %i legs' % len(legs))
        
        race = self.munge(race, legs)
        self.ip(0, "num races: %i" % race.routes.count())
        return race, self.output

    
    def munge(self, race, legs, route = None):
        """primary recursive function"""
        initialRoute = route
        x = 0
        y = 0
        
        # iterate through all legs we were passed.
        for leg in legs:
            y = y + 1
            self.ip(x,"processing: %s" % route)
            self.ip(x,"leg %i" % y)
            
            # reset the route to what is was leading into each new leg
            route = initialRoute

            if route:
                x = route.routelegs.count()
                self.ip(x,"[munge] %s" % leg)
            
            # check for bad distance
            if (leg.distance > race.max_leg_distance):
                self.ip(x,"\tFAIL: %s distance > max leg distance %s" % (leg.distance, race.max_leg_distance))
                continue
            self.ip(x,"\tPASS: %s distance <= max leg distance %s" % (leg.distance, race.max_leg_distance))

            # checkpoint_b should never be the starting line
            if (leg.checkpoint_b == race.checkpoint_start):
                self.ip(x,'\tFAIL: %s = starting line.  Cannot be a checkpoint.' % leg.checkpoint_b.name)
                continue
                
            self.ip(x,"\tPASS: %s != the starting line" % (leg.checkpoint_b.name))
                
            # additional checks when a route exists
            if route:
                numlegs = route.routelegs.count() 
                
                if (numlegs > race.checkpoint_qty):
                    self.ip(x,'\tERROR: numlegs = %s > %s (checkpoint qty).  Should not happen.' % (numlegs, race.checkpoint_qty + 1))
                    continue
                    
                # finish line checks
                if (leg.checkpoint_b == race.checkpoint_finish):
                    if (numlegs < race.checkpoint_qty - 1):
                        self.ip(x,'\tFAIL: %s = finish line, route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                        continue
                    else:
                        self.ip(x,'\tPASS: %s = finish line, route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                else:
                    if (numlegs == race.checkpoint_qty - 1):
                        self.ip(x,'\tFAIL: %s != finish line, route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                        continue
                    else:
                        self.ip(x,'\tPASS: %s != finish line, route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                            
                # checkpoint_b != finish, and numcheckpoints == total qty + 1
                #if (leg.checkpoint_b != race.checkpoint_finish) and (numlegs == race.checkpoint_qty - 1):
                #    self.ip(x,'\tFAIL: %s is not the finish line, but this route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                #    continue
                #else:
                 #   self.ip(x,'\tPASS: %s may be the finish line, and this route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                
                # checkpoint_b == finish, and numcheckpoints == total qty - 1
                #if (leg.checkpoint_b == race.checkpoint_finish) and (numlegs < race.checkpoint_qty - 1):
                #    self.ip(x,'\tFAIL: %s is the finish line, but this route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))
                #    continue
                #else:
                #    self.ip(x,'\tPASS: %s may be the finish line, and this route is %i/%i full' % (leg.checkpoint_b.name, numlegs, race.checkpoint_qty))

                # if adding this leg makes the total distance too far
                potentialDistance = getRouteLength(route) + leg.distance
                if potentialDistance > race.max_race_distance:
                    self.ip(x,"\tFAIL: %s distance > max race distance %d" % (potentialDistance, race.max_race_distance))
                    continue
                self.ip(x,"\tPASS: %s distance < max race distance %d" % (potentialDistance, race.max_race_distance))
                
                # fail if checkpoint_b is already used
                bad=False
                for r in route.routelegnode_set.all():
                    if r.routeleg.checkpoint_b == leg.checkpoint_b:
                        bad=True
                if bad:
                     self.ip(x,'\tFAIL: %s is already in use in this route.' % leg.checkpoint_b.name)
                     continue
                self.ip(x,'\tPASS: %s is not yet in use in this route.' % leg.checkpoint_b.name)


            # and if a route doesn't exist (i.e. right at the beginning), make one
            else:
                # build new route
                route = Route()
                route.name = 'Route %s' % (race.routes.count())
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

            # add the new node to the route
            route.routelegnode_set.add(node)
            
            # ---------------------------------------------
            # WINNING CONDITION!!!
            # add this route to our race object
            if (route.routelegs.count() == race.checkpoint_qty) and (leg.checkpoint_b == race.checkpoint_finish):
                self.ip(x,'[ WIN ] %s' % route)
#                route_copy = deepcopy(route)
                route_copy = deepcopy(route)
                self.ip(x, route_copy)
                route_copy.pk = None
                route_copy.save()
                race.routes.add(route_copy)
                
                # slide the highest node off the route
                self.sliceLatestNode(route, x)
            else:
                # ok, so we didn't win, but we have a leg that's not failing out.  Pursue additional recursion. 
                if (route.routelegs.count() == race.checkpoint_qty):
                    self.ip(x,'Route has enough legs.  Not recursing further.')
                else:
                    sublegs = RouteLeg.objects.filter(checkpoint_a__name="%s" % leg.checkpoint_b.name)  
                    self.ip(x,'[sublegs] found %i' % len(sublegs))
                    # recurrrrrsion!
                    race = self.munge(race, sublegs, route)
                

        # ROUTE FAIL.  Remove the most recent node and move on.    
        if route: # and not route in race.routes.all():
            # delete the latest node
            self.ip(x,"[END OF ROUTE POTENTIAL]")
            self.sliceLatestNode(route, x)
            
            # check to see if our route is length=0. if so, delete it
            if (route.routelegs.count() == 0):
                self.ip(x,"Deleting route containing 0 nodes")            
                Route.objects.get(id=route.pk).delete()
        
        # return our completed race object.
        self.ip(x,"returning race")            
        return race
        

    def sliceLatestNode(self, route, x):
        totalNodes = route.routelegs.count()
        deleteNode = RouteLegNode.objects.get(parent_route=route, order=totalNodes)
        self.ip(x, "Slicing %s:" % deleteNode)
        deleteNode.delete()
    