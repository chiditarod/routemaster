from django.db import models

class Race(models.Model):
    name = models.CharField(max_length=60)
    date = models.DateField()
    num_teams = models.IntegerField()
    num_people_per_team = models.IntegerField()
    max_race_distance = models.DecimalField(max_digits=3, decimal_places=2)
    max_leg_distance = models.DecimalField(max_digits=3, decimal_places=2)
    checkpoint_qty = models.IntegerField()
    checkpoint_start = models.ForeignKey('Checkpoint', related_name='checkpoint_start')
    checkpoint_finish = models.ForeignKey('Checkpoint', related_name='checkpoint_finish')
    routes = models.ManyToManyField('Route')
    url = models.URLField()
    
    def __unicode__(self):
        return self.name

class Checkpoint(models.Model):
    name = models.CharField(max_length=60)
    capacity = models.IntegerField()
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
#    lat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default='')
#    lon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default='')

    def __unicode__(self):
        return "%s, capacity: %i" % (self.name, self.capacity)

# Info about the distance between 2 checkpoints
class RouteLeg(models.Model):
    DISTANCE_CHOICES = (
        (u'miles', u'Miles'),
        (u'km', u'Kilometers'),
    )
    checkpoint_a = models.ForeignKey('Checkpoint', related_name='checkpoint_a')
    checkpoint_b = models.ForeignKey('Checkpoint', related_name='checkpoint_b')
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    measurement = models.CharField(max_length=5, choices=DISTANCE_CHOICES)
    
    def __unicode__(self):
        return u'%s -> %s = %d miles' % (self.checkpoint_a, self.checkpoint_b, self.distance)

# Relationship between routelegs
class Node(models.Model):
    parent_route = models.ForeignKey('Route')
    routeleg = models.ForeignKey('RouteLeg')
    order = models.IntegerField(unique=True)

    def __unicode__(self):
        return "Node %i of route %s: %s --> %s" % (self.order, self.parent_route.name, self.routeleg.checkpoint_a, self.routeleg.checkpoint_b) 

# Route
class Route(models.Model):
    name = models.CharField(max_length=60)
    routelegs = models.ManyToManyField('RouteLeg', through='Node')
    start = models.ForeignKey('Checkpoint', related_name='start_checkpoint')
    finish = models.ForeignKey('Checkpoint', related_name='end_checkpoint')

    def __unicode__(self):
        return u"%s (%s ---> %s)" % (self.name, self.start.name, self.finish.name)

	def distanceThusFar(self):
		"""docstring for distanceThusFar"""
		total = 0
		try:
			for r in routelegs:
				total += r.distance
			return total
		except Exception, e:
			raise e
		