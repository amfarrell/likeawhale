from nltk import SnowballStemmer
from nltk import sent_tokenize
from nltk import word_tokenize

import apiclient.discovery

from settings import GOOGLE_TRANSLATE_API_KEY

from models import Word
from models import Stem
from models import Language
from models import TranslatedPhrase


service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)

def translateword(word, native_language = None, target_language = 'en'):
  if type(target_language) is str:
    target_language = Language.objects.get(code = target_language)
  if type(word) is str and native_language is not None:
    if type(native_language) is str:
      native_language = Language.objects.get(code = native_language)
    native_stemmer = SnowballStemmer(native_language.name.lower())
    stem = Stem.objects.create(native_text = native_stemmer.stem(word), native_language = native_language)
    word = Word.objects.get_or_create(native_stem = stem, native_text = word, native_language = native_language)[0]
  target_text = service.translations().list(source = word.native_language.code,
                              target = target_language.code,
                              q = [word.native_text,]).execute()
  target_stemmer = SnowballStemmer(target_language.name.lower())
  target_text = target_text['translations'][0]['translatedText']
  target_stem = target_stem = Stem.objects.create(native_language = target_language, native_text = target_stemmer.stem(target_text))
  result = Word.objects.get_or_create(native_text = target_text, native_stem = target_stem, native_language = target_language)[0]
  translation = TranslatedPhrase.objects.create(first_target = result, first_native = word)
  return translation

def translatesentence(sentence, native_language, target_language):
  words = word_tokenize(sentence)
  translations = [translateword(word, native_language, target_language) for word in words]
  return ' '.join(translation.resulting_text() for translation in translations)

def translateparagraph(paragraph, native_language, target_language):
  sentences = sent_tokenize(paragraph)
  translations = [translatesentence(sentence, native_language, target_language) for sentence in sentences]
  return ' '.join(translation for translation in translations)

