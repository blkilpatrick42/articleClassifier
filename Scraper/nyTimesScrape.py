from bs4 import BeautifulSoup

import requests

import re

regex = re.compile('https://www.nytimes.com/2017/*')

articleList = []

urlList = ['nytimes.com', 
           'nytimes.com/section/world', 
           'nytimes.com/section/us',
           'nytimes.com/section/nyregion',
           'nytimes.com/section/business',
           'nytimes.com/section/opinion',
           'nytimes.com/section/technology',
           'nytimes.com/section/science',
           'nytimes.com/section/health',
           'nytimes.com/section/sports',
           'nytimes.com/section/arts']
f = open('nyTimes.txt','w')

for url in urlList:
   r  = requests.get("http://" + url)
   data = r.text
   soup = BeautifulSoup(data)
   for link in soup.find_all('a'):
      if re.match(regex,link.get('href')):
         r = requests.get(link.get('href'))
         new_data = r.text
         article = BeautifulSoup(new_data)
         print(link.get('href'))
         try:
            if article.find('h1',{'class':'headline'}).get_text() in articleList:
               continue
            else:
               articleList.append(article.find('h1',{'class':'headline'}).get_text())
               f.write(articleList[-1])
               f.write(' ')
               for each_p in article.findAll('p',{'class':'story-body-text story-content'}):
                  f.write(each_p.get_text())
               f.write('\n')
         except:
            continue

f.close()
