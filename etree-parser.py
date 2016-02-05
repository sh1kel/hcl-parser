#!/usr/local/bin/python2.7

from lxml import etree
import sys
from sqlalchemy import create_engine, Table, MetaData, orm

# db credentials
db_user = 'root'
db_pass = ''
db_host = 'localhost'
db_name = 'hcl'

xml_line = ''
sql_engine = create_engine("mysql://db_user:db_pass@db_host/db_name", echo=True)

# DB prepare
Base = declarative_base()

class validation(Base):
    __tablename__ = 'validation'
    id          = Column(integer, primary_key=True)
    server_id   = Column(integer)
    release_id  = Column(integer)
    val_date    = Column(datetime)
    customized_bootstrap = Column(integer)
    notes       = Column(string)

    class server(Base):
    __tablename__       = 'server'
    id                  = Column(integer, primary_key=True)
    server_vendor_id    = Column(integer)
    name                = Column(string)
    notes               = Column(string)

class server_vendor(Base):
    __tablename__       = 'server_vendor'
    id                  = Column(integer, primary_key=True)
    name                = Column(string)

class releases(Base):
    __tablename__       = 'releases'
    id                  = Column(integer, primary_key=True)
    name                = Column(string)

class dev_to_validation(Base):
    __tablename__       = 'dev-to-validation'
    id                  = Column(integer, primary_key=True)
    validation_id       = Column(integer)
    device_id           = Column(integer)
    driver_name         = Column(string)
    driver_ver          = Column(string)
    is_work             = Column(bool)

class device(Base):
    __tablename__       = 'device'
    id                  = Column(integer, primary_key=True)
    name                = Column(string)
    type                = Column(string)
    description         = Column(string)
    device_maker_id     = Column(integer)

class device_maker(Base):
    __tablename__       = 'device_maker'
    id                  = Column(integer, primary_key=True)
    name                = Column(string)


if len(sys.argv) < 2:
    print "Use the Params Luke..."
    print sys.argv[0], " hw_report_filename.txt"
    exit(0)

print "Parsing ", sys.argv[1]
document = sys.argv[1]

try:
    xml_report = open(document, 'r')
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    exit(1)

for line in xml_report:
    if line.startswith('Date:'):
        line.strip()
        twodots = line.find(':')
        v_date = line[twodots+1:].strip()
        print v_date
        continue
    if line.startswith('Fuel version'):
        line.strip()
        twodots = line.find(':')
        v_fuel =  line[twodots+1:].strip()
        print v_fuel
        continue
    if line.startswith('<?xml'):
        xml_line = line #[0:-1]
        continue
    if line.strip().startswith('<') and line.strip() != '</list>':
        xml_line += line #[0:-1]
    if line.strip() == '</list>':
        xml_line += line #[0:-1]
        break

if len(xml_line.strip()) > 0:
    tree = etree.fromstring(xml_line)
else:
    print "XML file is broken"
    exit(0)

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