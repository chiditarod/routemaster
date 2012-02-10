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
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('num_teams', self.gf('django.db.models.fields.IntegerField')()),
            ('num_people_per_team', self.gf('django.db.models.fields.IntegerField')()),
            ('max_race_distance', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('max_leg_distance', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('unified_start_checkpoint', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('unified_finish_checkpoint', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('checkpoint_qty', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('races', ['Race'])

        # Adding M2M table for field routes on 'Race'
        db.create_table('races_race_routes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('race', models.ForeignKey(orm['races.race'], null=False)),
            ('route', models.ForeignKey(orm['races.route'], null=False))
        ))
        db.create_unique('races_race_routes', ['race_id', 'route_id'])

        # Adding model 'Checkpoint'
        db.create_table('races_checkpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('capacity_comfortable', self.gf('django.db.models.fields.IntegerField')()),
            ('capacity_max', self.gf('django.db.models.fields.IntegerField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('state_province', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2, blank=True)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(default='0', max_digits=10, decimal_places=2, blank=True)),
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
            ('checkpoint_start', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkpoint_start', to=orm['races.Checkpoint'])),
            ('checkpoint_finish', self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkpoint_finish', to=orm['races.Checkpoint'])),
        ))
        db.send_create_signal('races', ['Route'])


    def backwards(self, orm):
        
        # Deleting model 'Race'
        db.delete_table('races_race')

        # Removing M2M table for field routes on 'Race'
        db.delete_table('races_race_routes')

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
            'capacity_comfortable': ('django.db.models.fields.IntegerField', [], {}),
            'capacity_max': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
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
            'checkpoint_qty': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_leg_distance': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'max_race_distance': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'num_people_per_team': ('django.db.models.fields.IntegerField', [], {}),
            'num_teams': ('django.db.models.fields.IntegerField', [], {}),
            'routes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['races.Route']", 'symmetrical': 'False'}),
            'unified_finish_checkpoint': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'unified_start_checkpoint': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'races.route': {
            'Meta': {'object_name': 'Route'},
            'checkpoint_finish': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkpoint_finish'", 'to': "orm['races.Checkpoint']"}),
            'checkpoint_start': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkpoint_start'", 'to': "orm['races.Checkpoint']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'routelegs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['races.RouteLeg']", 'through': "orm['races.Node']", 'symmetrical': 'False'})
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
