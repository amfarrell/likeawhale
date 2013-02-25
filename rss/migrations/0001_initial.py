# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('rss_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('rss', ['Language'])

        # Adding model 'Article'
        db.create_table('rss_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=124)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=124)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('source_lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Language'])),
            ('first_word', self.gf('django.db.models.fields.related.ForeignKey')(related_name='is_start_of', to=orm['rss.WordInArticle'])),
        ))
        db.send_create_signal('rss', ['Article'])

        # Adding model 'Word'
        db.create_table('rss_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('native_text', self.gf('django.db.models.fields.CharField')(max_length=124)),
            ('native_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Language'])),
            ('english_text', self.gf('django.db.models.fields.CharField')(max_length=124)),
        ))
        db.send_create_signal('rss', ['Word'])

        # Adding model 'WordInArticle'
        db.create_table('rss_wordinarticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Word'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rss.Article'])),
            ('prev', self.gf('django.db.models.fields.related.ForeignKey')(related_name='next', to=orm['rss.WordInArticle'])),
        ))
        db.send_create_signal('rss', ['WordInArticle'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table('rss_language')

        # Deleting model 'Article'
        db.delete_table('rss_article')

        # Deleting model 'Word'
        db.delete_table('rss_word')

        # Deleting model 'WordInArticle'
        db.delete_table('rss_wordinarticle')


    models = {
        'rss.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'first_word': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'is_start_of'", 'to': "orm['rss.WordInArticle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'}),
            'source_lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Language']"}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'})
        },
        'rss.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'rss.word': {
            'Meta': {'object_name': 'Word'},
            'english_text': ('django.db.models.fields.CharField', [], {'max_length': '124'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Language']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        },
        'rss.wordinarticle': {
            'Meta': {'object_name': 'WordInArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Article']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'next'", 'to': "orm['rss.WordInArticle']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Word']"})
        }
    }

    complete_apps = ['rss']