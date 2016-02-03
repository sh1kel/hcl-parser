#!/usr/bin/python

xml = 'document.xml'
from lxml import etree
tree = etree.parse('document.xml')


nodes = tree.xpath('/list/node/node[@id="core"]/node[starts-with(@id,"pci:")]/node[@class="network"]/product') 
#print nodes
for node in nodes:
	print node.text
	#print node.tag
	#print node.keys()
	#print node.values()
