# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from articles.models import Language
from articles.models import Article
from articles.models import PhraseInTranslation
from articles.models import Translation

from settings import DEBUG

ARTICLES_PER_PAGE = 5

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
    'articles': Translation.objects.filter(target_language = language)[:ARTICLES_PER_PAGE]
    })


@ensure_csrf_cookie
@login_required
def view_article(request, code, slug = None):
  if slug:
    article = get_object_or_404(Article, slug = slug)
  else:
    if 'url' not in request.GET:
      return redirect('view_language', code = code)
    article = get_object_or_404(Article, source_url = request.GET['url'])
  translation = article.translated_to(code, force = False)

  def stem_of(word):
    if word.stem:
      return word.native_stem
    else:
      return word
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
