# Create your views here.

try:
  import allauth
except ImportError:
  raise "You must install django-allauth0.10.0, which is not yet on pyPI. so `cd django-allauth; python setup.py install`"


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

def has_translated(request):
  pass
