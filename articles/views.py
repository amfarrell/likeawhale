# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from articles.models import Language
from articles.models import Article
from articles.models import PhraseInTranslation
from articles.models import Translation

ARTICLES_PER_PAGE = 5

def index(request):
  return render_to_response('index.html', {
    'languages': Language.objects.all(),
    'articles': Article.objects.all()[:ARTICLES_PER_PAGE]
    })

@login_required
def view_article(request, code, slug):
  article = get_object_or_404(Article, slug = slug)
  translation = article.translated_to(code)

  def stem_of(word):
    if word.stem:
      return word.native_stem
    else:
      return word
  pointers = PhraseInTranslation.objects.filter(part_of = translation).select_related(
      'phrase','phrase__first_target','phrase__first_native','phrase__first_target__native_text', 'phrase__first_native__native_text', 'phrase__first_native__native_stem').all()
  return render_to_response('article.html', {
    'article': article,
    'translation': translation,
    'phrases' : [(
        pointer._order,                                   #node_id
        pointer.phrase.first_native.pk,                   #word_id
        pointer.phrase.first_native.stem_id(),          #stem_id
        pointer.phrase.first_native.native_text,          #native_text
        pointer.phrase.first_target.native_text,          #target_text
      ) for pointer in pointers]
    })

def view_language(request, code):
  language = get_object_or_404(Language, code = code)
  return render_to_response('language.html', {
    'language': language,
    'articles': Translation.objects.filter(target_language = language)[:ARTICLES_PER_PAGE]
    })
