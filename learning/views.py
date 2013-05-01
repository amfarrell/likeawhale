# Create your views here.

from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import allauth
from articles.models import Word, Language, TranslatedPhrase
from learning.models import UserWordKnowledge, UserLanguageKnowledge
from Modeling_API import *


@login_required
def pretest(request):
  return render(request, 'pretest.html', {
    #'': Language.objects.all(),
    #'': Article.objects.all()
    })


@login_required
def has_translated(request):
  """
  params:
  'target_lang' : The ISO code for the language that the qord was translated into.
  'word_id' : The database primary key of the word.

  Called whenever a user requests the translation of a word.
  """
  callOnClick(request.user.id, word_id)

  #language = Language.objects.get(code = request.POST['target_lang'])
  #phrase = TranslatedPhrase.objects.get(first_native__pk = request.POST['word_id'], first_target__native_language = language)
  #print phrase
  #print UserWordKnowledge.objects.get_or_create(user = request.user, word = phrase.first_native)
  #print UserLanguageKnowledge.objects.get_or_create(user = request.user, language = language)
  #return HttpResponse(simplejson.dumps('okay'), mimetype='application/json')

@login_required
def has_seen(request):
  """
  Params:
    'article_id': pk of the article

  Assumption: Called when an article is uploaded
  """
  callOnArticleUpload(request.user.id, article_id)

  #return HttpResponse(simplejson.dumps('okay'), mimetype='application/json')



def populateModel(user_id, level):
"""
Initialize the model of the user. 
All word levels labled 1-6, 1 being the first 1 thousand, etc.
Mastery_level is just a boolean value.

Keyword arguments:
  user_id - the user id of type int
  level - the user level from 1 to 6.
"""
  words = Word.objects.get(difficulty__lte = level)
  for word in words:
    vector = UserWordKnowledge(user_id = user_id,
      word = word, mastery_level = 1)
    vector.save()
