# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserWordKnowledge'
        db.delete_table('articles_userwordknowledge')


        # Changing field 'Word.native_stem'
        db.alter_column('articles_word', 'native_stem_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Stem'], null=True))
        # Adding field 'Language._has_stemmer'
        db.add_column('articles_language', '_has_stemmer',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'UserWordKnowledge'
        db.create_table('articles_userwordknowledge', (
            ('mastery_level', self.gf('django.db.models.fields.IntegerField')()),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('word_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.Word'])),
        ))
        db.send_create_signal('articles', ['UserWordKnowledge'])


        # Changing field 'Word.native_stem'
        db.alter_column('articles_word', 'native_stem_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['articles.Stem']))
        # Deleting field 'Language._has_stemmer'
        db.delete_column('articles_language', '_has_stemmer')


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
            '_has_stemmer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'articles.layoutelement': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('article', 'text', 'position', 'element_type'),)", 'object_name': 'LayoutElement'},
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
            'difficulty': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'native_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Language']"}),
            'native_stem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.Stem']", 'null': 'True', 'blank': 'True'}),
            'native_text': ('django.db.models.fields.CharField', [], {'max_length': '124'})
        }
    }

    complete_apps = ['articles']