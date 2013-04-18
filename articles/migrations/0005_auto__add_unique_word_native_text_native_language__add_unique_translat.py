# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Word', fields ['native_text', 'native_language']
        db.create_unique('articles_word', ['native_text', 'native_language_id'])

        # Adding unique constraint on 'TranslatedPhrase', fields ['second_native', 'first_native', 'third_target', 'third_native', 'second_target', 'first_target']
        db.create_unique('articles_translatedphrase', ['second_native_id', 'first_native_id', 'third_target_id', 'third_native_id', 'second_target_id', 'first_target_id'])


        # Changing field 'PhraseInTranslation.end_punctuation'
        db.alter_column('articles_phraseintranslation', 'end_punctuation', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Changing field 'PhraseInTranslation.start_punctuation'
        db.alter_column('articles_phraseintranslation', 'start_punctuation', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))
        # Adding unique constraint on 'PhraseInTranslation', fields ['phrase', 'part_of', 'displays_as', 'position']
        db.create_unique('articles_phraseintranslation', ['phrase_id', 'part_of_id', 'displays_as_id', 'position'])

        # Adding unique constraint on 'Translation', fields ['original_article', 'target_language']
        db.create_unique('articles_translation', ['original_article_id', 'target_language_id'])

        # Adding unique constraint on 'Stem', fields ['native_text', 'native_language']
        db.create_unique('articles_stem', ['native_text', 'native_language_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Stem', fields ['native_text', 'native_language']
        db.delete_unique('articles_stem', ['native_text', 'native_language_id'])

        # Removing unique constraint on 'Translation', fields ['original_article', 'target_language']
        db.delete_unique('articles_translation', ['original_article_id', 'target_language_id'])

        # Removing unique constraint on 'PhraseInTranslation', fields ['phrase', 'part_of', 'displays_as', 'position']
        db.delete_unique('articles_phraseintranslation', ['phrase_id', 'part_of_id', 'displays_as_id', 'position'])

        # Removing unique constraint on 'TranslatedPhrase', fields ['second_native', 'first_native', 'third_target', 'third_native', 'second_target', 'first_target']
        db.delete_unique('articles_translatedphrase', ['second_native_id', 'first_native_id', 'third_target_id', 'third_native_id', 'second_target_id', 'first_target_id'])

        # Removing unique constraint on 'Word', fields ['native_text', 'native_language']
        db.delete_unique('articles_word', ['native_text', 'native_language_id'])


        # Changing field 'PhraseInTranslation.end_punctuation'
        db.alter_column('articles_phraseintranslation', 'end_punctuation', self.gf('django.db.models.fields.CharField')(default='', max_length=4))

        # Changing field 'PhraseInTranslation.start_punctuation'
        db.alter_column('articles_phraseintranslation', 'start_punctuation', self.gf('django.db.models.fields.CharField')(default='', max_length=4))

    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'}),
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
            'Meta': {'unique_together': "(('part_of', 'phrase', 'position', 'displays_as'),)", 'object_name': 'PhraseInTranslation'},
            'displays_as': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.LayoutElement']"}),
            'end_punctuation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Translation']"}),
            'phrase': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.TranslatedPhrase']"}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'previous': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'next'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['articles.PhraseInTranslation']"}),
            'start_punctuation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'articles.stem': {
            'Meta': {'unique_together': "(('native_text', 'native_language'),)", 'object_name': 'Stem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Stem']"}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        }
    }

    complete_apps = ['articles']