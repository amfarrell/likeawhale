from itertools import chain
from translate import word_tokenize
from translate import sent_tokenize #wordpunct_tokenize
from translate import SnowballStemmer
from translate import translate_word
from sys import stdout


import apiclient.discovery

from django.db import models
from django.db.models import permalink


from settings import GOOGLE_TRANSLATE_API_KEY
from settings import DEBUG


service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)

def ifthere(word):
  if word is None:
    return ''
  else:
    return ' %s' % word

class Language(models.Model):
  code = models.CharField(max_length = 8, unique = True)
  name = models.CharField(max_length = 32, unique = True)

  def __unicode__(self):
    return '%s' % self.name

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_language', None, {'code': self.code})

class Article(models.Model):
  title = models.CharField(max_length = 124, unique = True)
  slug = models.CharField(max_length = 124, unique = True)
  body = models.TextField()
  source_url = models.CharField(max_length = 2048, unique = True)
  native_language = models.ForeignKey('articles.Language')

  def sentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [Word.objects.get_or_create(native_language = self.native_language, native_text = text)[0]
              for text in chain.from_iterable([word_tokenize(t) for t in self.sentences()])]

  def translated_to(self, target_language = 'en', force = False):
    if isinstance(target_language, basestring) :
      target_language = Language.objects.get(code = target_language)
    trans = Translation.objects.filter(original_article = self, target_language = target_language)
    if force:
      trans.delete()
    if trans.exists():
      return trans.get()
    else:
      return self._translate(target_language)

  def _translate(self, target_language):
    LayoutElement.objects.filter(article = self, previous = None, position = 0, text = self.body, element_type = 'PARAGRAPH').delete()
    elements = [LayoutElement.objects.create(article = self, previous = None, position = 0, text = self.body, element_type = 'PARAGRAPH'), ]
    words = self.words() #TODO: make this use iterators.
    translation = Translation.objects.get_or_create(original_article = self, target_language = target_language)[0]
    phrases = [word.translated_to(target_language) for word in words]
    phrases_in_translation = [None,]
    for position, phrase in enumerate(phrases):
      phrases_in_translation.append(PhraseInTranslation.objects.create(
        displays_as = elements[0], #TODO: actually pay attention to elements.
        previous = phrases_in_translation[-1], 
        part_of = translation,
        position = position,
        phrase = phrase,
        start_punctuation = '', #TODO: actually pay attention to punctuation.
        end_punctuation = ''
      ))
    return translation

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.slug, 'code' : self.native_language.code})

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
  class Meta:
    unique_together = ('article', 'text', 'position', 'element_type')
    ordering = ['position']
    order_with_respect_to = 'article'


class Translation(models.Model):
  """
  An article prepared to be read by someone in a foreign language.
  """
  original_article = models.ForeignKey(Article)
  target_language = models.ForeignKey(Language)

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.original_article.slug, 'code' : self.original_article.native_language.code})

  class Meta:
    unique_together = ('original_article', 'target_language',)

class Stem(models.Model):
  native_text = models.CharField(max_length = 124)
  native_language = models.ForeignKey('articles.Language')
  def __unicode__(self):
    return "%s" % self.native_text

  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

  class Meta:
    unique_together = ('native_text', 'native_language',)

class WordManager(models.Manager):
  def _process_kwargs(self, kwargs):
    if isinstance(kwargs['native_language'], basestring) :
      kwargs['native_language'] = Language.objects.get(code = kwargs['native_language'])
    if kwargs.get('native_stem', None) is None:
      native_stemmer = SnowballStemmer(kwargs['native_language'].name.lower())
      kwargs['native_stem'] = Stem.objects.get_or_create(native_language = kwargs['native_language'], native_text = native_stemmer.stem(kwargs['native_text']))[0]
    return kwargs

  def create(self, **kwargs):
    return self.get_query_set().get_or_create(**self._process_kwargs(kwargs))

  def get_or_create(self, **kwargs):
    return self.get_query_set().get_or_create(**self._process_kwargs(kwargs))

class Word(models.Model):
  native_text = models.CharField(max_length = 124)
  native_stem = models.ForeignKey(Stem)
  native_language = models.ForeignKey('articles.Language')
  objects = WordManager()

  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

  def __unicode__(self):
    return "%s" % self.native_text

  class Meta:
    unique_together = ('native_text', 'native_language',)

  def translated_to(self, target_language = 'en'):
    if isinstance(target_language, basestring) :
      target_language = Language.objects.get(code = target_language)
    possible = TranslatedPhrase.objects.filter(first_native = self, second_native = None, third_native = None, first_target__native_language = target_language)
    if possible.exists():
      if DEBUG:
        stdout.write(".")
      return possible.get()
    else:
      if DEBUG:
        stdout.write("|")
      target_text = translate_word(self.native_text, self.native_language.code, target_language.code)
      target_stemmer = SnowballStemmer(target_language.name.lower())
      target_stem = Stem.objects.get_or_create(native_language = target_language, native_text = target_stemmer.stem(target_text))[0]
      result = Word.objects.get_or_create(native_text = target_text, native_stem = target_stem, native_language = target_language)[0]
      translation = TranslatedPhrase.objects.create(first_target = result, first_native = self)
      return translation

class TranslatedPhrase(models.Model):
  #TODO: constrain that these words are all the same language.
  first_target = models.ForeignKey(Word, related_name = "first_target_in")
  second_target = models.ForeignKey(Word, related_name = "second_target_in", null = True, blank = True)
  third_target = models.ForeignKey(Word, related_name = "third_target_in", null = True, blank = True)
  #TODO: constrain that these words are all the same language.
  first_native = models.ForeignKey(Word, related_name = "first_native_in")
  second_native = models.ForeignKey(Word, related_name = "second_native_in", null = True, blank = True)
  third_native = models.ForeignKey(Word, related_name = "third_native_in", null = True, blank = True)

  def source_text(self):
    return '%s%s%s' % (self.first_native, ifthere(self.second_native), ifthere(self.third_native))

  def resulting_text(self):
    return '%s%s%s' % (self.first_target, ifthere(self.second_target), ifthere(self.third_target))

  def __unicode__(self):
    return '[%s] %s -> [%s] %s' % (self.first_target.native_language.code, self.source_text(),
                                           self.first_native.native_language.code, self.resulting_text())
  class Meta:
    unique_together = ('first_target', 'second_target', 'third_target', 
                       'first_native', 'second_native', 'third_native')


class PhraseInTranslation(models.Model):
  displays_as = models.ForeignKey(LayoutElement)
  previous = models.ForeignKey('self', related_name = 'next', null = True, blank = True, on_delete = models.SET_NULL)
  part_of = models.ForeignKey(Translation)
  #TODO: Constraint that the translation's article is the same as the layout's article.
  phrase = models.ForeignKey(TranslatedPhrase)
  end_punctuation = models.CharField(max_length = 4, null = True, blank = True, default = '')
  start_punctuation = models.CharField(max_length = 4, null = True, blank = True, default = '')
  position = models.IntegerField() #TODO: add a check that the previous always has a position lower by 1 and is part of the same document.

  class Meta:
    unique_together = ('part_of', 'phrase', 'position', 'displays_as')
    ordering = ['position']
    order_with_respect_to = 'part_of'
