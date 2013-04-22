# Additional models to be added to model.py
 class UserWordKnowledge(models.Model):
  user_id = models.ForeignKey(User) # need to add User model
  word_id = models.ForeignKey(Word)
  word = models.CharField(max_length=255)
  mastery_level = models.IntegerField() # 0-100. 50 is default
  last_view = models.DateField(auto_now_add = True)
  view_count = models.IntegerField()
  last_lookup = models.DateField(auto_now_add = True)
  lookup_count = models.IntegerField()
# Need to upload the grade level list to Word table


###-------------------------------------###


"""
class methods for Model
We can measure the fluency level of a user
by the number of words they know.

User choses level. Beginning, intermidate, advanced. 0-2, 3-4, or 5-6
Create function that randomly displays 10 words from each level

Click on word once, then set to unknown
If after 3 reads, if no clicks, then set word to known.
Anytime a word click happens, it resets to zero.
"""

def initializeModel(self, user, lvl):
"""
Initialize the model of the user. 
All word levels labled 1-6, 1 being the first 1 thousand, etc.
Mastery_level is just a boolean value.

Keyword arguments:
  user - the username of type string
  lvl - the user level from 1 to 6.
"""
  words = Word.objects.filter(level <= lvl) # do conditionals work?
  for w in words:
    difficulty = w.difficulty
    v = UserWordKnowledge(word=w, word_id=w.id, user_id=user, mastery_level=1)
    v.save()


# Sets word to unknown.
def callOnClick(self, user, word):
  """
  Function needs to be called on a user word definition
  lookup click. This updates the model.

  Keyword arguments:
    user - the username of type string
    word - the word of type string
  """
  vector = UserWordKnowledge.objects.filter(user=user, word=word)
  vector.mastery_level = 0
  vector.view_count = 0
  vector.save()


# Assumes an Article words() method.
def callOnArticleUpload(self, user, title):
  """
  Function needs to be called on an article click.
  When an article is displayed, increase the read 
  count of every word.

  Keyword arguments:
    user - the username of type string
    title - the title of the article of type string
  """
  article = Article.objects.filter(title=title)
  text = article.words()

  for word in text:
    vector = UserWordKnowledge.objects.filter(user=user, word=word)
    vector.view_count += 1
    vector.save()
    if vector.view_count >= 3:
      vector.mastery_level = 1
      vector.view_count = 0
      vector.save()



def scoreArticle(self, user, title):
  """
  Returns ratio of words known to total words.
  Includes duplicate words.

  Keyword arguments:
    user - the username of type string
    title - the title of the article of type string
  """
  article = Article.objects.get(title = title)
  score = 0.0
  for w in article.words():
    if UserWordKnowledge.objects.get(word=w) not None:
      score += 1
  return score/len(article.words())


def rankArticles(self, user, titles):
  """
  Takes in a list of article names and returns the ranked order.

  Keyword arguments:
    user - the username of type string
    titles - a list of string titles
  """
  ranking = []
  for title in titles:
    score = self.scoreArticle(user, title)
    ranking.append((score, title))
  ranking.reverse()
  ranking = [title for score, title in ranking]
  return ranking




""" 
Later, more advanced modeling methods, possibly with 
relevance, backoff, etc.
"""
# def callOnLookup(word, user_vectors):
#   pass

# def callOnView(word, user_vectors):
#   pass

# def mastery_update(word,command):
#   pass