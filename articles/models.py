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
  source_lang = models.ForeignKey('articles.Language')

  def scentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [i for i in chain.from_iterable([word_tokenize(t) for t in self.scentences()])]

  def parsed_article(self, target_langauge = 'en', force = False):
    raise NotImplementedError
    if target_langauge != 'en':
      raise NotImplementedError("Only English translation for now.")
    target_langauge = Language.objects.get(code = target_langauge) #TODO: make this resilient.
    trans = Translation.objects.filter(original_article = self, target_langauge = target_langauge)
    if force:
      trans.delete()
    if trans.exists():
      return trans.get()
    else:
      return self.translate(target_langauge)


  def translate(self, target_langauge = 'en'):
    if type(target_langauge) is str:
      target_langauge = Language.objects.get(code = target_langauge)
    if target_langauge.code != 'en':
      raise NotImplementedError("Only English translation for now.")
    # todo:
    target_langauge = Language.objects.get(code = target_langauge.code)
    tokens = self.words() #TODO: make this use iterators.
    pass
#    stemmer = SnowballStemmer(self.source_lang.name.lower())
#    length = len(tokens)
#    i = 0
#    old_index = None
#    translation = Translation.objects.create(original_article = self, target_langauge = target_langauge)
#
#    while i < length:
#      current_text = tokens[i]
#      current_stem = stemmer.stem(current_text)
#      current_word = Word.objects.filter(native_text = current_text, native_language = self.source_lang)
#      if current_word.count() == 0:
#        current_word = Word.objects.create(native_text = current_text, native_language = self.source_lang, native_stem = current_stem, english_text = current_stem)
#      else:
#        current_word = current_word.get()
#
#      if i == 0:
#        pa = Translation.objects.create(original_article = self, target_langauge = target_langauge, first_word = current_word)
#      #if bool(old_index): 
#      #  current_index = WordInArticle.objects.create(word_id = current_word.id, article_id = pa.id, prev_id = old_index.id)
#      #else:
#      #  current_index = WordInArticle.objects.create(word = current_word, article = pa)
#
#      #old_index = current_index
#      i += 1
#
#    pa.save()
#    return pa

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
  target_langauge = models.ForeignKey(Language)

  @permalink
  def get_absolute_url(self):
    return ('articles.views.view_article', None, {'slug': self.original_article.slug, 'code' : self.original_article.source_lang.code})

class Stem(models.Model):
  native_text = models.CharField(max_length = 124)
  native_language = models.ForeignKey('articles.Language')
  def __unicode__(self):
    return "%s" % self.native_text

  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

class Word(models.Model):
  native_text = models.CharField(max_length = 124)
  native_stem = models.ForeignKey(Stem)
  native_language = models.ForeignKey('articles.Language')
  def __repr__(self):
    return "[%s] %s" % (self.native_language.code, self.native_text)

  def __unicode__(self):
    return "%s" % self.native_text

  def translate_to(self, target_language = 'en'):
    if type(target_language) is str:
      target_language = Language.objects.get(code = target_language)
    target_text = translate_word(self.native_text, self.native_language.code, target_language.code)
    target_stemmer = SnowballStemmer(target_language.name.lower())
    target_stem = target_stem = Stem.objects.create(native_language = target_language, native_text = target_stemmer.stem(target_text))
    result = Word.objects.get_or_create(native_text = target_text, native_stem = target_stem, native_language = target_language)[0]
    #TranslatedPhrase.objects.create(first_target = result, first_native = self)
    return result

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
  end_punctuation = models.CharField(max_length = 4)
  start_punctuation = models.CharField(max_length = 4)
  position = models.IntegerField() #TODO: add a check that the previous always has a position lower by 1 and is part of the same document.
