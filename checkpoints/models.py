from django.db import models

class Race(models.Model):
    name = models.CharField(max_length=60)
    date = models.DateField()

class Checkpoint(models.Model):
    name = models.CharField(max_length=60)
    capacity = models.IntegerField()
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

# Leg between 2 checkpoints on a route
class RouteLeg(models.Model):
    a = models.ForeignKey('Checkpoint', related_name='a')
    b = models.ForeignKey('Checkpoint', related_name='b')
    distance = models.DecimalField(max_digits=3, decimal_places=2)
    
    def __unicode__(self):
        return u'%s -> %s = %d miles' % (self.a, self.b, self.distance)

class Route(models.Model):
    name = models.CharField(max_length=60)
    race = models.ForeignKey('Race')
    routelegs = models.ManyToManyField('RouteLeg', through='RouteLegOrder')

    def __unicode__(self):
        return self.name, routelegs

class RouteLegOrder(models.Model):
    route = models.ForeignKey('Route')
    routeleg = models.ForeignKey('RouteLeg')
    order = models.IntegerField(unique=True)
