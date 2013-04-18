from nltk import SnowballStemmer
from nltk import sent_tokenize
from nltk import word_tokenize

import apiclient.discovery

from settings import GOOGLE_TRANSLATE_API_KEY

service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)

def translate_word(native_text, native_language, target_language = 'en'):
  if not isinstance(target_language, basestring):
    target_language = target_language.code
  if not isinstance(native_language, basestring):
    native_language = native_language.code
  target_text = service.translations().list(source = native_language,
                              target = target_language,
                              q = [native_text,]).execute()
  target_text = target_text['translations'][0]['translatedText']
  return target_text

def translate_sentence(sentence, native_language, target_language = 'en'):
  words = word_tokenize(sentence)
  translations = [translate_word(word, native_language, target_language) for word in words]
  return ' '.join(translation for translation in translations)

def translate_paragraph(paragraph, native_language, target_language = 'en'):
  sentences = sent_tokenize(paragraph)
  translations = [translate_sentence(sentence, native_language, target_language) for sentence in sentences]
  return ' '.join(translation for translation in translations)

