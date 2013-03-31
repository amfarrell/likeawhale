# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Article', fields ['source_url']
        db.create_unique('articles_article', ['source_url'])


    def backwards(self, orm):
        # Removing unique constraint on 'Article', fields ['source_url']
        db.delete_unique('articles_article', ['source_url'])


    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'}),
            'source_lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'source_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'})
        },
        'articles.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'articles.layoutelement': {
            'Meta': {'object_name': 'LayoutElement'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['articles.LayoutElement']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'articles.phraseintranslation': {
            'Meta': {'object_name': 'PhraseInTranslation'},
            'displays_as': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.LayoutElement']"}),
            'end_punctuation': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Translation']"}),
            'phrase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.TranslatedPhrase']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['articles.PhraseInTranslation']"}),
            'start_punctuation': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'articles.stem': {
            'Meta': {'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        },
        'articles.translatedphrase': {
            'Meta': {'object_name': 'TranslatedPhrase'},
            'first_native': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_native_in'", 'to': "orm['articles.Word']"}),
            'first_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_target_in'", 'to': "orm['articles.Word']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_native': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_native_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'second_target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_target_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'third_native': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_native_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'third_target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_target_in'", 'null': 'True', 'to': "orm['articles.Word']"})
        },
        'articles.translation': {
            'Meta': {'object_name': 'Translation'},
            'dest_lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"})
        },
        'articles.word': {
            'Meta': {'object_name': 'Word'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Stem']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        }
    }

    complete_apps = ['articles']