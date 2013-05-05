from nltk import SnowballStemmer
from nltk import sent_tokenize as base_sent_tokenize
from nltk import word_tokenize as base_word_tokenize
from itertools import chain, ifilter, imap

import apiclient.discovery
from segment import SocketSeg
CHINESE_SEGMENTER = SocketSeg()
DEFAULT_TOKEN_DIVIDER = '^'
TRANSLATE_CHUNK_SIZE = 16
NONSENSE_TOKENS = [DEFAULT_TOKEN_DIVIDER, '=','*',' ','', '==']

from settings import GOOGLE_TRANSLATE_API_KEY

service = apiclient.discovery.build('translate', 'v2', developerKey=GOOGLE_TRANSLATE_API_KEY)

def sent_tokenize(paragraph, language_code = 'en', token_divider = DEFAULT_TOKEN_DIVIDER):
  if language_code == 'zh':
    return token_divider.join(base_sent_tokenize('\n'.join(CHINESE_SEGMENTER.segment_text(line + '\n') for line in paragraph.split('\n'))))
  else:
    return token_divider.join(base_sent_tokenize(paragraph))

def word_tokenize(scentence, language_code = 'en', token_divider = DEFAULT_TOKEN_DIVIDER):
  return token_divider(base_word_tokenize(scentence))

remove_junk = lambda tokens: filter(lambda elem: elem not in NONSENSE_TOKENS, map(lambda elem: elem.strip(), tokens))

def total_word_tokenize(paragraph, language_code = 'en', token_divider = DEFAULT_TOKEN_DIVIDER):
  if language_code == 'zh':
    return list(chain.from_iterable(
             map(remove_junk, (
               base_word_tokenize(sentence) for sentence in base_sent_tokenize(
                  ''.join(CHINESE_SEGMENTER.segment_text(line + '\n') for line in paragraph.split('\n'))
                )
             ))
           ))
  else:
    #return token_divider.join(
    return list(chain.from_iterable(
             map(remove_junk, (
               base_word_tokenize(sentence) for sentence in base_sent_tokenize(paragraph)
             ))
           ))

def chunk(size, iterable):
  assert size > 0
  current = []
  for elem in iterable:
    current.append(elem)
    if len(current) == size:
      yield current
      current = []


def translate_text(native_text, native_language, target_language = 'en'):
  if not isinstance(target_language, basestring):
    target_language = target_language.code
  if not isinstance(native_language, basestring):
    native_language = native_language.code
  try:
    native_text = list(map(lambda nt: unicode(nt), native_sentence) for native_sentence in native_text)
  except UnicodeDecodeError:
    native_text = list(map(lambda nt: nt.decode('utf-8'), native_sentence) for native_sentence in native_text)
  #TODO: figure out how to send a list of requests.
  translations = []
  for sentence in chunk(TRANSLATE_CHUNK_SIZE, chain.from_iterable(native_text)):
    target_text = service.translations().list(source = native_language,
                                target = target_language,
                                q = list(sentence)).execute()
    target_text = map(lambda target_token: target_token['translatedText'], target_text['translations'])
    translations.append(target_text)
  return list(chain.from_iterable(translations))

def translate_sentence(sentence, native_language, target_language = 'en'):
  words = word_tokenize(sentence)
  translations = [translate_text(word, native_language, target_language) for word in words]
  return ' '.join(translation for translation in translations)

def translate_paragraph(paragraph, native_language, target_language = 'en'):
  print paragraph
  tokenized = total_word_tokenize(paragraph, native_language.code)
  print tokenized
  translation = translate_text(tokenized, native_language, target_language)
  print translation
  return tokenized, translation, DEFAULT_TOKEN_DIVIDER
