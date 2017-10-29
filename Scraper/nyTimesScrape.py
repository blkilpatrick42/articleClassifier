from bs4 import BeautifulSoup

import requests

import re

regex = re.compile('https://www.nytimes.com/2017/*')

articleList = []

url = 'nytimes.com'

r  = requests.get("http://" +url)

f = open('nyTimes.txt','w')

data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all('a'):
   if re.match(regex,link.get('href')):
      r = requests.get(link.get('href'))
      new_data = r.text
      article = BeautifulSoup(new_data)
      if article.find('h1',{'class':'headline'}).get_text() in articleList:
         continue
      else:
         articleList.append(article.find('h1',{'class':'headline'}).get_text())
         f.write(articleList[-1])
         for each_p in article.findAll('p',{'class':'story-body-text story-content'}):
            f.write(each_p.get_text())
         f.write('\n')
