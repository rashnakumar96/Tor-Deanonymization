import scrapy
import lxml.etree
import lxml.html
import re
import urllib2
from bs4 import BeautifulSoup
import json
import time
import random

# dict ={}

# u = 'https://www.hackthissite.org/forums/viewtopic.php?f=159&t=12319&sid=9f8b185c0c544a5144b0eb59f89a2d4d'

def _page(url,dict):
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html,'html.parser')
	divList = soup.findAll('div', attrs={ "class" : "postbody"}) 
	# divList = soup.findAll('div', attrs={ "class" : "postbody"}) 
	for div in divList:
		for l in div:
			try:
				if l['class'][0] == 'author':
					author= l.text.split(' ')[1]
				if l['class'][0] == 'content':
					l.blockquote.decompose()
					content = l.text
					# break
				if author not in dict:
					dict[author]=[]
					dict[author].append(content)	

				else:
					if content not in dict[author]:
						dict[author].append(content)	
			except:
				continue

def mainpage(u,dict,no):
	html = urllib2.urlopen(u)
	soup1 = BeautifulSoup(html,'html.parser')
	pages = soup1.find('div',attrs={'class':'pagination'})
	links = []
	try:
		for page in pages.span:
			try:
				links.append(page['href'])
			except: 
				continue
	except Exception,e:
		print str(e)

	# print links
	_page(u,dict)
	for link in links:
		url = 'https://www.hackthissite.org/forums'+link[1:]
		_page(url,dict)

	time.sleep(random.randint(1,5))	
	with open('weLiveSecurity'+no+'.json', 'w') as fp:
	    json.dump(dict, fp)





