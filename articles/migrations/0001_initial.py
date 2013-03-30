# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('articles_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('articles', ['Language'])

        # Adding model 'Article'
        db.create_table('articles_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=124)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=124)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('source_url', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('source_lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Language'])),
        ))
        db.send_create_signal('articles', ['Article'])

        # Adding model 'LayoutElement'
        db.create_table('articles_layoutelement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
            ('previous', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next', null=True, on_delete=models.SET_NULL, to=orm['articles.LayoutElement'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('element_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('articles', ['LayoutElement'])

        # Adding model 'Translation'
        db.create_table('articles_translation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Article'])),
            ('dest_lang', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Language'])),
        ))
        db.send_create_signal('articles', ['Translation'])

        # Adding model 'Stem'
        db.create_table('articles_stem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('native_text', self.gf('django.db.models.fields.CharField')(max_length=124)),
            ('native_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Language'])),
        ))
        db.send_create_signal('articles', ['Stem'])

        # Adding model 'Word'
        db.create_table('articles_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('native_text', self.gf('django.db.models.fields.CharField')(max_length=124)),
            ('native_stem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Stem'])),
            ('native_language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Language'])),
        ))
        db.send_create_signal('articles', ['Word'])

        # Adding model 'TranslatedPhrase'
        db.create_table('articles_translatedphrase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('represents_first', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_represented_by', to=orm['articles.Word'])),
            ('represents_second', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_represented_by', null=True, to=orm['articles.Word'])),
            ('represents_third', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_represented_by', null=True, to=orm['articles.Word'])),
            ('using_first', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_in_phrase', to=orm['articles.Word'])),
            ('using_second', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_in_phrase', null=True, to=orm['articles.Word'])),
            ('using_third', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='third_in_phrase', null=True, to=orm['articles.Word'])),
        ))
        db.send_create_signal('articles', ['TranslatedPhrase'])

        # Adding model 'PhraseInTranslation'
        db.create_table('articles_phraseintranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('displays_as', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.LayoutElement'])),
            ('previous', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='next', null=True, on_delete=models.SET_NULL, to=orm['articles.PhraseInTranslation'])),
            ('part_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Translation'])),
            ('phrase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.TranslatedPhrase'])),
            ('end_punctuation', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('start_punctuation', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('articles', ['PhraseInTranslation'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table('articles_language')

        # Deleting model 'Article'
        db.delete_table('articles_article')

        # Deleting model 'LayoutElement'
        db.delete_table('articles_layoutelement')

        # Deleting model 'Translation'
        db.delete_table('articles_translation')

        # Deleting model 'Stem'
        db.delete_table('articles_stem')

        # Deleting model 'Word'
        db.delete_table('articles_word')

        # Deleting model 'TranslatedPhrase'
        db.delete_table('articles_translatedphrase')

        # Deleting model 'PhraseInTranslation'
        db.delete_table('articles_phraseintranslation')


    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '124'}),
            'source_lang': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'source_url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'represents_first': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_represented_by'", 'to': "orm['articles.Word']"}),
            'represents_second': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_represented_by'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'represents_third': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_represented_by'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'using_first': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_in_phrase'", 'to': "orm['articles.Word']"}),
            'using_second': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_in_phrase'", 'null': 'True', 'to': "orm['articles.Word']"}),
            'using_third': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'third_in_phrase'", 'null': 'True', 'to': "orm['articles.Word']"})
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