from django.db import models
from django.contrib.auth.models import User
from articles.models import Word
from articles.models import Language

# Create your models here.

class UserLanguageKnowledge(models.Model):
  user = models.ForeignKey(User)
  language = models.ForeignKey(Language)
  mastery_level = models.IntegerField(default = 0)
  view_count = models.IntegerField(default = 0)
  last_lookup = models.DateField(auto_now_add = True)
  lookup_count = models.IntegerField(default = 0)

  class Meta:
    unique_together = ('user', 'language')

class UserWordKnowledge(models.Model):
  user_id = models.ForeignKey(User) # need to add User model
  word_id = models.ForeignKey(Word)
  word = models.CharField(max_length=255)
  mastery_level = models.IntegerField() # 0-100. 50 is default
  last_view = models.DateField(auto_now_add = True)
  view_count = models.IntegerField()
  last_lookup = models.DateField(auto_now_add = True)
  lookup_count = models.IntegerField()

  class Meta:
    unique_together = ('user', 'word')
