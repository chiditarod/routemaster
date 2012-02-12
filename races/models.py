from django.db import models
import copy

class CloneableModel(models.Model):
    """ This will NOT work for ManyToMany relations using a 'through' intermediate model.
        from: http://djangosnippets.org/snippets/1271/
    """
    class Meta:
        abstract = True

    def cloneme(self):
        """Return an identical copy of the instance with a new ID."""
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned.')
        duplicate = copy.copy(self)
        # Setting pk to None tricks Django into thinking this is a new object.
        duplicate.pk = None
        duplicate.save()
        # ... but the trick loses all ManyToMany relations.
        for field in self._meta.many_to_many:
            source = getattr(self, field.attname)
            destination = getattr(duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return duplicate

class Race(models.Model):
    DISTANCE_CHOICES = (
        (u'miles', u'Miles'),
        (u'km', u'Kilometers'),
    )
    name = models.CharField(max_length=60)
    date = models.DateField()
    url = models.URLField(blank=True)
    num_teams = models.IntegerField()
    num_people_per_team = models.IntegerField()
    max_race_distance = models.DecimalField(max_digits=3, decimal_places=2)
    max_leg_distance = models.DecimalField(max_digits=3, decimal_places=2)
    checkpoint_start = models.ForeignKey('Checkpoint', related_name='races_starting_here')
    checkpoint_finish = models.ForeignKey('Checkpoint', related_name='races_finishing_here')
    # TODO: Change to route_legs
    checkpoint_qty = models.IntegerField('Total Legs (checkpoints + finish)')
    routes = models.ManyToManyField('Route', related_name='races', blank=True)
    measurement_system = models.CharField(max_length=5, choices=DISTANCE_CHOICES)
    
    def __unicode__(self):
        return "%s [ %s ==> %s ]" % (self.name, self.checkpoint_start.name, self.checkpoint_finish.name)

class Checkpoint(models.Model):
    name = models.CharField(max_length=60)
    capacity_comfortable = models.IntegerField()
    capacity_max = models.IntegerField()
    address = models.CharField(max_length=70)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    lat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default='0')
    lon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default='0')

    def __unicode__(self):
        return "%s" % (self.name)

class RouteLeg(models.Model):
    """Model containing the distance between 2 checkpoints"""
    checkpoint_a = models.ForeignKey('Checkpoint', related_name='from_checkpoint')
    checkpoint_b = models.ForeignKey('Checkpoint', related_name='to_checkpoint')
    distance = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return u'[ %s ] %s -> %s' % (float(self.distance), self.checkpoint_a.name, self.checkpoint_b.name)

class RouteLegNode(models.Model):
    """Intermediate Model defining the relationship between Routes and Routelegs."""
    parent_route = models.ForeignKey('Route')
    routeleg = models.ForeignKey('RouteLeg')
    order = models.IntegerField()

    def __unicode__(self):
        return "Node %i of %s: %s --> %s" % (self.order, self.parent_route.name, self.routeleg.checkpoint_a, self.routeleg.checkpoint_b) 

class Route(models.Model):
    """Route Model"""
    name = models.CharField(max_length=60)
    routelegs = models.ManyToManyField('RouteLeg', through='RouteLegNode', related_name='routelegs')
    checkpoint_start = models.ForeignKey('Checkpoint', related_name='start_for_route')
    checkpoint_finish = models.ForeignKey('Checkpoint', related_name='finish_for_route')
    is_valid = models.BooleanField()

    def getLength(self):
    	total = 0
    	for r in self.routelegnode_set.all():
    		total += r.routeleg.distance
    	return total

    def __unicode__(self):
        o = ''
        last = ''
        try:
            for r in self.routelegs.all():
                if r.checkpoint_a.name != last:
                    o += r.checkpoint_a.name
                o += ' -> ' 
                o += r.checkpoint_b.name
                last = r.checkpoint_b.name
            # else:
            #    o = "No RouteLegs"
        except Exception, e:
            return "No Routelegs"
        return u"%s: %s" % (self.name, o)
        
    def clone(self):
        """Return an identical copy of the instance with a new ID."""
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned.')
        duplicate = copy.copy(self)
        # Setting pk to None tricks Django into thinking this is a new object.
        duplicate.pk = None
        duplicate.save()
        # ... but the trick loses all ManyToMany relations.
        # copy the ManyToMany/through relation
        for field in self.routelegnode_set.all():
            rln = RouteLegNode.objects.create(parent_route=duplicate, routeleg=field.routeleg, order=field.order)
            duplicate.routelegnode_set.add(rln)
        duplicate.save()
        return duplicate
    
    def hasRoutelegs(self):
        try:
            if self.routelegnode_set.count() > 0:
                return True
            return False
        except ValueError, e:
            return False

    def countRoutelegs(self):
        try:
            return self.routelegnode_set.count()
        except ValueError, e:
            return 0
