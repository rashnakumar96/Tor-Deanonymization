import scrapy
import lxml.etree
import lxml.html
import re
import urllib2
from bs4 import BeautifulSoup
import json
import forumPost
import threading

def firstPage(pageLink):
	topics=[]
	html=urllib2.urlopen(pageLink)
	soup = BeautifulSoup(html,'html.parser')

	divList = soup.findAll('dt', attrs={ "title" : "No new posts"}) 

	for div in divList:
		for a in div.findAll('a'):
			url='https://www.hackthissite.org/forums'+ a['href'][1:]
			topics.append(url)
	return topics

def page(pageLink,dict,no):
	html=urllib2.urlopen(pageLink)
	soup = BeautifulSoup(html,'html.parser')

	divList = soup.findAll('dt', attrs={ "title" : "No new posts"}) 

	for div in divList:
		for a in div.findAll('a'):
			url='https://www.hackthissite.org/forums'+ a['href'][1:]
			forumPost.mainpage(url,dict,no) 

def pages(u,links):
	html = urllib2.urlopen(u)
	soup1 = BeautifulSoup(html,'html.parser')
	pages = soup1.find('div',attrs={"class":"pagination"})
	try:
		for page in pages.span:
			try:
				if page['href'] not in links:
					links.append(page['href'])
			except: 
				continue
		return links
			
	except Exception,e:
		print str(e)

# topics=firstPage('https://www.hackthissite.org/forums/index.php?sid=1964bad7dc6631e9e2ec8f5d0fde55eb')
def _topics(u,no):
	# print 'HEREEE'
# topics=topics[13:]
	dict={}
# for topic in topics:

	try:
		links=[]
		# u=topic
		# u='https://www.hackthissite.org/forums/viewforum.php?f=37&sid=458c7ccd9bda99388a50dc85af5ec80f'
		# u='https://www.hackthissite.org/forums/viewforum.php?f=79&sid=b5476ebdde904aea908cff2c64ee1c8a'		
		links =pages(u,links)
		try: 
			size=len(links)
		except:
			size=0
		u1='https://www.hackthissite.org/forums'+links[-2][1:]
		temp=[]
		count=0
		while (1):	
			count+=1
			try:	
				links=pages(u1,links[:-1])
				
				if len(links)<=size:
					break
				else:
					size=len(links)
					u1='https://www.hackthissite.org/forums'+links[-2][1:]
					print 'LINKKKKK'+u1
			except:
				break
		for l in links:
			l='https://www.hackthissite.org/forums'+l[1:]
			print l
			page(l,dict,no)
		print 'Thread  '+str(threading.currentThread().getName())+':   Len of links: '+str(len(links))
	except Exception,e:
		print str(e)+"IZ COOOOL"		

topicsList=firstPage('https://www.hackthissite.org/forums/index.php?sid=1964bad7dc6631e9e2ec8f5d0fde55eb')
topicsList=topicsList[13:]
with open('topics.json','w') as f:
	json.dump(topicsList,f)

topicsList = json.load(open('topics.json'))

threads=[]
for x in range(len(topicsList)):
	u=topicsList[x]
	print u
	# u='https://www.hackthissite.org/forums/viewforum.php?f=37&sid=458c7ccd9bda99388a50dc85af5ec80f'

	threads.append(threading.Thread(name=str(x),target=_topics,args=(u,str(x))))
	
	# break
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
