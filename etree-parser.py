#!/usr/bin/python

import xml.etree.ElementTree as etree

tree = etree.parse('document.xml')
root = tree.getroot()

print root

print len(root)
for child in root:
    print '> ', child
    print '> ', child.attrib
    for next_child in child:
        print '>> ', next_child
        print '>> ', next_child.attrib

all_ethernet = tree.findall('//class')
