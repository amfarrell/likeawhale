# Create your views here.

from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import allauth
from articles.models import Word, Language, TranslatedPhrase
from learning.models import UserWordKnowledge, UserLanguageKnowledge

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
  language = Language.objects.get(code = request.POST['target_lang'])
  phrase = TranslatedPhrase.objects.get(first_native__pk = request.POST['word_id'], first_target__native_language = language)
  print phrase
  print UserWordKnowledge.objects.get_or_create(user = request.user, word = phrase.first_native)
  print UserLanguageKnowledge.objects.get_or_create(user = request.user, language = language)
  return HttpResponse(simplejson.dumps('okay'), mimetype='application/json')

@login_required
def has_seen(request):
  return HttpResponse(simplejson.dumps('okay'), mimetype='application/json')
  pass



def populateModel(user, level):
  """
  Takes in a user and level and populates words based on level
  """
  words = Word.objects.get(difficulty <= level)
  for word in words:
    vector = UserWordKnowledge(user = user, word = word.native_text, mastery_level = 1)
    vector.save()
