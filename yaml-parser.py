#!/usr/bin/python
import yaml
import sys
from sqlalchemy import create_engine, Table, MetaData, orm, Integer, ForeignKey, Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from termcolor import colored
from datetime import datetime

# db credentials
db_user = 'root'
db_pass = '123'
db_host = '192.168.27.10'
db_name = 'hcl_test'

val_list = []
DATE_FORMATS = ['%Y-%m-%d %H:%M:%S.%f', '%d %b %Y %H:%M', '%Y-%m-%d %H:%M']

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
    result              = Column(Enum('passed','partially passed','failed'))
    notes               = Column(String(4000))
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

# preparing for parsing

if len(sys.argv) < 2:
    print "Use the Params Luke..."
    print sys.argv[0], " hw_report_filename.txt"
    exit(0)

print colored("Parsing ", 'cyan'), sys.argv[1]
document = sys.argv[1]
# try to open report file
try:
    yaml_report = open(sys.argv[1], 'r')
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    exit(1)

try:
    server_info = yaml.load(yaml_report)
except:
    print sys.argv[1], colored("is not YAML format", 'red')
    exit(1)

# prepared

# *******************************************************************************************************
# *                                         DB Filling                                                  *
# *******************************************************************************************************

server_name = server_info['server']['name']
server_vendor_name = server_info['server']['vendor']

# Server info
print colored('***** Server info *****', 'blue',  attrs=['bold'])
try:
    server_obj = session.query(Server).filter(Server.name == server_name).one()
    print "Server", colored(server_obj.name, 'white', attrs=['bold']), "already in DB"
# if there is no that server in DB...
except:
    try:
        # try to find server's vendor is in DB
        server_vendor_obj = session.query(Server_vendor).filter(Server_vendor.name == server_vendor_name).one()
        # if vendor is in DB
        server_obj = Server(name = server_name, server_vendor_id = server_vendor_obj.id)
        print "Server vendor", colored(server_vendor_obj.name, 'green', attrs=['bold']), "already in DB"
        print "Adding server", colored(server_obj.name, 'white', attrs=['bold']), " to DB"
        session.add(server_obj)
    except:
        # if vendor is not in DB
        print "Server vendor", colored(server_vendor_name, 'green', attrs=['bold']), "is not in DB..."
        server_vendor_obj = Server_vendor(name=server_vendor_name)
        server_obj = Server(name = server_name, vendor = server_vendor_obj)
        session.add(server_vendor_obj)
        session.add(server_obj)
        print "Adding server vendor", colored(server_vendor_obj.name, 'green'), "to DB"
        print "Adding server", colored(server_obj.name, 'white', attrs=['bold']), " to DB"
session.commit()

# Release and Validation info
for cert in server_info['certification']:
    v_fuel = cert['fuel_version']
    try:
        release_obj = session.query(Releases).filter(Releases.name == v_fuel).one()
        print "Release", colored(release_obj.name, 'white', attrs=['bold']), "already in DB"
    except:
        release_obj = Releases(name = v_fuel)
        session.add(release_obj)
        print "Adding release", colored(release_obj.name, 'white', attrs=['bold']), " to DB"
        session.commit()
    for date_format in DATE_FORMATS:
        try:
            dt = datetime.strptime(cert['date'], date_format) 
            dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    #if 'status' in cert and cert['status'] == 'Passed':    
    validation_obj = Validation(server_id = server_obj.id, release_id = release_obj.id, val_date = dt, result = 'passed')
    val_list.append(validation_obj)
    session.add(validation_obj)
    session.commit()

# Hardware info
step = 1
for hw in server_info['components']:
    device_name         = hw['name']
    device_vendor       = hw['vendor']
    device_type         = hw['type']
    device_driver_name  = hw['driver']['name']
    device_driver_ver   = hw['driver']['version'] 
    try:
        # try to find device in DB
        device_obj = session.query(Device).filter(Device.name == device_name).one()
        print "Device", colored(device_obj.name, 'white', attrs=['bold']), colored("[", 'green'), colored(device_vendor, 'green'), colored("]", 'green'), "is already in DB"
    # if there is no that device in DB...
    except:
        try:
            # try to find device's vendor is in DB
            devmaker = session.query(Device_maker).filter(Device_maker.name == device_vendor).one()
            # if vendor is in DB...
            device_obj = Device(name = device_name, type = device_type, device_maker_id = devmaker.id)
            session.add(device_obj)
            print "Vendor", colored(devmaker.name, 'green'), "already in DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
            session.commit()
        except:
            # if vendor is not in DB...
            print "Vendor", colored(device_vendor, 'green'), "is not in DB..."
            device_maker_obj = Device_maker(name = device_vendor)
            device_obj = Device(name = device_name, type = device_type, maker = device_maker_obj)
            print "Adding vendor", colored(device_maker_obj.name, 'green'), "to DB"
            print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
            session.add(device_maker_obj)
            session.add(device_obj)
            session.commit()
    for val_elem in val_list:
        dev_to_val_obj = Dev_to_validation(validation = val_elem, device_id = device_obj.id, driver_name = device_driver_name, driver_ver =  device_driver_ver)
        session.add(dev_to_val_obj)
        session.commit()
    step = step+1
