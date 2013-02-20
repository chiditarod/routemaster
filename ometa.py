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
import operator
import timeit
from itertools import permutations
from operator import itemgetter, attrgetter

#from copy import copy


class RaceBuilder(object):

    def __init__(self):
        self.output = HttpResponse(content_type="text/plain")

    def ip(self, x, str):
        s = ''
        for i in range(x):
            s += "  "

        self.output.write("%s%s\n" % (s, str))
        print "%s%s" % (s, str)

    def buildRoutesForRace(self, race_id):
        """main function to build an entire race, given a start and finish point. calls our recursion."""

        race = Race.objects.get(id=race_id)

        # start building routes using each potential routeleg
        self.ip(0, '[race] %s  [start] %s' % (race.name, race.checkpoint_start.name))
        legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % race.checkpoint_start.name).exclude(checkpoint_b__enabled=False)
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
                self.ip(x,'[NEW ROUTE] %s' % route.name)

            x = route.countRoutelegs()
            self.ip(x,"Trying %s for route: %s" % (leg, route))

            # check for bad distance
            if (leg.distance > race.max_leg_distance):
                self.ip(x,"  FAIL: %s distance > max: %s" % (leg.distance, race.max_leg_distance))
                continue
            self.ip(x,"  PASS: %s distance <= max: %s" % (leg.distance, race.max_leg_distance))

            if (leg.distance < race.min_leg_distance):
                self.ip(x,"  FAIL: %s distance < min: %s" % (leg.distance, race.min_leg_distance))
                continue
            self.ip(x,"  PASS: %s distance >= min:%s" % (leg.distance, race.min_leg_distance))

            # ensure that checkpoint b is not disabled
            if (leg.checkpoint_b.enabled == False):
                self.ip(x, '\tFAIL: %s is disabled.  Skipping.' % leg.checkpoint_b.name)
                continue

            # checkpoint_b should never be the starting line
            if (leg.checkpoint_b == race.checkpoint_start):
                self.ip(x,'\tFAIL: %s = starting line.  Cannot be a checkpoint.' % leg.checkpoint_b.name)
                continue

            self.ip(x,"  PASS: %s != the starting line" % (leg.checkpoint_b.name))

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
                    self.ip(x,"  FAIL: %s distance > max race distance %s" % (potentialDistance, race.max_race_distance))
                    continue
                self.ip(x,"  PASS: %s distance < max race distance %s" % (potentialDistance, race.max_race_distance))

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
            node.order = route.countRoutelegs()
            self.ip(x,'[NEW NODE] %s [order: %s]' % (node, node.order))

            # add the new node to the route
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
                    # TODO: check for duplicate first.  see:
                    #   https://docs.djangoproject.com/en/1.2/topics/db/queries/#query-expressions
                    #   http://stackoverflow.com/questions/2055626/filter-many-to-many-relation-in-django
                    route_copy.length = route_copy.getLength()
                    race.routes.add(route_copy)
                    race.save()

                # slide the highest node off the route, regardless of whether or not we saved it
                self.sliceLatestNode(route, x)

            else:
                # ok, so we didn't win, but we have a leg that's not failing out.  Pursue additional recursion. 

                # This case should not occur
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
            deleteNode = RouteLegNode.objects.get(parent_route=route, order=totalNodes-1) # order starts at 0
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
        """Add capacities into the database for each route stored in a race."""
        count = 0
        for r in race.routes.all():
            self.addCapacityToRoute(r)
            count += 1
        return count


    def deleteRoutesInRace(self, race):
        """Delete all routes attached to a particular race."""
        r = Route.objects.filter(race=race)
        routesToDelete = r.count()
        r.all().delete()
        return "Deleted %s routes from %s" % (routesToDelete, race)


    def findUniqueRoutes(self, race, repeat_qty = 0):
        """Choose the routes that don't overlap any checkpoints in each respective routeleg position.  Repeats are allowed via a variable."""
        used_routes = []
        deferred_routes = []
        positions = race.checkpoint_qty - 1 # subtract one so we don't include the finish line.
        # make a list of lists, 'positions' in length
        a = list(list() for i in range(positions))

        # iterate through all routes in the race
        for route in race.routes.all():

            ok = True
            print "processing route id: %s" % route.id

            # temp list b, a list of lists
            b = list(list() for i in range(positions))

            # iterate through all checkpoints in each route
            for x, leg in enumerate(route.routelegs.all()):

                # if we're evaluating the finish line, skip (since the finish is always the same)
                if (x == positions):
                    break

                print "a[%s] is: %s" % (x, a[x])
                print "leg is: %s" % leg

                # not used
                if leg.checkpoint_b not in a[x]:
                    print "checkpoint %s is not yet used as checkpoint %s.  Add it to our temp list, b\n" % (leg.checkpoint_b, x)
                    b[x].append(leg.checkpoint_b)
                # used less than our repeat qty
                elif repeat_qty and a[x].count(leg.checkpoint_b) < int(repeat_qty) + 1:
                    print "checkpoint %s is used %s times as checkpoint %s, with %s repeats allowed. Add it to our temp list, b\n" % (leg.checkpoint_b, x, a[x].count(leg.checkpoint_b), repeat_qty)
                    b[x].append(leg.checkpoint_b)
                # failure case
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




    def findUniqueRoutes2(self, race, repeat_qty = 0):
        """Choose the routes that don't overlap any checkpoints in each respective routeleg position.  Repeats are allowed via a variable."""

        #timer = Timer()

        maxUnique = 0

        # build a list of all potential combinations of routes.
        all_route_combos = permutations(race.routes.all())

#        n = 0
#        for x in all_route_combos:
#            n += 1
#        print "total permutations: %s" % n

        master_results = list()

        for n, routeset in enumerate(all_route_combos):

            if n % 100 == 0:
                print "processing routeset: %s" % n

            used_routes = []
 #           deferred_routes = []
            positions = race.checkpoint_qty - 1 # subtract one so we don't include the finish line.
            # make a list of lists, 'positions' in length
            a = list(list() for i in range(positions))

            # iterate through all routes in the race
            for route in routeset:

                ok = True
                if settings.DEBUG_MODE:
                    print "processing route id: %s" % route.id

                # temp list b, a list of lists
                b = list(list() for i in range(positions))

                # iterate through all checkpoints in each route
                for x, leg in enumerate(route.routelegs.all()):

                    # if we're evaluating the finish line, skip (since the finish is always the same)
                    if (x == positions):
                        break


                    if settings.DEBUG_MODE:
                        print "a[%s] is: %s" % (x, a[x])
                        print "leg is: %s" % leg

                    # not used
                    if leg.checkpoint_b not in a[x]:
                        if settings.DEBUG_MODE:
                            print "checkpoint %s is not yet used as checkpoint %s.  Add it to our temp list, b\n" % (leg.checkpoint_b, x)
                        b[x].append(leg.checkpoint_b)
                    # used less than our repeat qty
                    elif repeat_qty and a[x].count(leg.checkpoint_b) < int(repeat_qty) + 1:
                        if settings.DEBUG_MODE:            
                            print "checkpoint %s is used %s times as checkpoint %s, with %s repeats allowed. Add it to our temp list, b\n" % (leg.checkpoint_b, x, a[x].count(leg.checkpoint_b), repeat_qty)
                        b[x].append(leg.checkpoint_b)
                    # failure case
                    else:
                        if settings.DEBUG_MODE:
                            print "checkpoint %s is already used as checkpoint %s.  defer entire route\n" % (leg.checkpoint_b, x)
#                        deferred_routes.append(route)
                        ok = False
                        break

                # if we made it this far, add our temp list b to our master list a
                # TODO: there must be a cleaner way of doing this other than checkpoint[0]
                if ok:
                    for x, checkpoint in enumerate(b):
                        if len(checkpoint):
                            if settings.DEBUG_MODE:
                                print "appending: %s %s\n" % (x, checkpoint)
                            a[x].append(checkpoint[0])

                    # add this route to our used route list.
                    used_routes.append(route)

            if settings.DEBUG_MODE:
                print ""
                for i in a:
                    print "%s" % i
                print ""

                print "used_routes: %s" % len(used_routes)
                #print "deferred_routes: %s" % len(deferred_routes)

            if len(used_routes) > maxUnique:
                print "routeset %s: # of unique routes (%s) > current maxUnique value (%s)" % (n, len(used_routes), maxUnique)
                maxUnique = len(used_routes)
                master_results.append( (len(used_routes),used_routes) )

        return master_results

# ======================================================================================    


    def checkpointFrequency(self, routes):
        """Count up how many times each checkpoint appears in a list of routes."""
        counts = dict()
        for r in routes:
            for leg in r.routelegs.all():
                if leg.checkpoint_b.name == r.race.checkpoint_finish.name:
                    continue
                if str(leg.checkpoint_b.name) in counts:
                    counts[str(leg.checkpoint_b.name)] += 1
                else:
                    counts[str(leg.checkpoint_b.name)] = 1
        s = sorted(counts.iteritems(), key=operator.itemgetter(1))
        return s


    def rarityTree(self, race, rarityThreshold):
        """Figure out the least-frequent checkpoint/position pairs repeated for all routes and pull their routes."""
        print "Rarity Tree for Race: %s" % race
        print "total routes to examine: %s" % race.routes.count()

        preferredRoutes = list()

        positions = race.checkpoint_qty - 1 # subtract one so we don't include the finish line.
        # make a list of lists, 'positions' in length
        a = list(dict() for i in range(positions))

        # iterate through all routes in the race
        for route in race.routes.all():

            # iterate through all checkpoints in each route
            for x, leg in enumerate(route.routelegs.all()):

                # if we're evaluating the finish line, skip (since the finish is always the same)
                if (x == positions):
                    break

                # build an index of each checkpoint position.  put a dict of checkpoint/occurence frequency values in each.
                key = str(leg.checkpoint_b.pk)
                if key in a[x]:
                    a[x][key] += 1
                else:
                    a[x][key] = 1

        for x, pos in enumerate(a):
            print "%s: %s" % (x, pos)
        rarityTree = list()             # init our result list

        # iterate through each checkpoint position
        for x, row in enumerate(a):
            print "\n[position %s]" % (x)
            # convert dict checkpoint/occurence list into sortable tuples.
            pairs = zip(row.values(), row.keys())

            # sort the least-occuring position/checkpoint combos first
            sortedPairs = sorted(pairs)
            print sortedPairs

            y = 0                       # for moving upwards in the rarity threshold
            i = sortedPairs[y][0]       # initial value

            while (i <= rarityThreshold):
                #print "pos: %s, y: %s, i: %s" % (x,y,i)
                checkpoint_id = sortedPairs[y][1] # grab the checkpoint name from the tuple.
                checkpoint = Checkpoint.objects.get(id__exact=checkpoint_id)
                print "freq: %s.  checkpoint: %s (id: %s) appears in position %s" % (i, checkpoint.name, checkpoint.pk, x)
                # filter routes: choose the routes that have 'checkpoint' in order 'x'.
                # TODO 2013 - this call below is showing disabled checkpoints.  WTF.
                routes = Route.objects.filter(race=race)\
                                      .filter(routelegnode__order=x, routelegs__checkpoint_b__pk=checkpoint_id)\
                                      .distinct()

                print "found %s routes" % routes.count()

                print ''
                #print "Found %s routes:" % routes.count()
                for r in routes:
                    # update the rarity for this route
                    r.rarity = i
                    r.save()
                    rarityTree.append({'order': x+1, 'rarity':i, 'route':r, 'checkpoint':checkpoint})
                    #print r.getPath()
                y += 1
                i = sortedPairs[y][0]

            else:
                print "freq: %s.  Threshold of %s reached.  Moving on." % (i, rarityThreshold)

        #print rarityTree
        return sorted(rarityTree)

