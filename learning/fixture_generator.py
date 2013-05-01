#!/usr/bin/python
from django.core import serializers

f = open('Char_level_list.txt','r')
new = open('fixture.json','w')

level = 1
pk = 1

new.write('[')

lang_serialize = serializers.serialize('json',Language.objects.get(name='chinese'))

for line in f:
	if len(line) > 2:
		wordList = line.split()
		for i in range(len(wordList)):
			listLen = len(wordList)-1
			word = wordList[i]
			entry = """
			{
			    "model": "articles.models.Word",
			    "pk": %s,
			    "fields": {
			      "native_text":%s,
			      "native_stem":,
			      "native_language":%s,
			      "difficulty":%s
				}
  			}""" % (pk, word, lang_serialize, level)
  			pk += 1
  			if level != 6 or i != listLen:
  				new.write(entry + ',\n')
  			else:
  				new.write(entry)

  	# Update level after new line
  	if len(line) > 5:	
  		level += 1

new.write(']')
new.close()