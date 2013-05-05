# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Word.wikipedia_link'
        db.add_column('articles_word', 'wikipedia_link',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Word'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Word.has_wikipedia_link'
        db.add_column('articles_word', 'has_wikipedia_link',
                      self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Word.wikipedia_link'
        db.delete_column('articles_word', 'wikipedia_link_id')

        # Deleting field 'Word.has_wikipedia_link'
        db.delete_column('articles_word', 'has_wikipedia_link')


    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'source_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        'articles.language': {
            'Meta': {'object_name': 'Language'},
            '_has_stemmer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'alphabetic': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'articles.layoutelement': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('article', 'position', 'element_type'),)", 'object_name': 'LayoutElement'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'element_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['articles.LayoutElement']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'articles.phraseintranslation': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('part_of', 'phrase', 'position', 'displays_as'),)", 'object_name': 'PhraseInTranslation'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'displays_as': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.LayoutElement']"}),
            'end_punctuation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Translation']"}),
            'phrase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.TranslatedPhrase']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['articles.PhraseInTranslation']"}),
            'start_punctuation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'articles.stem': {
            'Meta': {'unique_together': "(('native_text', 'native_language'),)", 'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'articles.translatedphrase': {
            'Meta': {'unique_together': "(('first_target', 'second_target', 'third_target', 'first_native', 'second_native', 'third_native'),)", 'object_name': 'TranslatedPhrase'},
            'first_native': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_native_in'", 'to': "orm['articles.Word']"}),
            'first_target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_target_in'", 'to': "orm['articles.Word']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'second_native': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_native_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'second_target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_target_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'third_native': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_native_in'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'third_target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_target_in'", 'null': 'True', 'to': "orm['articles.Word']"})
        },
        'articles.translation': {
            'Meta': {'unique_together': "(('original_article', 'target_language'),)", 'object_name': 'Translation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Article']"}),
            'target_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"})
        },
        'articles.word': {
            'Meta': {'unique_together': "(('native_text', 'native_language'),)", 'object_name': 'Word'},
            'difficulty': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'has_wikipedia_link': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Stem']", 'null': 'True', 'blank': 'True'}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'wikipedia_link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Word']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['articles']