#!/usr/local/bin/python2.7
from lxml import etree
import sys
from sqlalchemy import create_engine, Table, MetaData, orm, Integer, ForeignKey, Column, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from termcolor import colored

# db credentials
db_user = 'root'
db_pass = 'Admin112'
db_host = 'localhost'
db_name = 'hcl_test'

xml_line = ''
sql_engine = create_engine("mysql://" + db_user + ":" + db_pass + "@" + db_host +"/" + db_name) #, echo=True)
Session = sessionmaker(bind=sql_engine)
session = Session()
# DB prepare
Base = declarative_base()

class Validation(Base):
    __tablename__       = 'validation'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    server_id           = Column(Integer, ForeignKey("server.id"), nullable=False, primary_key=True)
    release_id          = Column(Integer, ForeignKey("releases.id"), nullable=False, primary_key=True)
    val_date            = Column(DateTime, nullable=False)
    customized_bootstrap = Column(Integer)
    notes               = Column(String(255))
    release             = relationship("Releases")
    server              = relationship("Server", backref=backref('server'), uselist=True, cascade='delete,all')
    dtv                 = relationship("Dev_to_validation", backref=backref('dtv'), uselist=True, cascade='delete,all')

class Server_vendor(Base):
    __tablename__       = 'server_vendor'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name                = Column(String(128), unique=True, nullable=False)
    server              = relationship("Server", backref=backref('servers', uselist=True, cascade='delete,all'))

class Server(Base):
    __tablename__       = 'server'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    server_vendor_id    = Column(Integer, ForeignKey("server_vendor.id"), nullable=False, primary_key=True)
    name                = Column(String(128), unique=True, nullable=False)
    notes               = Column(String(255))
    vendor              = relationship("Server_vendor")
    validation          = relationship("Validation")

class Releases(Base):
    __tablename__       = 'releases'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name                = Column(String(64), unique=True, nullable=False)
    validation          = relationship("Validation", backref=backref('validation'), uselist=True, cascade='delete,all')

class Dev_to_validation(Base):
    __tablename__       = 'dev_to_validation'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    validation_id       = Column(Integer, ForeignKey("validation.id"), nullable=False, primary_key=True)
    device_id           = Column(Integer, ForeignKey("device.id"), primary_key=True, nullable=False)
    driver_name         = Column(String(128), nullable=False)
    driver_ver          = Column(String(64), nullable=False)
    is_work             = Column(Boolean)
    validation          = relationship("Validation")
    device              = relationship("Device")


class Device(Base):
    __tablename__       = 'device'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name                = Column(String(128), unique=True, nullable=False)
    type                = Column(String(64), nullable=False)
    description         = Column(String(255))
    device_maker_id     = Column(Integer, ForeignKey("device_maker.id"), primary_key=True, nullable=False)
    maker               = relationship("Device_maker")
    dtv                 = relationship("Dev_to_validation")

class Device_maker(Base):
    __tablename__       = 'device_maker'
    __table_args__      = {'mysql_engine':'InnoDB'}
    id                  = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name                = Column(String(128), unique=True, nullable=False)
    device              = relationship("Device", backref=backref('devices', uselist=True, cascade='delete,all'))

#Base.metadata.create_all(sql_engine)

if len(sys.argv) < 2:
    print "Use the Params Luke..."
    print sys.argv[0], " hw_report_filename.txt"
    exit(0)

print colored("Parsing ", 'cyan'), sys.argv[1]
document = sys.argv[1]
# try to open report file
try:
    xml_report = open(document, 'r')
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    exit(1)

# parsing
for line in xml_report:
    if line.startswith('Date:'):            # Date field
        line.strip()
        twodots = line.find(':')            # search for :
        v_date = line[twodots+1:].strip()   # get value after :
        continue
    if line.startswith('Fuel version'):
        line.strip()
        twodots = line.find(':')
        v_fuel =  line[twodots+1:].strip()
        continue
    if line.startswith('<?xml'):            # search for starting of xml
        xml_line = line
        continue
    if line.strip().startswith('<') and line.strip() != '</list>':      # xml
        xml_line += line                    # add xml lines to str
    if line.strip() == '</list>':           # xml ends
        xml_line += line
        break



if len(xml_line.strip()) > 0:               # if xml String size not null
    tree = etree.fromstring(xml_line)       # parse xml
else:
    print "XML file is broken"
    exit(0)

# get server info
server_info = tree.xpath('/list/node')
# server name
server_name = server_info[0].find('product').text
# server vendor
server_vendor_name = server_info[0].find('vendor').text

# supermicro hack
if server_name.find('To be filled by') != -1:
    server_name = server_name.split('(')[0]
    server_name = server_name.rstrip()

#validation_obj = validation
# NICs
# looking for nodes with class network
step = 1
nics = tree.xpath('/list/node/node[@id="core"]/descendant::node[@class="network"]')
for nic in nics:
    print colored("Device #", 'yellow'), colored(step, 'yellow'), colored("found!",'yellow')
    nic_name = nic.find('product')
    nic_type = nic.find('description')
    nic_vendor = nic.find('vendor')
    # lookging for subvalues with drivers info
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
    try:
        # check if found device is in DB
        dev = session.query(Device).filter(Device.name == nic_name.text).one()
        print "Device", colored(dev.name, 'white', attrs=['bold']), colored("[", 'green'), colored(nic_vendor.text, 'green'), colored("]", 'green'), "is already in DB"
    # if there is no that device in DB...
    except:
        try:
            # check if device's vendor is in DB
            devmaker = session.query(Device_maker).filter(Device_maker.name == nic_vendor.text).one()
            # if vendor is in DB...
            device_obj = Device(name = nic_name.text, type = 'nic', device_maker_id = devmaker.id)
            session.add(device_obj)
            print "Vendor", colored(devmaker.name, 'green'), "already in DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
        except:
            # if vendor is not in DB...
            print "Vendor", colored(nic_vendor.text, 'green'), "is not in DB..."
            device_maker_obj = Device_maker(name = nic_vendor.text)
            device_obj = Device(name = nic_name.text, type = 'nic', maker = device_maker_obj)
            session.add(device_maker_obj)
            session.add(device_obj)
            print "Adding vendor", colored(device_maker_obj.name, 'green'), "to DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
    session.commit()
    step = step+1

# RAIDs
# looking for nodes which ids starts from storage and has class storage
raids = tree.xpath('/list/node/node[@id="core"]/descendant::node[starts-with(@id,"storage") and @class="storage"]')
for raidcnt in raids:
    print colored("Device #", 'yellow'), colored(step, 'yellow'), colored("found!",'yellow')
    nic_name = nic.find('product')
    # if there is no that device in DB...
    nic_name = nic.find('product')
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
    try:
        # check if found device is in DB
        dev = session.query(Device).filter(Device.name == raid_name.text).one()
        print "Device", colored(dev.name, 'white', attrs=['bold']), colored("[", 'green'), colored(raid_vendor.text, 'green'), colored("]", 'green'), "is already in DB"
    # if there is no that device in DB...
    except:
        try:
            # check if device's vendor is in DB
            devmaker = session.query(Device_maker).filter(Device_maker.name == raid_vendor.text).one()
            # if vendor is in DB...
            device_obj = Device(name = raid_name.text, type = 'raid', device_maker_id = devmaker.id)
            session.add(device_obj)
            print "Vendor", colored(devmaker.name, 'green'), "already in DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
        except:
            # if vendor is not in DB...
            print "Vendor", colored(raid_vendor.text, 'green'), "is not in DB..."
            device_maker_obj = Device_maker(name = raid_vendor.text)
            device_obj = Device(name = raid_name.text, type = 'raid', maker = device_maker_obj)
            session.add(device_maker_obj)
            session.add(device_obj)
            print "Adding vendor", colored(device_maker_obj.name, 'green'), "to DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
    session.commit()
    step = step+1


# vendor sql object
server_vendor_obj = Server_vendor(name=server_vendor_name)
# server sql object
server_obj = Server(name = server_name, vendor = server_vendor_obj)
release_obj = Releases(name = v_fuel)

#session.add(server_vendor_obj)
#session.add(server_obj)
#session.commit()
