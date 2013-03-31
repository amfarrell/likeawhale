from itertools import chain
from translate import word_tokenize
from translate import sent_tokenize #wordpunct_tokenize
from translate import SnowballStemmer
from translate import translate_word


import apiclient.discovery

from django.db import models
from django.db.models import permalink


from settings import GOOGLE_TRANSLATE_API_KEY


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

  def scentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [Word.objects.get_or_create(native_language = self.native_language, native_text = text)
              for text in chain.from_iterable([word_tokenize(t) for t in self.scentences()])]

  def translate_to(self, target_langauge = 'en', force = False):
    raise NotImplementedError
    if target_langauge.code != 'en':
      raise NotImplementedError("Only English translation for now.")
    if type(target_langauge) is str:
      target_langauge = Language.objects.get(code = target_langauge)
    trans = Translation.objects.filter(original_article = self, target_langauge = target_langauge)
    if force:
      trans.delete()
    if trans.exists():
      return trans.get()
    else:
      return self._translate(target_langauge)

  def _translate(self, target_language):
    elements = [LayoutElement(article = self, previous = None, position = 0, text = self.text, element_type = 'PARAGRAPH'), ]
    words = self.words() #TODO: make this use iterators.
    translation = Translation.objects.create(original_article = self, target_language = target_language)
    phrases = [word.translate_to(target_language) for word in words]
    phrases_in_translation = [None,]
    for phrase, position in enumerate(phrases):
      phrases_in_translation.append(PhraseInTranslation.objects.create(
        displays_as = elements[0], #TODO: actually pay attention to elements.
        previous_phrase = phrases_in_translation[-1], 
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


class Translation(models.Model):
  """
  An article prepared to be read by someone in a foreign language.
  """
  original_article = models.ForeignKey(Article)
  target_langauge = models.ForeignKey(Language)

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.original_article.slug, 'code' : self.original_article.native_language.code})

class Stem(models.Model):
  native_text = models.CharField(max_length = 124)
  native_language = models.ForeignKey('articles.Language')
  def __unicode__(self):
    return "%s" % self.native_text

  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

class WordManager(models.Manager):
  def process_kwargs(self, **kwargs):
    if type(kwargs['native_language']) is str:
      kwargs['native_langauge'] = Language.objects.get(code = kwargs['native_langauge'])
    if kwargs.get('native_stem', None) is None:
      native_stemmer = SnowballStemmer(kwargs['native_language'].name.lower())
      kwargs['native_stem'] = Stem.objects.get_or_create(native_language = kwargs['native_language'], native_text = native_stemmer.stem(kwargs['native_text']))
    return kwargs

  def create(self, **kwargs):
    return self.get_query_set().get_or_create(**self.process_kwargs(kwargs))

  def get(self, **kwargs):
    return self.get_query_set().get_or_create(**self.process_kwargs(kwargs))

class Word(models.Model):
  native_text = models.CharField(max_length = 124)
  native_stem = models.ForeignKey(Stem)
  native_language = models.ForeignKey('articles.Language')
  objects = WordManager()

  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

  def __unicode__(self):
    return "%s" % self.native_text

  def translate_to(self, target_language = 'en'):
    if type(target_language) is str:
      target_language = Language.objects.get(code = target_language)
    target_text = translate_word(self.native_text, self.native_language.code, target_language.code)
    target_stemmer = SnowballStemmer(target_language.name.lower())
    target_stem = Stem.objects.create(native_language = target_language, native_text = target_stemmer.stem(target_text))
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
    return '[%s] %s -> [%s] %s' % (self.represents_first.native_language.code, self.source_text(),
                                           self.using_first.native_language.code, self.resulting_text())


class PhraseInTranslation(models.Model):
  displays_as = models.ForeignKey(LayoutElement)
  previous = models.ForeignKey('self', related_name = 'next', null = True, blank = True, on_delete = models.SET_NULL)
  part_of = models.ForeignKey(Translation)
  #TODO: Constraint that the translation's article is the same as the layout's article.
  phrase = models.ForeignKey(TranslatedPhrase)
  end_punctuation = models.CharField(max_length = 4, null = True, blank = True)
  start_punctuation = models.CharField(max_length = 4, null = True, blank = True)
  position = models.IntegerField() #TODO: add a check that the previous always has a position lower by 1 and is part of the same document.
