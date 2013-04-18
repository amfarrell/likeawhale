from django.core.management.base import BaseCommand
from articles.scraping import scrape_wikipedia

class Command(BaseCommand):
    args = 'topic language_code '

    help = 'Download a wikipedia article on a particular topic.'

    def handle(self, *args, **options):
      if len(args) != 2 or len(args[0]) > len(args[1]):
        raise Exception("\nusage ./manage.py scrape_wikipedia %s\n" % Command.args)
      return scrape_wikipedia(args[0], args[1]) + '\n'
