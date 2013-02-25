# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Word.native_stem'
        db.add_column('rss_word', 'native_stem',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=124),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Word.native_stem'
        db.delete_column('rss_word', 'native_stem')


    models = {
        'rss.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
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
        'rss.parsedarticle': {
            'Meta': {'object_name': 'ParsedArticle'},
            'dest_lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Language']"}),
            'first_word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Word']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Article']"})
        },
        'rss.word': {
            'Meta': {'object_name': 'Word'},
            'english_text': ('django.db.models.fields.CharField', [], {'max_length': '124'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Language']"}),
            'native_stem': ('django.db.models.fields.CharField', [], {'max_length': '124'}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        },
        'rss.wordinarticle': {
            'Meta': {'object_name': 'WordInArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.ParsedArticle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prev': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'to': "orm['rss.WordInArticle']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rss.Word']"})
        }
    }

    complete_apps = ['rss']