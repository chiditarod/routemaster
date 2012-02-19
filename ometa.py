"""
ometa.py

Created by Devin Breen on 2012-02-08.
Copyright (c) 2012 Ometa, Inc. All rights reserved.
"""

#from django.http import HttpResponse, Http404
#from django.template.loader import  get_template
#from django.template import Context
#from django.shortcuts import render_to_response
#import datetime

from races.models import RouteLeg, Race, Checkpoint, RouteLegNode, Route
from django.http import HttpResponse
from django.conf import settings

class RaceBuilder(object):

    def __init__(self):
        self.output = HttpResponse(content_type="text/plain")
    
    def ip(self, x, str):
        s = ''
        for i in range(x):
            s += "\t"
            
        self.output.write("%s%s\n" % (s, str))
        print "%s%s" % (s, str)

    def buildRoutesForRace(self, race_id):
        """main function to build an entire race, given a start and finish point. calls our recursion."""
        
        race = Race.objects.get(id=race_id)
                    
        # start building routes using each potential routeleg
        self.ip(0, '[race] %s  [start] %s' % (race.name, race.checkpoint_start.name))
        legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name)  
        self.ip(0, 'found %i legs' % len(legs))
        
        race = self.buildRoute(race, legs)
        self.ip(0, "num routes found: %i" % race.routes.count())
        return race, self.output

    
    def buildRoute(self, race, legs, route = None):
        """primary recursive function"""
        
        # capture the route as-is before trying to add on new legs
        initialRoute = route
        x = 0
        y = 0
        
        # iterate through all potential legs
        for leg in legs:
            y = y + 1
            
            # reset the route to what is was leading into each new leg
            route = initialRoute
            
            # make a new route if we weren't passed one via recursion.
            if not route:
                route = Route()
                route.name = 'Route %s' % (race.routes.count())
                route.race = race
                route.checkpoint_start = race.checkpoint_start
                route.checkpoint_finish = race.checkpoint_finish
#                route.is_valid = False
                self.ip(x,'[NEW ROUTE] %s' % route.name)

            x = route.countRoutelegs()
            self.ip(x,"Trying %s for route: %s" % (leg, route))
        
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
                numlegs = route.countRoutelegs() 
                
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
                            
                # if adding this leg makes the total distance too far
                potentialDistance = route.getLength() + leg.distance
                if potentialDistance > race.max_race_distance:
                    self.ip(x,"\tFAIL: %s distance > max race distance %s" % (potentialDistance, race.max_race_distance))
                    continue
                self.ip(x,"\tPASS: %s distance < max race distance %s" % (potentialDistance, race.max_race_distance))
                
                # fail if checkpoint_b is already used
                bad=False
                for r in route.routelegnode_set.all():
                    if r.routeleg.checkpoint_b == leg.checkpoint_b:
                        bad=True
                if bad:
                     self.ip(x,'\tFAIL: %s is already in use in this route.' % leg.checkpoint_b.name)
                     continue
                self.ip(x,'\tPASS: %s is not yet in use in this route.' % leg.checkpoint_b.name)


            # if we made it this far, add a RouteLegNode to our routes list
            node = RouteLegNode()
            node.parent_route = route
            node.routeleg = leg
            node.order = route.countRoutelegs() + 1
            self.ip(x,'[NEW NODE] %s [order: %s]' % (node, node.order))

            # add the new node to the route
            # TODO: check for duplicate first.  see:
            #   https://docs.djangoproject.com/en/1.2/topics/db/queries/#query-expressions
            #   http://stackoverflow.com/questions/2055626/filter-many-to-many-relation-in-django
            route.save()
            route.routelegnode_set.add(node)
            
            # ---------------------------------------------
            # WINNING CONDITION!!!
            
            # these are the conditions for a winning route.  additional tests are applied within.
            if (route.countRoutelegs() == race.checkpoint_qty) and (leg.checkpoint_b == race.checkpoint_finish):
                
                # additional tests that only apply to a completed route
                if route.getLength() < race.min_race_distance:
                    self.ip(x,'\tFAIL: %s distance < min race distance %s' % (route.getLength(), race.min_race_distance))
                else:
                    # we're good.  Save.
                    self.ip(x,'[ WIN ] %s' % route)
                    # copy our route (and the intermediate models) and save it to the route table.
                    route_copy = route.clone()
            
                    race.routes.add(route_copy)
                    race.save()
                                
                # slide the highest node off the route, regardless of whether or not we saved it
                self.sliceLatestNode(route, x)
                
            else:
                # ok, so we didn't win, but we have a leg that's not failing out.  Pursue additional recursion. 
                
                # i don't think the if below will ever run...
                if (route.countRoutelegs() == race.checkpoint_qty):
                    self.ip(x,'Route has enough legs.  Not recursing further.')
                else:
                    sublegs = RouteLeg.objects.filter(checkpoint_a__name="%s" % leg.checkpoint_b.name)  
                    self.ip(x,'[sublegs] found %i' % len(sublegs))
                    # recurrrrrsion!
                    race = self.buildRoute(race, sublegs, route)
                

        # ROUTE FAIL.  Remove the most recent node and move on.    
        if route: # and not route in race.routes.all():
            # delete the latest node
            self.ip(x,"[END OF ROUTE POTENTIAL]")
            self.sliceLatestNode(route, x)
            
            # check to see if our route is length=0. if so, delete it
            if (route.countRoutelegs() == 0):
                self.ip(x,"Deleting route containing 0 nodes")  
                # we only have to delete the route if it's not already in the DB          
                if route.id is not None:
                    route.delete()
        
        # return our completed race object.
        self.ip(x,"returning race")            
        return race
        

    def sliceLatestNode(self, route, x):
        """Slices off the most recent routelegnode from a route"""
        try:
            totalNodes = route.countRoutelegs()
            deleteNode = RouteLegNode.objects.get(parent_route=route, order=totalNodes)
            if deleteNode:
                self.ip(x, "[SLICE NODE] %s:" % deleteNode)
                deleteNode.delete()
        except Exception, e:
            self.ip(x, "[SLICE NODE] No node to delete OR problem.")
            
    
    def addCapacityToRoute(self, route):
        """Go through each checkpoint in a route and calculate the max and comfortable capacity for the entire route."""
        capComfortable = settings.DEFAULT_CAPACITY_COMFORTABLE
        capMaximum = settings.DEFAULT_CAPACITY_MAXIMUM
        """Figures out the comfortable and maximum capacity for each route by looking at each checkpoint"""
        for r in route.routelegs.all():
            print capComfortable, capMaximum
            print r
            if r.checkpoint_a.capacity_comfortable < capComfortable:
                capComfortable = r.checkpoint_a.capacity_comfortable
            if r.checkpoint_a.capacity_max < capMaximum:
                capMaximum = r.checkpoint_a.capacity_max
        route.capacity_comfortable = capComfortable
        route.capacity_max = capMaximum
        route.save()
        return capComfortable, capMaximum
        
        
    def addRouteCapacities(self, race):
        """Add capacities for each route stored in a race."""
        count = 0
        for r in race.routes.all():
            self.addCapacityToRoute(r)
            count += 1
        return count
    
    
    def findUniqueRoutes(self, race, repeat_qty = 0):
        """Choose the routes that don't overlap any checkpoints in each respective routeleg position."""
        used_routes = []
        deferred_routes = []
        positions = race.checkpoint_qty - 1 # subtract one so we don't include the finish line.
        a = list(list() for i in range(positions))
        
        # iterate through all routes in the race
        for route in race.routes.all():

            print "processing route id: %s" % route.id

            ok = True
            
            # temp list b, a list of lists
            b = list(list() for i in range(positions))
            
            # iterate through all checkpoints in each route
            for x, leg in enumerate(route.routelegs.all()):
                
                # skip the final routeleg (as we aren't processing the finish line, which is always the same)
                if (x == positions):
                    break
                    
                print "a[%s] is: %s" % (x, a[x])
                print "leg is: %s" % leg
                
                if leg.checkpoint_b not in a[x]:
                    print "checkpoint %s is not yet used as checkpoint %s.  Add it to our temp list, b\n" % (leg.checkpoint_b, x)
                    b[x].append(leg.checkpoint_b)
                elif repeat_qty and a[x].count(leg.checkpoint_b) < int(repeat_qty) + 1:
                    print "checkpoint %s is used %s times as checkpoint %s, with %s repeats allowed. Add it to our temp list, b\n" % (leg.checkpoint_b, x, a[x].count(leg.checkpoint_b), repeat_qty)
                    b[x].append(leg.checkpoint_b)
                else:
                    print "checkpoint %s is already used as checkpoint %s.  defer entire route\n" % (leg.checkpoint_b, x)
                    deferred_routes.append(route)
                    ok = False
                    break
            
            # if we made it this far, add our temp list b to our master list a
            # TODO: there must be a cleaner way of doing this other than checkpoint[0]
            if ok:
                for x, checkpoint in enumerate(b):
                    if len(checkpoint):
                        print "appending: %s %s\n" % (x, checkpoint)
                        a[x].append(checkpoint[0])
            
                # add this route to our used route list.
                used_routes.append(route)
            
        print ""
        for i in a:
            print "%s" % i
        print ""
            
        print "used_routes: %s" % len(used_routes)
        print "deferred_routes: %s" % len(deferred_routes)

        return used_routes, deferred_routes
    
    