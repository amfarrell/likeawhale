from wiki2plain import Wiki2Plain
from wikipedia import Wikipedia
from articles.models import Article, Language

def scrape_wikipedia(language, topic):
  if isinstance(language, basestring):
    language = Language.objects.get(code = language)

  body = Wiki2Plain(Wikipedia(language.code).article(topic))
  article = Article.objects.create(
    native_language = language,
    source_url = Wikipedia.url_article % (language.code, topic), #DRY
    body = body,
    title = topic
  )
  return article
