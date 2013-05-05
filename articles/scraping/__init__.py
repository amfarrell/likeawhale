from wiki2plain import Wiki2Plain
from wikipedia import Wikipedia
from articles.models import Article, Language, Word

def scrape_wikipedia(language, topic_u, force = False):
  if isinstance(language, basestring):
    language = Language.objects.get(code = language)
  url = (Wikipedia.url_article % (language.code, topic_u))
  if Article.objects.filter(source_url = url).count() == 1:
    return Article.objects.get(source_url = url)
  else:
    print language.code
    site = Wikipedia(language.code)
    wiki = Wiki2Plain(site.article(topic_u.encode('utf-8')))
    body_u = unicode(wiki)
    for link in wiki.links:
      word = Word.objects.filter(native_text = link, native_language = language)
      if word.exists() and word.get().has_wikipedia_link is None:
        word = word.get()
        topic_8 = site.exists(link)
        if topic_8 != link:
          other = Word.objects.filter(native_text = topic_8, native_language = language)
          if other.exists():
            word.wikipedia_link = other.all()[0]
            word.has_wikipedia_link = True
          else:
            word.has_wikipedia_link = False
        else:
          word.wikipedia_link = word
          word.has_wikipedia_link = True
        word.save()
    article = Article.objects.create(
      native_language = language,
      source_url = url,
      body = body_u,
      title = topic_u
    )
    return article
