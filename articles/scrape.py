

def scrape(url):
  #TODO: take a url and download the text of the article and create an Article object then find the layoutElements within it and translate them.
  pass

  def scentences(self):
    return sent_tokenize(self.body)

  def words(self):
    #TODO inefficient.
    return [i for i in chain.from_iterable([word_tokenize(t) for t in self.scentences()])]

  def __unicode__(self):
    return '%s' % self.title

  def parsed_article(self, dest_lang = 'en'):
    raise NotImplementedError
    if dest_lang != 'en':
      raise NotImplementedError("Only English translation for now.")
    dest_lang = Language.objects.get(code = dest_lang) #TODO: make this resilient.
    pa = Translation.objects.filter(original_article = self, dest_lang = dest_lang)
    if pa.count():
      return pa.get()
    else:
      return self.parse(dest_lang)


  def parse(self, dest_lang = 'en'):
    raise NotImplementedError
    if dest_lang != 'en':
      raise NotImplementedError("Only English translation for now.")
    # todo:
    dest_lang = Language.objects.get(code = dest_lang) #TODO: make this resilient.
    tokens = self.words() #TODO: make this user iterators.
    stemmer = SnowballStemmer(self.source_lang.name.lower())
    length = len(tokens)
    i = 0
    #old_index = None
    pa = None

    while i < length:
      current_text = tokens[i]
      current_stem = stemmer.stem(current_text)
      current_word = Word.objects.filter(native_text = current_text, native_language = self.source_lang)
      if current_word.count() == 0:
        current_word = Word.objects.create(native_text = current_text, native_language = self.source_lang, native_stem = current_stem, english_text = current_stem)
      else:
        current_word = current_word.get()

      if i == 0:
        pa = Translation.objects.create(original_article = self, dest_lang = dest_lang, first_word = current_word)
      #if bool(old_index): 
      #  current_index = WordInArticle.objects.create(word_id = current_word.id, article_id = pa.id, prev_id = old_index.id)
      #else:
      #  current_index = WordInArticle.objects.create(word = current_word, article = pa)

      #old_index = current_index
      i += 1

    pa.save()
    return pa
