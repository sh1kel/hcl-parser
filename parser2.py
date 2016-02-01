#!/usr/bin/python

import xmltodict
with open('document.xml') as fd:
	doc = xmltodict.parse(fd.read())

for y in doc['list']['node']['node']:
	#print doc['list']['node']['node'][y] #['@class']
	if y['@class'] == 'network':
		for x in y:
			print x['description']
			print "----"	

#print doc['list']['node']['node']


