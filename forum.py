import scrapy
import lxml.etree
import lxml.html
import re
import urllib2
from bs4 import BeautifulSoup
import json
import forumPost

dict={}
html = urllib2.urlopen('https://www.hackthissite.org/forums/viewforum.php?f=159&sid=6187af2d9b63b60463eeb5436594babf')
soup = BeautifulSoup(html,'html.parser')

divList = soup.findAll('dt', attrs={ "title" : "No new posts"}) 

for div in divList:
	for a in div.findAll('a'):
		url='https://www.hackthissite.org/forums'+ a['href'][1:]
		forumPost.mainpage(url,dict) 
			