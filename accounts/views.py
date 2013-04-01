# Create your views here.
from django.contrib.auth.models import authenticate
from django.contrib.auth.models import login

def log_in(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username = username, password = password)
  if user is not None:
    if user.is_active:
      login(request, user)
    else:
      raise NotImplementedError
  else:
    raise NotImplementedError
    #Redirect to create account page.

def has_seen(request):
  for word_id in request.POST['words']:
    UserWordKnowledge.objects.get
  pass

def has_translated(request):
  pass
