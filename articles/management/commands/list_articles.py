from django.core.management.base import BaseCommand
from articles.models import Language

def articles_of(language):
  return '\n'.join(["-- %s" % article.source_url for article in language.article_set.all()])

class Command(BaseCommand):
    args = 'topic language_code '

    help = 'Download a wikipedia article on a particular topic.'

    def handle(self, *args, **options):
      if len(args) == 1:
        return articles_of(Language.objects.get(code=args[0]))
      else:
        return '\n'.join(['[%s] %s articles\n' % (language.name, language.article_set.count()) + articles_of(language) for language in Language.objects.all()])
        raise NotImplementedError()
