#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Devin Breen on 2012-02-08.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

#import sys
#import os
#
#
#def main():
#	pass
#
#
#if __name__ == '__main__':
#	main()


#from django.http import HttpResponse, Http404
#from django.template.loader import  get_template
#from django.template import Context
#from django.shortcuts import render_to_response
#import datetime

from races.models import RouteLeg, Race, Checkpoint, Node, Route

# main function to build an entire race, given a start and finish point.
#def buildrace(start, finish):
def buildrace(self):
    # instantiate a new race object
    race = Race()
    
    # TODO: move race creation to web interface.
    race.checkpoint_start = Checkpoint.objects.get(name="Minimonk")
    race.checkpoint_finish = Checkpoint.objects.get(name="Bottom Lounge")
    race.checkpoint_qty = 5
    
    # start building routes using each potential routeleg
    potential_legs = RouteLeg.objects.filter(checkpoint_a__name="%s" % start.name)  
    
    for routeleg in potential_legs:        
        route = buildRoute(race, routeleg)
        if route is not None:
			race.routes.add(route)


def buildRoute(race, routeleg, route = None):
    
    # ------------------------------------------
    # checks of a bad routeleg:
	
	# routeleg distance > max_leg_distance
	if (routeleg.distance > race.max_leg_distance):
		return None
		
	# if adding routeleg makes the total distance too far
	if route.distanceThusFar + routeleg.distance > race.max_race_distance:
	    return None
	    
    # checkpoint_b = finish, and numcheckpoints+1 != total
    #if (routeleg.checkpoint_b is race.checkpoint_finish) and ((route.routelegs.count + 1) is not race.checkpoint_qty):
    #    return None
        
    # checkpoint_b already used
	for r in route.routelegs:
		if r.checkpoint_b is routeleg.checkpoint_b:
			return None
    
	# ---------------------------------------------
	# all tests pass. what next?
	




# TODO: This should be called somewhere else.
#buildrace
