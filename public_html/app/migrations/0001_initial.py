# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Book'
        db.create_table(u'app_book', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('pub_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('quantity', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('available', self.gf('django.db.models.fields.BigIntegerField')(default=True)),
            ('test', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'app', ['Book'])

        # Adding model 'Member'
        db.create_table(u'app_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('contactNo', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('member_since', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('membership_type', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('hasBooks', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('request', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'app', ['Member'])

        # Adding model 'Books_Issued'
        db.create_table(u'app_books_issued', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Member'])),
            ('isbn', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['app.Book'])),
            ('issue_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('due_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2015, 7, 7, 0, 0))),
            ('fine', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('issued', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
        ))
        db.send_create_signal(u'app', ['Books_Issued'])


    def backwards(self, orm):
        # Deleting model 'Book'
        db.delete_table(u'app_book')

        # Deleting model 'Member'
        db.delete_table(u'app_member')

        # Deleting model 'Books_Issued'
        db.delete_table(u'app_books_issued')


    models = {
        u'app.book': {
            'Meta': {'ordering': "['-title']", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'available': ('django.db.models.fields.BigIntegerField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'quantity': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'test': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'app.books_issued': {
            'Meta': {'object_name': 'Books_Issued'},
            'due_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2015, 7, 7, 0, 0)'}),
            'fine': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Book']"}),
            'issue_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'issued': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'user_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Member']"})
        },
        u'app.member': {
            'Meta': {'object_name': 'Member'},
            'contactNo': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'dob': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'hasBooks': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member_since': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'membership_type': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'request': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']