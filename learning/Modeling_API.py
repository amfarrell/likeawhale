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

###-------------------------------------###


from articles.models import Word, Language, Article
from learning.models import UserWordKnowledge
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

def populateModel(user_id, level):
  """
  Initialize the model of the user. 
  All word levels labled 1-6, 1 being the first 1 thousand, etc.
  Mastery_level is just a boolean value.

  Keyword arguments:
    user_id - the user id of type int
    level - the user level from 1 to 6.
  """
  words = Word.objects.get(difficulty__lte = level)
  for word in words:
    vector = UserWordKnowledge(user_id = user_id,
      word = word, mastery_level = 1)
    vector.save()


# Sets word to unknown.
def callOnClick(user_id, word_id):
  """
  Function needs to be called on a user word definition
  lookup click. This updates the model.

  Keyword arguments:
    user_id - the primary key (pk) of username of type int
    word_id - the pk of word of type int
  """
  word = Word.objects.get(pk=word_id)
  vector = UserWordKnowledge.objects.get(user_id=user_id, word=word)
  vector.mastery_level = 0
  vector.view_count = 0
  vector.save()


# Assumes an Article words() method.
def callOnArticleUpload(user_id, article_id):
  """
  Function needs to be called on an article click.
  When an article is displayed, increase the read 
  count of every word.

  Keyword arguments:
    user_id - the user id of type int
    article_id - the pk of the article of type int
  """
  article = Article.objects.get(pk=article_id)
  text = article.words()

  for word in text:
    vector = UserWordKnowledge.objects.filter(user_id=user_id, word=word)
    vector.view_count += 1
    vector.save()
    if vector.view_count >= 3:
      vector.mastery_level = 1
      vector.view_count = 0
      vector.save()



def scoreArticle(user_id, article_id):
  """
  Returns ratio of words known to total words.
  Assumption: Includes duplicate words.

  Keyword arguments:
    user_id - the user id of type int
    article_id - the pk of the article of type int
  """
  article = Article.objects.get(article_id = article_id)
  score = 0.0
  words = list(set(article.words()))
  for word in words:
    if UserWordKnowledge.objects.get(user_id, word=word) != None:
      score += 1
  return score/len(article.words())


def rankArticles(user_id, article_ids):
  """
  Takes in a list of article ids and returns the ranked order.

  Keyword arguments:
    user_id - the username of type string
    article_ids - a list of int article id's
  """
  ranking = []
  for article_id in article_ids:
    score = scoreArticle(user_id, article_id)
    ranking.append((score, article_id))
  ranking.reverse()
  ranking = [title for score, title in ranking]
  return ranking