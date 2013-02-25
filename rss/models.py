from django.db import models
from django.db.models import permalink

from nltk import word_tokenize, sent_tokenize #wordpunct_tokenize
from itertools import chain
from nltk import SnowballStemmer

class Language(models.Model):
  code = models.CharField(max_length = 8, unique = True) #TODO: add index based on this
  name = models.CharField(max_length = 32, unique = True)

  def __unicode__(self):
    return '%s' % self.name

  @permalink
  def get_absolute_url(self):
    return ('rss.views.view_language', None, {'code': self.code})

class Article(models.Model):
  title = models.CharField(max_length = 124, unique = True)
  slug = models.CharField(max_length = 124, unique = True)#TODO: add index based on this
  body = models.TextField()
  source_url = models.CharField(max_length = 2048) #TODO: add index based on this
  source_lang = models.ForeignKey('rss.Language')

  def scentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [i for i in chain.from_iterable([word_tokenize(t) for t in self.scentences()])]

  def __unicode__(self):
    return '%s' % self.title

  def parse(self, dest_lang):
    if dest_lang != 'en':
      raise NotImplementedError("Only English translation for now.")
    # todo:
    dest_lang = Language.objects.get(code = dest_lang) #TODO: make this resilient.
    tokens = self.words() #TODO: make this user iterators.
    stemmer = SnowballStemmer(self.source_lang.name.lower())
    length = len(tokens)
    i = 0
    old_index = None
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
        pa = ParsedArticle.objects.create(original_article = self, dest_lang = dest_lang, first_word = current_word)
      if bool(old_index): 
        current_index = WordInArticle.objects.create(word_id = current_word.id, article_id = pa.id, prev_id = old_index.id)
      else:
        current_index = WordInArticle.objects.create(word = current_word, article = pa)

      old_index = current_index
      i += 1

    pa.save()
    return pa

  @permalink
  def get_absolute_url(self):
    return ('rss.views.view_article', None, {'slug': self.slug, 'code' : self.source_lang.code})

class Word(models.Model):
  native_text = models.CharField(max_length = 124)
  native_stem = models.CharField(max_length = 124)
  native_language = models.ForeignKey('rss.Language')
  english_text = models.CharField(max_length = 124)
  #TODO: replace with wordtranslation M2M field to different languages.

class ParsedArticle(models.Model):
  """
  An article prepared to be read by someone in a foreign language.
  """
  original_article = models.ForeignKey(Article)
  first_word = models.ForeignKey(Word)
  dest_lang = models.ForeignKey(Language) #TODO: add en as default.

  def text(self):
    #TODO: make this an iterator
    #TODO: make this not terrifyingly inefficient
    words = []
    word_id = 0
    pointer = WordInArticle.objects.filter(word = self.first_word, article = self).get()
    while pointer.next.count() == 1:
      words.append((pointer.word.english_text, pointer.word.native_text, 'word_'+str(word_id)))
      pointer = pointer.next.get()
      word_id += 1
    return words

class WordInArticle(models.Model):
  # I suspect that creating a doubly-linked-list in the database is going to be terrifyingly inefficient.
  # The query over it certainly is.
  word = models.ForeignKey(Word)
  article = models.ForeignKey(ParsedArticle)
  prev = models.ForeignKey('rss.WordInArticle', related_name = 'next', blank = True, null = True)
