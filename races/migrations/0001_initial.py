# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Race'
        db.create_table('races_race', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('num_teams', self.gf('django.db.models.fields.IntegerField')()),
            ('num_people_per_team', self.gf('django.db.models.fields.IntegerField')()),
            ('max_race_distance', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('max_leg_distance', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('races', ['Race'])

        # Adding model 'Checkpoint'
        db.create_table('races_checkpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('races', ['Checkpoint'])

        # Adding model 'RouteLeg'
        db.create_table('races_routeleg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checkpoint_a', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkpoint_a', to=orm['races.Checkpoint'])),
            ('checkpoint_b', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkpoint_b', to=orm['races.Checkpoint'])),
            ('distance', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('measurement', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('races', ['RouteLeg'])

        # Adding model 'Node'
        db.create_table('races_node', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['races.Route'])),
            ('routeleg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['races.RouteLeg'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('races', ['Node'])

        # Adding model 'Route'
        db.create_table('races_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('parent_race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['races.Race'])),
            ('start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='start_checkpoint', to=orm['races.Checkpoint'])),
            ('finish', self.gf('django.db.models.fields.related.ForeignKey')(related_name='end_checkpoint', to=orm['races.Checkpoint'])),
        ))
        db.send_create_signal('races', ['Route'])


    def backwards(self, orm):
        
        # Deleting model 'Race'
        db.delete_table('races_race')

        # Deleting model 'Checkpoint'
        db.delete_table('races_checkpoint')

        # Deleting model 'RouteLeg'
        db.delete_table('races_routeleg')

        # Deleting model 'Node'
        db.delete_table('races_node')

        # Deleting model 'Route'
        db.delete_table('races_route')


    models = {
        'races.checkpoint': {
            'Meta': {'object_name': 'Checkpoint'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'races.node': {
            'Meta': {'object_name': 'Node'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'parent_route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['races.Route']"}),
            'routeleg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['races.RouteLeg']"})
        },
        'races.race': {
            'Meta': {'object_name': 'Race'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_leg_distance': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'max_race_distance': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'num_people_per_team': ('django.db.models.fields.IntegerField', [], {}),
            'num_teams': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'races.route': {
            'Meta': {'object_name': 'Route'},
            'finish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'end_checkpoint'", 'to': "orm['races.Checkpoint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'parent_race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['races.Race']"}),
            'routelegs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['races.RouteLeg']", 'through': "orm['races.Node']", 'symmetrical': 'False'}),
            'start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'start_checkpoint'", 'to': "orm['races.Checkpoint']"})
        },
        'races.routeleg': {
            'Meta': {'object_name': 'RouteLeg'},
            'checkpoint_a': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkpoint_a'", 'to': "orm['races.Checkpoint']"}),
            'checkpoint_b': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkpoint_b'", 'to': "orm['races.Checkpoint']"}),
            'distance': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['races']
