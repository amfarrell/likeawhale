# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from articles.models import Language
from articles.models import Article
from articles.models import PhraseInTranslation
from articles.models import Translation

from scraping import scrape_wikipedia

from settings import DEBUG

ARTICLES_PER_PAGE = 5
DEFAULT_LANGUAGE = 'en'

@login_required
def index(request):
  return render(request, 'index.html', {
    'languages': Language.objects.all(),
    'articles': Article.objects.all()[:ARTICLES_PER_PAGE]
    })

@login_required
def view_language(request, code):
  language = get_object_or_404(Language, code = code)
  return render(request, 'language.html', {
    'language': language,
    'articles': Translation.objects.filter(original_article__native_language = language)[:ARTICLES_PER_PAGE]
    })


@ensure_csrf_cookie
@login_required
def view_article(request, code):
  if 'url' not in request.GET:
    return redirect(reverse(view_language, kwargs = {'code' : code}))
  article = get_object_or_404(Article, native_language__code = code, source_url = request.GET['url'])
  translation = article.translated_to(request.GET.get('target_lang', DEFAULT_LANGUAGE), force = False)
  pointers = PhraseInTranslation.objects.filter(part_of = translation).select_related(
      'phrase','phrase__first_target','phrase__first_native','phrase__first_target__native_text', 'phrase__first_native__native_text', 'phrase__first_native__native_stem').all()
  return render(request, 'article.html', {
    'article': article,
    'translation': translation,
    'phrases' : [(
        pointer._order,                                   #node_id
        pointer.phrase.first_native.pk,                   #word_id
        pointer.phrase.first_native.stem_id(),            #stem_id
        pointer.phrase.first_native.native_text,          #native_text
        pointer.phrase.first_target.native_text,          #target_text
      ) for pointer in pointers]
    })

@login_required
def view_wikipedia_article(request, code):
  try:
    topic_u = unicode(request.GET['topic'])
  except UnicodeEncodeError:
    topic_u = request.GET['topic'].decode('utf-8')
  article = scrape_wikipedia(code, topic_u)
  article.save()
  translation = article.translated_to('en') #TODO: generalize this to the users' language.
  translation.save()
  return redirect(translation.get_absolute_url())
