#!/usr/bin/python

from lxml import etree
tree = etree.parse('document2.xml')


nics = tree.xpath('/list/node/node[@id="core"]/descendant::node[@class="network"]')
for nic in nics:
    nic_name = nic.find('product')
    nic_type = nic.find('description')
    nic_vendor = nic.find('vendor')
    nic_driver_name_obj = nic.find('configuration/setting[@id="driver"]')
    nic_driver_ver_obj = nic.find('configuration/setting[@id="driverversion"]')
    try:
        nic_driver_name = nic_driver_name_obj.get('value')
    except:
        nic_driver_name = "unknown"
    try:
        nic_driver_ver = nic_driver_ver_obj.get('value')
    except:
        nic_driver_ver = "unknown"
    print "Device: ", nic_name.text
    print "Vendor: ", nic_vendor.text
    print "Driver name: ", nic_driver_name
    print "Driver version: ", nic_driver_ver

raids = tree.xpath('/list/node/node[@id="core"]/descendant::node[starts-with(@id,"storage") and @class="storage"]')
for raidcnt in raids:
    raid_name = raidcnt.find('product')
    raid_type = raidcnt.find('description')
    raid_vendor = raidcnt.find('vendor')
    raid_driver_name_obj = raidcnt.find('configuration/setting[@id="driver"]')
    raid_driver_ver_obj = raidcnt.find('configuration/setting[@id="driverversion"]')
    try:
        raid_driver_name = raid_driver_name_obj.get('value')
    except:
        raid_driver_name = "unknown"
    try:
        raid_driver_ver = raid_driver_ver_obj.get('value')
    except:
        raid_driver_ver = "unknown"
    print "Device: ", raid_name.text
    print "Vendor: ", raid_vendor.text
    print "Driver name: ", raid_driver_name
    print "Driver version: ", raid_driver_ver
