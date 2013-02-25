# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WordInArticle.prev'
        db.alter_column('rss_wordinarticle', 'prev_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['rss.WordInArticle']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'WordInArticle.prev'
        raise RuntimeError("Cannot reverse this migration. 'WordInArticle.prev' and its values cannot be restored.")

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