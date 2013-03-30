from settings import GOOGLE_TRANSLATE_API_KEY
import apiclient.discovery
from models import Word
from models import Stem
from models import Language
from models import TranslatedPhrase
from nltk import SnowballStemmer

service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)

def translateword(word, target_language, native_language = None):
  if type(target_language) is str:
    target_language = Language.objects.get(code = target_language)
  if type(word) is str and native_language is not None:
    if type(native_language) is str:
      native_language = Language.objects.get(code = native_language)
    native_stemmer = SnowballStemmer(native_language.name.lower())
    stem = Stem.objects.create(native_text = native_stemmer.stem(word), native_language = native_language)
    word = Word.objects.get_or_create(native_stem = stem, native_text = word, native_language = native_language)[0]
  text = service.translations().list(source = word.native_language.code,
                              target = target_language.code,
                              q = [word.native_text,]).execute()
  target_stemmer = SnowballStemmer(target_language.name.lower())
  text = text['translations'][0]['translatedText']
  target_stem = target_stem = Stem.objects.create(native_language = target_language, native_text = target_stemmer.stem(text))
  result = Word.objects.get_or_create(native_text = text, native_stem = target_stem, native_language = target_language)[0]
  translation = TranslatedPhrase.objects.create(represents_first = result, using_first = word)
  return translation
