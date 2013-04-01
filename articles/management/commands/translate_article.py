from django.core.management.base import BaseCommand
from articles.models import Article
from articles.models import Language

class Command(BaseCommand):
    args = '(articles_slug | article_url) language_code '

    help = 'Add a record of a language.'

    def handle(self, *args, **options):
      if len(args[0]) < len(args[1]):
        print "\nusage ./manage.py translate_article %s\n" % Command.args
      if 'http://' in args[0]:
        kwargs = {'source_url' : args[0]}
      else:
        kwargs = {'slug' : args[0]}
      article = Article.objects.get(**kwargs)
      language = Language.objects.get(code = args[1])
      translation = article.translated_to(language, force = True)
      return "%s translated to %s\n Viewable at %s\n" % (article.slug, language.name, translation.get_absolute_url())
