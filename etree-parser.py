#!/usr/local/bin/python2.7

from sqlalchemy import create_engine, Table, MetaData, orm, Integer, ForeignKey, Column, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# db credentials
db_user = 'root'
db_pass = ''
db_host = 'localhost'
db_name = 'hcl'

xml_line = ''
sql_engine = create_engine("mysql://" + db_user + ":" + db_pass + "@" + db_host +"/" + db_name, echo=True)
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

Base.metadata.create_all(sql_engine)

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

# vendor sql object
server_vendor_obj = Server_vendor(name=server_vendor_name)
# server sql object
server_obj = Server(name = server_name, vendor = server_vendor_obj)

session.add(server_vendor_obj)
session.add(server_obj)
session.commit()




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