# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Universe'
        db.create_table(u'enterprise_universe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'enterprise', ['Universe'])

        # Adding model 'Enterprise'
        db.create_table(u'enterprise_enterprise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
            ('created_irl', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_igt', self.gf('django.db.models.fields.DateTimeField')()),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start_cash', self.gf('django.db.models.fields.IntegerField')()),
            ('universe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enterprise.Universe'])),
        ))
        db.send_create_signal(u'enterprise', ['Enterprise'])

        # Adding M2M table for field owners on 'Enterprise'
        db.create_table(u'enterprise_enterprise_owners', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('enterprise', models.ForeignKey(orm[u'enterprise.enterprise'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'enterprise_enterprise_owners', ['enterprise_id', 'user_id'])

        # Adding model 'ActionRecord'
        db.create_table(u'enterprise_actionrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enterprise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enterprise.Enterprise'])),
            ('when_igt', self.gf('django.db.models.fields.DateTimeField')()),
            ('when_irl', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'enterprise', ['ActionRecord'])

        # Adding model 'Transaction'
        db.create_table(u'enterprise_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enterprise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['enterprise.Enterprise'])),
            ('when_igt', self.gf('django.db.models.fields.DateTimeField')()),
            ('when_irl', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('acc_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'enterprise', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Universe'
        db.delete_table(u'enterprise_universe')

        # Deleting model 'Enterprise'
        db.delete_table(u'enterprise_enterprise')

        # Removing M2M table for field owners on 'Enterprise'
        db.delete_table('enterprise_enterprise_owners')

        # Deleting model 'ActionRecord'
        db.delete_table(u'enterprise_actionrecord')

        # Deleting model 'Transaction'
        db.delete_table(u'enterprise_transaction')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'enterprise.actionrecord': {
            'Meta': {'ordering': "['-when_irl']", 'object_name': 'ActionRecord'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enterprise.Enterprise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when_igt': ('django.db.models.fields.DateTimeField', [], {}),
            'when_irl': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'enterprise.enterprise': {
            'Meta': {'object_name': 'Enterprise'},
            'created_igt': ('django.db.models.fields.DateTimeField', [], {}),
            'created_irl': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owners': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'start_cash': ('django.db.models.fields.IntegerField', [], {}),
            'universe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enterprise.Universe']"})
        },
        u'enterprise.transaction': {
            'Meta': {'ordering': "['-when_irl']", 'object_name': 'Transaction'},
            'acc_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'enterprise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['enterprise.Enterprise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when_igt': ('django.db.models.fields.DateTimeField', [], {}),
            'when_irl': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'enterprise.universe': {
            'Meta': {'object_name': 'Universe'},
            'current_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['enterprise']