import urllib2
from bs4 import BeautifulSoup
import json
import time
import random

def page(url,dict):
	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html,'html.parser')
	divList = soup.findAll('div', attrs={ "data-role" : "commentContent"}) 
	divAuthors=soup.findAll('h3', attrs={ "class" : "ipsType_sectionHead cAuthorPane_author ipsResponsive_showPhone ipsResponsive_inlineBlock ipsType_break ipsType_blendLinks ipsTruncate ipsTruncate_line"})

	a=0
	authors=[]
	content=[]
	for div in divAuthors:
		authors.append(div.text.replace('\n',''))
	for div in divList:
		try:
			div.blockquote.decompose()
		except:
			a=a+1
		try:	
			div.span.decompose()
		except:
			a=a+1
		try:
			div.pre.decompose()
		except:
			a=a+1
		content.append(div.text)

	for i in range (len(authors)):
		if authors[i] not in dict:
			dict[authors[i]]=[]
			dict[authors[i]].append(content[i])
		else:
			if content[i] not in dict[authors[i]]:
				dict[authors[i]].append(content[i])

def pages(url,links):
	try:
		html = urllib2.urlopen(url)
		soup1 = BeautifulSoup(html,'html.parser')
		_pages = soup1.find('ul',attrs={'class':'ipsPagination'})
		_pages = _pages.findAll('li',attrs={'class':'ipsPagination_page'})

		try:
			for page in _pages:
				try:
					if page.a['href'] not in links:
						links.append(page.a['href'])
				except: 
					continue

		except Exception,e:
			print str(e)
	except Exception,e:
		print str(e)
	return links

def _innerpages(url,links):
	# try:
	html = urllib2.urlopen(url)
	soup1 = BeautifulSoup(html,'html.parser')
	# _pages = soup1.find('ul',attrs={'class':'ipsPagination'})
	_pages = soup1.findAll('li',attrs={'class':'ipsPagination_page'})

	try:
		for page in _pages:
			try:
				if page.a['href'] not in links:
					links.append(page.a['href'])
			except: 
				continue

	except Exception,e:
		print str(e)
	# except Exception,e:
	# 	print str(e)
	return links

def forumPost(u,dict): 
	links=[]
	links =_innerpages(u,links)
	if len(links)!=0:		 
		try: 
			size=len(links)
		except:
			size=0
		u1=links[-1]
		temp=[]
		count=0
		while (1):	
			count+=1
			try:	
				links=_innerpages(u1,links)
				
				if len(links)<=size:
					break
				else:
					size=len(links)
					u1=links[-1]
			except:
				break
		for link in links:
			page(link,dict)
		with open('hak5.json', 'w') as fp:
		    json.dump(dict, fp)

def forumPage(u,dict):
	html = urllib2.urlopen(u)
	soup = BeautifulSoup(html,'html.parser')
	divList = soup.findAll('span', attrs={ "class" : "ipsType_break ipsContained"})
	pagesList=[]
	for div in divList: 
		if div.a['href'] not in pagesList:
			pagesList.append(div.a['href'])
	for _page in pagesList:
		forumPost(_page,dict)
	time.sleep(random.randint(1,5))	
			

dict={}
u='https://forums.hak5.org/forum/43-security/'
_links=[]
_links =pages(u,_links)
if len(_links)!=0:		 
	try: 
		size=len(_links)
	except:
		size=0
	u1=_links[-1]
	# print u1
	temp=[]
	count=0
	while (1):	
		count+=1
		try:	
			_links=pages(u1,_links)
			
			if len(_links)<=size:
				break
			else:
				size=len(_links)
				u1=_links[-1]
		except:
			break
count=0
for _link in _links:
	# time.sleep(random.randint(1,5))	
	count+=1
	print str(100*(count/float(len(_links))))[:4]+'%'
	forumPage(_link,dict)

# forumPost('https://forums.hak5.org/topic/45140-internal-ip%E2%80%99s-visible-on-wan-port/',dict)