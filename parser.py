#!/usr/bin/python

#from lxml import etree
#import xml.dom.minidom as minidom
#import elementtree.ElementTree as ET
import xml.etree.cElementTree as ET

#tree = etree.parse('document.xml')
#print tree.xpath("/list/node/product/text()")
sourcefile = ('document.xml')

nodelist = ET.ElementTree(file=sourcefile)

#tree = minidom.parse(sourcefile)

#nodelist = tree.getElementsByTagName('node')
#print(len(nodelist))
#for node in nodelist:
#	if node.attributes['class'].value == 'network':
#		print (node.attributes['id'].value)


#for node in nodelist.iter('description'):
#	node_class = node.\xattrib.get('description')
#	if node_class == 'Ethernet interface':
#		print node_class

root = nodelist.getroot()

print "tag=%s, attrib=%s" % (root.tag, root.attrib)
for child in root:
	#print "\t", child.tag, child.attrib
	for step_child1 in child:
		#print "\t\t", step_child1.tag, step_child1.attrib
		for step_child2 in step_child1:
			print "\t\t\t", step_child2.tag
			print "---"
#ET.dump(tree)

