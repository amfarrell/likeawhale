# -*- coding: utf-8 -*-
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

ARTICLES_PER_PAGE = 20
DEFAULT_LANGUAGE = 'en'

#@login_required
def index(request):
  return render(request, 'index.html', {
    'languages': Language.objects.all(),
    'articles': Article.objects.all()[:ARTICLES_PER_PAGE]
    })

#@login_required
def view_language(request, code):
  language = get_object_or_404(Language, code = code)
  return render(request, 'language.html', {
    'language': language,
    'articles': Translation.objects.filter(original_article__native_language = language)[:ARTICLES_PER_PAGE]
    })


#@login_required
@ensure_csrf_cookie
def view_article(request, code):
  if 'url' not in request.GET:
    return redirect(reverse(view_language, kwargs = {'code' : code}))
  article = get_object_or_404(Article, native_language__code = code, source_url = request.GET['url'])
  translation = article.translated_to(request.GET.get('target_lang', DEFAULT_LANGUAGE), force = False)
  pointers = PhraseInTranslation.objects.filter(part_of = translation).select_related(
      'phrase','phrase__first_target','phrase__first_native','phrase__first_target__native_text', 'phrase__first_native__native_text', 'phrase__first_native__native_stem').all()
  def wiki_link(pointer):
    if pointer.phrase.first_native.has_wikipedia_link is True:
      return pointer.phrase.first_native.wikipedia_link.native_text 
    else :
      return ''
  return render(request, 'article.html', {
    'article': article,
    'translation': translation,
    'native_code' : translation.original_article.native_language.code,
    'phrases' : [(
        pointer._order,                                   #node_id
        pointer.phrase.first_native.pk,                   #word_id
        pointer.phrase.first_native.stem_id(),            #stem_id
        pointer.start_punctuation + pointer.phrase.first_native.native_text + pointer.end_punctuation,          #native_text
        pointer.start_punctuation + pointer.phrase.first_target.native_text + pointer.end_punctuation,          #target_text
        wiki_link(pointer),
      ) for pointer in pointers]
    })

#@login_required
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
