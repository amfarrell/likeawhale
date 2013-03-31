from django.core.management.base import BaseCommand
from articles.models import Language

class Command(BaseCommand):
    args = 'code name'
    help = 'Add a record of a language.'

    def handle(self, *args, **options):
      return "%s\n" % Language.objects.get_or_create(code = args[0], name = args[1])[0]
