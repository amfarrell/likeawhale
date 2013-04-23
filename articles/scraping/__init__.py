from wiki2plain import Wiki2Plain
from wikipedia import Wikipedia
from articles.models import Article, Language

def scrape_wikipedia(language, topic, force = False):
  if isinstance(language, basestring):
    language = Language.objects.get(code = language)
  url = (Wikipedia.url_article % (language.code, topic))
  if Article.objects.filter(source_url = url).count() == 1:
    return Article.objects.get(source_url = url)
  else:
    body = unicode(Wiki2Plain(Wikipedia(language.code).article(topic.encode('utf-8'))))
    article = Article.objects.create(
      native_language = language,
      source_url = url,
      body = body,
      title = topic
    )
    return article
