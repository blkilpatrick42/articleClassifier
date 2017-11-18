from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

f = None
articleList = None

dataset = input("Use data from | (1) CNN | (2) BBC | (3) Fox News | (4) NYT | (5) Al Jazeera) | -> ")
if int(dataset) == 1:
   f = open('../Datasets/clean_cnn_dataset','r')
   articleList = open('../Datasets/clean_cnn_dataset').readlines()
elif int(dataset) == 2:
   f = open('../Datasets/clean_bbc_dataset','r')
   articleList = open('../Datasets/clean_bbc_dataset').readlines()
elif int(dataset) == 3:
   f = open('../Datasets/clean_fox_dataset','r')
   articleList = open('../Datasets/clean_fox_dataset').readlines()
elif int(dataset) == 4:
   f = open('../Datasets/clean_bbc_dataset','r')
   articleList = open('../Datasets/clean_bbc_dataset').readlines()
elif int(dataset) == 5:
   f = open('../Datasets/clean_alj_dataset','r')
   articleList = open('../Datasets/clean_alj_dataset').readlines()

term = input("Query For Term: ")
regex = re.compile(r"([^.]*? "+term+" [^.]*\.)")
quotes = re.compile(r"(.*?)")
sentence_list = []
quotes_list = []

#find all sentences mentioning the keyword in the dataset
for article in articleList:
    sentence_list.extend(re.findall(regex,article))

#extract quotations so that they are considered seperately
#this way, the bias of certain quotes provided by the source
#are considered outside of their neutral phrasing
#for sentence in sentence_list:
#    quotes_list.extend(re.findall('"([^"]*)"',sentence))

#print(quotes_list)

token_list = []

for sentence in sentence_list:
    token_list.extend(tokenize.sent_tokenize(sentence))

sentence_list = sentence_list + quotes_list

sid = SentimentIntensityAnalyzer()
avgNeg = 0
avgPos = 0
avgNeu = 0
numTokens = 0

for token in token_list:
   ss = sid.polarity_scores(token)
   print(token)
   avgNeg = avgNeg + ss['neg']
   avgPos = avgPos + ss['pos']
   avgNeu = avgNeu + ss['neu']
   numTokens = numTokens + 1
   for k in sorted(ss):
      print('{0}: {1}, '.format(k, ss[k]),end='')
   print()

avgNeg = avgNeg / numTokens
avgPos = avgPos / numTokens
avgNeu = avgNeu / numTokens

print("Average pos: ")
print(avgPos)
print("Average neg: ")
print(avgNeg)
print("Average neu: ")
print(avgNeu)
