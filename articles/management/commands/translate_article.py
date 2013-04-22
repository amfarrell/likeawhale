from django.core.management.base import BaseCommand
from articles.models import Article
from articles.models import Language

class Command(BaseCommand):
    args = 'article_url language_code '

    help = 'Add a record of a language.'

    def handle(self, *args, **options):
      if len(args[0]) < len(args[1]):
        print "\nusage ./manage.py translate_article %s\n" % Command.args
      article = Article.objects.get(source_url = args[0])
      language = Language.objects.get(code = args[1])
      translation = article.translated_to(language, force = True)
      return "%s translated to %s\n Viewable at %s\n" % (article.title, language.name, translation.get_absolute_url())
