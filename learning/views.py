# Create your views here.

from django.utils import simplejson
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import allauth
from articles.models import Word, Language, TranslatedPhrase
from learning.models import UserWordKnowledge, UserLanguageKnowledge

#def log_in(request):
#  username = request.POST['username']
#  password = request.POST['password']
#  if user is not None:
#    if user.is_active:
#      login(request, user)
#    else:
#      raise NotImplementedError
#  else:
#    raise NotImplementedError
#    #Redirect to create account page.
#
#def has_seen(request):
#  for word_id in request.POST['words']:
#    UserWordKnowledge.objects.get
#  pass

@login_required
def has_translated(request):
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
