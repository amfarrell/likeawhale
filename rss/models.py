from django.db import models
from django.db.models import permalink

class Language(models.Model):
  code = models.CharField(max_length = 8, unique = True)
  name = models.CharField(max_length = 32, unique = True)

  def __unicode__(self):
    return '%s' % self.name

  @permalink
  def get_absolute_url(self):
    import pdb;pdb.set_trace()
    return ('rss.views.view_language', None, {'code': self.code})

class Article(models.Model):
  title = models.CharField(max_length = 124, unique = True)
  slug = models.CharField(max_length = 124, unique = True)
  body = models.TextField()
  source_url = models.CharField(max_length = 2048)
  source_lang = models.ForeignKey('rss.Language')

  def __unicode__(self):
    return '%s' % self.title

  @permalink
  def get_absolute_url(self):
    return ('rss.views.view_article', None, {'slug': self.slug, 'code' : self.source_lang.code})


