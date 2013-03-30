from settings import GOOGLE_TRANSLATE_API_KEY
import apiclient.discovery
from models import Word
from models import Language
from models import TranslatedPhrase

service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)


def translateword(self, word, target_language):
  text = service.translations().list(source = word.native_language.code, 
                              target = target_language.code,
                              q = [word.text,]).execute()
  Word.objects.find_or_create(native_text = text, native_language = target_language)
