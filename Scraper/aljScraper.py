from bs4 import BeautifulSoup
import urllib.request
import sys
import os
import bisect
from bisect import bisect_left

class urlScraper:
    def __init__(self, url):
        self.url = urlScraper.httpPrefix(url)
        self.site = urlScraper.getSite(url)
        self.soup = urlScraper.getSoup(url)
        self.text = urlScraper.getText(self)
        self.links = urlScraper.getLinks(self)
        
    def getSoup(url):
        soup = None
        request = urllib.request.Request(url)
        with urllib.request.urlopen(request) as page:
            html = page.read()
            soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def getText(self):
        soup = self.soup
        results = soup.findAll('div', attrs={'class':'main-article-body'})
        text = []
        for result in results:
            text += result.findAll(text = True)
        return urlScraper.clean_text(text)
    
    def clean_text(text):
        cleaned = ""
        for segment in text:
            segment = segment.replace('\n', ' ')
            cleaned += segment + " "
        cleaned = ' '.join(cleaned.split())
        if cleaned != '':
            cleaned += '\n'
        return cleaned
        
    def getSite(url): #get site name like cnn.com without prefix or www
        if (url == None):
            site = ''
        elif (url[:7] == 'http://'):
            site = url[7:].split('/')[0]
        elif(url[:8] == 'https://'):
            site = url[8:].split('/')[0]
        else:
            site = url.split('/')[0]
        if (site[:4] == 'www.'):
            site = site[4:]
        return site
    
    def httpPrefix(url):
        if (url == None):
            site = ''
        else:
            if(url[:8] == 'https://'):
                site = url[8:]
            if (url[:7] == 'http://'):
                site = url[7:]
            if (url[:4] == 'www.'):
                site = url[4:]
            else:
                site = url
        return "http://www." + site

    
    def getLinks(self):
        linkList = []
        #print(self.site)
        for link in self.soup.find_all('a'):
            linkUrl = link.get('href')
            if (linkUrl != None):
                if (linkUrl[:1] == '/' and linkUrl[:2] != '//'): #relative path & avoiding //preferences-mgr.truste.com/?pid=turnermedia01&aid=turnermedia01
                    linkUrl = self.site + linkUrl
                linkUrl = urlScraper.httpPrefix(linkUrl)
                linkSite = urlScraper.getSite(linkUrl)
                if linkUrl[-1:] == "/":
                    linkUrl = linkUrl[:len(linkUrl) - 1]
                #print('link is {} site id {}'.format((linkUrl), self.site))
                #print('link is {} site id {}'.format(linkSite, self.site))
                if (linkSite == self.site):
                    #print('link is {} site id {}'.format((linkUrl), self.site))
                    if linkUrl not in linkList:
                        #print('inserting')
                        linkList.append(linkUrl)
        return sorted(linkList)

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    return -1 #raise ValueError
    
path = "../Datasets/"
todoFile = path + "aljTodo"
visitedFile = path + "aljVisited"
datasetFile = path + "aljDataset"
for file in [todoFile, visitedFile, datasetFile]:
    if not os.path.exists(file):
        open(file, 'w').close()
    
onlyFound = True
count = 5
#while count:
#    count -=1
while os.path.getsize(todoFile) != 0:
    visited = []
    todo = []
    for line in open(visitedFile, 'r'):
        visited.append(line.strip()) #load the sorted array of visited sites
    #print('visited nodes are {}'.format(visited))
    for line in open(todoFile, 'r'):
        todo.append(line.strip())
    #print('todo nodes are {}'.format(todo))
    todoTemp = list(todo)
    for url in todoTemp:
        #print('in for loop processing {}'.format(url))
        if index(visited, url) != -1: #if url already visited
            print('{} found in visited'.format(url))
            todo.remove(url)
        else:
            print('{} not found in visited'.format(url))
            onlyFound = False
            #print('process {}'.format(url))########################################
            obj = urlScraper(url)
            with open(datasetFile, 'a') as f:
                try:
                    f.write(str(obj.text))
                except:
                    print("Error writing line")
            todo.remove(url) #remove from todo
            bisect.insort(visited, url) #insert into visited
            todo.extend(obj.links)
            with open(todoFile, 'w') as f:
                f.write('\n'.join(todo))
            with open(visitedFile, 'w') as f:
                f.write('\n'.join(visited))
            break
    if onlyFound:
        print('all entries in todo were found in visited, zeroing')
        open(todoFile, 'w').close() #zero file
print("Finished")
