from bs4 import BeautifulSoup

import requests

import re

regex = re.compile('https://www.foxnews.com/*')

articleList = []

url = 'foxnews.com'

r  = requests.get("https://" +url)

f = open('foxNews.txt','w')

data = r.text

soup = BeautifulSoup(data)

maxArticles = 10000;

i = 0;

for link in soup.find_all('a'):
#   if re.match(regex,link.get('href')):
      try:
         r = requests.get(link.get('href'))
         new_data = r.text
         article = BeautifulSoup(new_data)
      except:
         continue

      print(link.get('href'))

      try:
         if article.find('h1',{'class':'headline head1'}).get_text() in articleList:
            continue
         else:
 #           i = i + 1
            articleList.append(article.find('h1',{'class':'headline head1'}).get_text())
            f.write(articleList[-1])
            f.write(' ')
            for each_p in article.findAll('p'): 
               f.write(' ')
               f.write(each_p.get_text())
               f.write(' ')
            f.write('\n')
      except:
         continue
#      if i > maxArticles:
#         break

f.close()
