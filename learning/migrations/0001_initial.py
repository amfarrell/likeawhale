# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserLanguageKnowledge'
        db.create_table('accounts_userlanguageknowledge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Language'])),
            ('mastery_level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_lookup', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('lookup_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('accounts', ['UserLanguageKnowledge'])

        # Adding unique constraint on 'UserLanguageKnowledge', fields ['user', 'language']
        db.create_unique('accounts_userlanguageknowledge', ['user_id', 'language_id'])

        # Adding model 'UserWordKnowledge'
        db.create_table('accounts_userwordknowledge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Word'])),
            ('mastery_level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_lookup', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('lookup_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('accounts', ['UserWordKnowledge'])

        # Adding unique constraint on 'UserWordKnowledge', fields ['user', 'word']
        db.create_unique('accounts_userwordknowledge', ['user_id', 'word_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserWordKnowledge', fields ['user', 'word']
        db.delete_unique('accounts_userwordknowledge', ['user_id', 'word_id'])

        # Removing unique constraint on 'UserLanguageKnowledge', fields ['user', 'language']
        db.delete_unique('accounts_userlanguageknowledge', ['user_id', 'language_id'])

        # Deleting model 'UserLanguageKnowledge'
        db.delete_table('accounts_userlanguageknowledge')

        # Deleting model 'UserWordKnowledge'
        db.delete_table('accounts_userwordknowledge')


    models = {
        'accounts.userlanguageknowledge': {
            'Meta': {'unique_together': "(('user', 'language'),)", 'object_name': 'UserLanguageKnowledge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'last_lookup': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lookup_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mastery_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'accounts.userwordknowledge': {
            'Meta': {'unique_together': "(('user', 'word'),)", 'object_name': 'UserWordKnowledge'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_lookup': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'lookup_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mastery_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Word']"})
        },
        'articles.language': {
            'Meta': {'object_name': 'Language'},
            '_has_stemmer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'articles.stem': {
            'Meta': {'unique_together': "(('native_text', 'native_language'),)", 'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        },
        'articles.word': {
            'Meta': {'unique_together': "(('native_text', 'native_language'),)", 'object_name': 'Word'},
            'difficulty': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Stem']", 'null': 'True', 'blank': 'True'}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']