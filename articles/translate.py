from nltk import SnowballStemmer
from nltk import sent_tokenize as base_sent_tokenize
from nltk import word_tokenize as base_word_tokenize
from itertools import chain, ifilter

import apiclient.discovery
from segment import SocketSeg
CHINESE_SEGMENTER = SocketSeg()
DEFAULT_TOKEN_DIVIDER = '^'
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

def total_word_tokenize(paragraph, language_code = 'en', token_divider = DEFAULT_TOKEN_DIVIDER):
  if language_code == 'zh':
#    segmented = [CHINESE_SEGMENTER.segment_text(line + '\n') for line in paragraph.split('\n')]
#    segmented = ''.join(segmented)
#    segmented = base_sent_tokenize(segmented)
#    segmented = [base_word_tokenize(s) for s in segmented]
#    segmented = [i for i in chain.from_iterable(segmented)]
#    segmented = token_divider.join(segmented)
#    return segmented
    return token_divider.join(
        ifilter(lambda token: token not in NONSENSE_TOKENS,
          chain.from_iterable(
            base_word_tokenize(sentence) for sentence in base_sent_tokenize(
              ''.join(CHINESE_SEGMENTER.segment_text(line + '\n') for line in paragraph.split('\n'))
            )
          )
        )
      )
  else:
    return token_divider.join(
        chain(
          base_word_tokenize(sentence) for sentence in base_sent_tokenize(paragraph)
        )
      )


def translate_text(native_text, native_language, target_language = 'en'):
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
  return target_text

def translate_sentence(sentence, native_language, target_language = 'en'):
  words = word_tokenize(sentence)
  translations = [translate_text(word, native_language, target_language) for word in words]
  return ' '.join(translation for translation in translations)

def translate_paragraph(paragraph, native_language, target_language = 'en'):
  tokenized = total_word_tokenize(paragraph, native_language.code)
  translation = translate_text(tokenized, native_language, target_language)
  return tokenized.split(DEFAULT_TOKEN_DIVIDER), translation.split(DEFAULT_TOKEN_DIVIDER), DEFAULT_TOKEN_DIVIDER
