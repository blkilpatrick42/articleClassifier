# Author: Patrick Blanchard
# Date: 10-26-17
# Description: Scrapes CNN for news articles

from bs4 import BeautifulSoup 
import urllib

# collects links from page and adds them to a queue
# max_size determines how large the queue can get before exiting
# returns a list of articles
def crawl(domain, max_size):
	queue = set([domain])
	dataset = []	

	while len(queue) < max_size:
		url = queue.pop()
		page = get_page(url)
		links = get_links(page, domain)
		text = extract_article(page)
		if len(text) > 0:
			dataset.append(text)
		queue.update(links)

	return dataset

# extracts links from a page
# returns a list of links
def get_links(page, domain):
	try:
		soup = BeautifulSoup(page, 'html5lib')
	except:
		return ''

	links = []
	a = soup.findAll('a')

	if a is not None:
		for link in a:
			link = link.get('href')
			if link is None or len(link) == 0:
				continue
			if domain in link and '.img' not in link and link not in links:
				links.append(link)
			elif link[0] is '/':
				link = domain + link
				if link not in links:
					links.append(link)
			elif "cnn" in link:
				if link not in links:
					links.append(link)
			else:
				continue

	return links

# gets html associated to the url
# returns html text
def get_page(url):
	try:
		with urllib.request.urlopen(url) as url:
			page = url.read()
		return page
	except:
		pass

# extracts article text from html page
# returns string of article
def extract_article(page):
	try:
		soup = BeautifulSoup(page, 'html5lib')
	except:
		return ''
	text = ''
	div = soup.findAll('div', {'class': 'l-container'})

	article = []
	for child in div:
		for p in child.findAll('p'):
			article.append(p)

	for p in article:
		text += '\n' + ''.join(p.findAll(text = True))

	body = soup.findAll('div', attrs={'class':'zn-body__paragraph'})
	for p in body:
		text += '\n' + ''.join(p.findAll(text = True))
	
	return text

# cleans the given dataset by removeing unecessary whitespace and newlines
# returns a list of cleaned articles
def clean_text(dataset):
	cleanset = set()
	for data in dataset:
		data = ' '.join(data.split())
		data = ' '.join(data.split('\n'))
		data += '\n'
		cleanset.update([data])
	return cleanset
		

if __name__ == '__main__':
	domain = 'http://www.cnn.com'
	size = 10000
	dataset = crawl(domain, size)
	cleanset = clean_text(dataset)
	with open("cnn_dataset", 'w') as f:
		for data in cleanset:
			f.write(data)
			f.flush()
	f.closed
