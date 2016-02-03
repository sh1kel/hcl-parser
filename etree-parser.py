#!/usr/bin/python

from lxml import etree
tree = etree.parse('document.xml')


nics = tree.xpath('/list/node/node[@id="core"]/descendant::node[@class="network"]')
for nic in nics:
    nic_name = nic.find('product')
    nic_type = nic.find('description')
    nic_vendor = nic.find('vendor')
    nic_driver_name = nic.find('configuration/setting[@id="driver"]').get('value')
    nic_driver_ver = nic.find('configuration/setting[@id="driverversion"]').get('value')
    print nic_name.text
    print nic_vendor.text
    print nic_driver_name, nic_driver_ver

