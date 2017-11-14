from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

regex = re.compile('Trump')
f = open('../Datasets/nytimes_dataset','r')
articleList = open('../Datasets/nytimes_dataset').readlines()
lines_list = []

for article in articleList:
   if re.search(regex,article):    
      lines_list.extend(tokenize.sent_tokenize(article))

sid = SentimentIntensityAnalyzer()

for sentence in lines_list:
   ss = sid.polarity_scores(sentence)
   if ss['neg'] > 0.5 or ss['pos'] > 0.5:
      print(sentence)
      for k in sorted(ss):
         print('{0}: {1}, '.format(k, ss[k]),end='')
      print()
