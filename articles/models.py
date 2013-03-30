from django.db import models
from django.db.models import permalink

from itertools import chain
from nltk import word_tokenize
from nltk import sent_tokenize #wordpunct_tokenize
from nltk import SnowballStemmer

class Language(models.Model):
  code = models.CharField(max_length = 8, unique = True) #TODO: add index based on this
  name = models.CharField(max_length = 32, unique = True)

  def __unicode__(self):
    return '%s' % self.name

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_language', None, {'code': self.code})

class Article(models.Model):
  title = models.CharField(max_length = 124, unique = True)
  slug = models.CharField(max_length = 124, unique = True)#TODO: add index based on this
  body = models.TextField()
  source_url = models.CharField(max_length = 2048) #TODO: add index based on this
  source_lang = models.ForeignKey('articles.Language')

  def scentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [i for i in chain.from_iterable([word_tokenize(t) for t in self.scentences()])]

  def __unicode__(self):
    return '%s' % self.title

  def parsed_article(self, dest_lang = 'en'):
    raise NotImplementedError
    if dest_lang != 'en':
      raise NotImplementedError("Only English translation for now.")
    dest_lang = Language.objects.get(code = dest_lang) #TODO: make this resilient.
    pa = Translation.objects.filter(original_article = self, dest_lang = dest_lang)
    if pa.count():
      return pa.get()
    else:
      return self.parse(dest_lang)


  def parse(self, dest_lang = 'en'):
    raise NotImplementedError
    if dest_lang != 'en':
      raise NotImplementedError("Only English translation for now.")
    # todo:
    dest_lang = Language.objects.get(code = dest_lang) #TODO: make this resilient.
    tokens = self.words() #TODO: make this user iterators.
    stemmer = SnowballStemmer(self.source_lang.name.lower())
    length = len(tokens)
    i = 0
    #old_index = None
    pa = None

    while i < length:
      current_text = tokens[i]
      current_stem = stemmer.stem(current_text)
      current_word = Word.objects.filter(native_text = current_text, native_language = self.source_lang)
      if current_word.count() == 0:
        current_word = Word.objects.create(native_text = current_text, native_language = self.source_lang, native_stem = current_stem, english_text = current_stem)
      else:
        current_word = current_word.get()

      if i == 0:
        pa = Translation.objects.create(original_article = self, dest_lang = dest_lang, first_word = current_word)
      #if bool(old_index): 
      #  current_index = WordInArticle.objects.create(word_id = current_word.id, article_id = pa.id, prev_id = old_index.id)
      #else:
      #  current_index = WordInArticle.objects.create(word = current_word, article = pa)

      #old_index = current_index
      i += 1

    pa.save()
    return pa

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.slug, 'code' : self.source_lang.code})

ELEMENT_TYPES = (('CAPTION', 'caption'), ('TITLE', 'title'), ('SUBTITLE', 'subtitle'), ('BLOCKQUOTE', 'blockquote'), ('PARAGRAPH', 'paragraph'))
class LayoutElement(models.Model):
  """An element in the display of the text of the article. Contains styling info and text"""
  article = models.ForeignKey(Article)
  previous = models.ForeignKey('self', related_name = 'next', null = True, blank = True, on_delete = models.SET_NULL)
  position = models.IntegerField() #TODO: add a check that the previous always has a position lower by 1 and is part of the same document.
  text = models.TextField()
  element_type = models.CharField(
    choices = ELEMENT_TYPES,
    max_length = 10
  )
  #TODO: add images


class Translation(models.Model):
  """
  An article prepared to be read by someone in a foreign language.
  """
  original_article = models.ForeignKey(Article)
  dest_lang = models.ForeignKey(Language) #TODO: add en as default.

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.original_article.slug, 'code' : self.original_article.source_lang.code})

class Stem(models.Model):
  native_text = models.CharField(max_length = 124)
  native_language = models.ForeignKey('articles.Language')

class Word(models.Model):
  native_text = models.CharField(max_length = 124)
  native_stem = models.ForeignKey(Stem)
  native_language = models.ForeignKey('articles.Language')

class TranslatedPhrase(models.Model):
  #TODO: constrain that these words are all the same language.
  represents_first = models.ForeignKey(Word, related_name = "first_represented_by")
  represents_second = models.ForeignKey(Word, related_name = "second_represented_by", null = True, blank = True)
  represents_third = models.ForeignKey(Word, related_name = "third_represented_by", null = True, blank = True)
  #TODO: constrain that these words are all the same language.
  using_first = models.ForeignKey(Word, related_name = "first_in_phrase")
  using_second = models.ForeignKey(Word, related_name = "second_in_phrase", null = True, blank = True)
  using_third = models.ForeignKey(Word, related_name = "third_in_phrase", null = True, blank = True)

class PhraseInTranslation(models.Model):
  displays_as = models.ForeignKey(LayoutElement)
  previous = models.ForeignKey('self', related_name = 'next', null = True, blank = True, on_delete = models.SET_NULL)
  part_of = models.ForeignKey(Translation)
  #TODO: Constraint that the translation's article is the same as the layout's article.
  phrase = models.ForeignKey(TranslatedPhrase)
  end_punctuation = models.CharField(max_length = 4)
  start_punctuation = models.CharField(max_length = 4)
  position = models.IntegerField() #TODO: add a check that the previous always has a position lower by 1 and is part of the same document.
