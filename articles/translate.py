from nltk import SnowballStemmer
from nltk import sent_tokenize as base_sent_tokenize
from nltk import word_tokenize as base_word_tokenize

import apiclient.discovery
from segment import SocketSeg
CHINESE_SEGMENTER = SocketSeg()

from settings import GOOGLE_TRANSLATE_API_KEY

service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)


def sent_tokenize(paragraph, language_code = 'en'):
  if language_code == 'zh':
    retur= base_sent_tokenize('\n'.join(CHINESE_SEGMENTER.segment_text(line) for line in paragraph.split('\n')[0]))
  else:
    retur= base_sent_tokenize(paragraph)
  return retur

def word_tokenize(scentence, language_code = 'en'):
  return base_word_tokenize(scentence)

def translate_word(native_text, native_language, target_language = 'en'):
  if not isinstance(target_language, basestring):
    target_language = target_language.code
  if not isinstance(native_language, basestring):
    native_language = native_language.code
  try:
    native_text = unicode(native_text)
  except UnicodeDecodeError:
    native_text = native_text.decode('utf-8')
  target_text = service.translations().list(source = native_language,
                              target = target_language,
                              q = [native_text,]).execute()
  target_text = target_text['translations'][0]['translatedText']
  return target_text.decode('utf-8')

def translate_sentence(sentence, native_language, target_language = 'en'):
  words = word_tokenize(sentence)
  translations = [translate_word(word, native_language, target_language) for word in words]
  return ' '.join(translation for translation in translations)

def translate_paragraph(paragraph, native_language, target_language = 'en'):
  sentences = sent_tokenize(paragraph, native_language.code)
  translations = [translate_sentence(sentence, native_language, target_language) for sentence in sentences]
  return ' '.join(translation for translation in translations)
