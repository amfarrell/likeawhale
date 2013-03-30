# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from articles.models import Language, Article

ARTICLES_PER_PAGE = 5

def index(request):
  return render_to_response('index.html', {
    'languages': Language.objects.all(),
    'articles': Article.objects.all()[:ARTICLES_PER_PAGE]
    })

def view_article(request, code, slug):
  article = get_object_or_404(Article, slug = slug)
  parsed_article = article.parsed_article()
  return render_to_response('article.html', {
    'article': article,
    'parsed_article': parsed_article
    })

def view_language(request, code):
  language = get_object_or_404(Language, code = code)
  return render_to_response('language.html', {
    'language': language,
    'articles': Article.objects.filter(source_lang = language)[:ARTICLES_PER_PAGE]
    })
