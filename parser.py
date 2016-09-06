#!/usr/bin/python
from lxml import etree
import sys
from sqlalchemy import create_engine, Table, MetaData, orm, Integer, ForeignKey, Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from termcolor import colored
from datetime import datetime

# db credentials
db_user = ''
db_pass = ''
db_host = ''
db_name = ''

v_fuel = 'unknown'
xml_started = 0

vendor_list = ['Dell','Cisco','VMware','Fujitsu','Huawei','Supermicro']

sql_engine = create_engine("mysql://" + db_user + ":" + db_pass + "@" + db_host +"/" + db_name) #, echo=True)
Session = sessionmaker(bind=sql_engine)
session_ex = Session()
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

Base.metadata.create_all(sql_engine)



# ************************* server info func *************************
def insert_server_info(session, server_name, server_vendor_name):
    print colored('***** Server info *****', 'blue',  attrs=['bold'])
    # try to find server in DB
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
    return server_obj.id


# ************************* release info func *************************
def insert_release_info(session, v_fuel):
    # add release info to DB
    try:
        release_obj = session.query(Releases).filter(Releases.name == v_fuel).one()
        print "Release", colored(release_obj.name, 'white', attrs=['bold']), "already in DB"
    except:
        release_obj = Releases(name = v_fuel)
        session.add(release_obj)
        print "Adding release", colored(release_obj.name, 'white', attrs=['bold']), " to DB"
        session.commit()
    return release_obj.id

# ************************* validation info func *************************
def insert_validation_info(session, serverid, releaseid, validation_date, result_value):

    DATE_FORMATS = ['%Y-%m-%d %H:%M:%S.%f', '%d %b %Y %H:%M', '%Y-%m-%d %H:%M']
    # validation
    for date_format in DATE_FORMATS:
        try:
            dt = datetime.strptime(validation_date, date_format) 
            dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
    validation_obj = Validation(server_id = serverid, release_id = releaseid, val_date = dt, result = result_value)
    session.add(validation_obj)
    session.commit()
    return validation_obj.id

# ************************* nic info func *************************
def insert_nic_info(session, tree, validationid):
    # NICs
    # looking for nodes with class network
    step = 1
    print colored('***** Devices *****', 'blue', attrs=['bold'])
    nics = tree.xpath('/list/node/node[@id="core"]/descendant::node[@class="network"]')
    for nic in nics:
        print colored("NIC device #", 'yellow', attrs=['bold']), colored(step, 'yellow', attrs=['bold']), colored("found!",'yellow', attrs=['bold'])
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
            # try to find device in DB
            device_obj = session.query(Device).filter(Device.name == nic_name.text).one()
            print "Device", colored(device_obj.name, 'white', attrs=['bold']), colored("[", 'green'), colored(nic_vendor.text, 'green'), colored("]", 'green'), "is already in DB"
        # if there is no that device in DB...
        except:
            try:
                # try to find device's vendor is in DB
                devmaker = session.query(Device_maker).filter(Device_maker.name == nic_vendor.text).one()
                # if vendor is in DB...
                device_obj = Device(name = nic_name.text, type = 'nic', device_maker_id = devmaker.id)
                session.add(device_obj)
                print "Vendor", colored(devmaker.name, 'green'), "already in DB"
                print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
                session.commit()
            except:
                # if vendor is not in DB...
                print "Vendor", colored(nic_vendor.text, 'green'), "is not in DB..."
                device_maker_obj = Device_maker(name = nic_vendor.text)
                device_obj = Device(name = nic_name.text, type = 'nic', maker = device_maker_obj)
                print "Adding vendor", colored(device_maker_obj.name, 'green'), "to DB"
                print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
                session.add(device_maker_obj)
                session.add(device_obj)
                session.commit()
        dev_to_val_obj = Dev_to_validation(validation_id = validationid, device_id = device_obj.id, driver_name = nic_driver_name, driver_ver =  nic_driver_ver)
        session.add(dev_to_val_obj)
        session.commit()
        step = step+1
    return

# ************************* raid info func *************************
def insert_raid_info(session, tree, validationid):
    # RAIDs
    # looking for nodes which ids starts from storage and has class storage
    step = 1
    raids = tree.xpath('/list/node/node[@id="core"]/descendant::node[starts-with(@id,"storage") and @class="storage"]')
    for raidcnt in raids:
        print colored("RAID device #", 'yellow', attrs=['bold']), colored(step, 'yellow', attrs=['bold']), colored("found!",'yellow', attrs=['bold'])
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
            # try to find device is in DB
            device_obj = session.query(Device).filter(Device.name == raid_name.text).one()
            print "Device", colored(device_obj.name, 'white', attrs=['bold']), colored("[", 'green'), colored(raid_vendor.text, 'green'), colored("]", 'green'), "is already in DB"
        # if there is no that device in DB...
        except:
            try:
                # try to find device's vendor is in DB
                devmaker = session.query(Device_maker).filter(Device_maker.name == raid_vendor.text).one()
                # if vendor is in DB...
                device_obj = Device(name = raid_name.text, type = 'raid', device_maker_id = devmaker.id)
                session.add(device_obj)
                print "Vendor", colored(devmaker.name, 'green'), "already in DB"
                print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
                session.commit()
            except:
                # if vendor is not in DB...
                print "Vendor", colored(raid_vendor.text, 'green'), "is not in DB..."
                device_maker_obj = Device_maker(name = raid_vendor.text)
                device_obj = Device(name = raid_name.text, type = 'raid', maker = device_maker_obj)
                print "Adding vendor", colored(device_maker_obj.name, 'green'), "to DB"
                print "Adding device", colored(device_obj.name, 'white', attrs=['bold']), " to DB"
                session.add(device_maker_obj)
                session.add(device_obj)
                session.commit()
        dev_to_val_obj = Dev_to_validation(validation_id = validationid, device_id = device_obj.id, driver_name = raid_driver_name, driver_ver =  raid_driver_ver)
        session.add(dev_to_val_obj)
        session.commit()
        step = step+1
    return

# ************************* parse func *************************
def parse_server(session, validation_date, fuel_version, rawxml):
    tree = etree.fromstring(rawxml)
    # get server info
    server_info = tree.xpath('/list/node')
    # server name
    server_name = server_info[0].find('product').text
    # server vendor
    server_vendor_name = server_info[0].find('vendor').text
    for vendor in vendor_list:
        if server_vendor_name.startswith(vendor):
            server_vendor_name = vendor
            break
    # supermicro hack
    if server_name.find('To be filled by') != -1:
        server_name = server_name.split('(')[0]
        server_name = server_name.rstrip()
    serverid = insert_server_info(session, server_name, server_vendor_name)
    releaseid = insert_release_info(session, fuel_version)
    validationid = insert_validation_info(session, serverid, releaseid, validation_date, 'passed')
    insert_nic_info(session, tree, validationid)
    insert_raid_info(session, tree, validationid)
    while True:
        is_correct = raw_input('Is it correct [Ja/Nicht]: ')
        if (is_correct.lower() == "j" or is_correct.lower() == "ja"):
            print 'Oh, ja! - Das ist fantastisch!'
            return
        elif (is_correct.lower() == "n" or is_correct.lower() == "nicht"):
            print 'Nicht Validaten!'
            session.query(Validation).filter(Validation.id == validationid).update({'result': 'failed'})
            #session.query(Validation).filter(Validation.server_id == serverid and Validation.release_id == releaseid).update({'result': 'failed'})
            session.commit()
            return
        else:
            print "Vvoditen J or N! Schneller!"
    return

# ************************* END FUNC *************************

# MAIN 

if len(sys.argv) < 2:
    print "Use the Params Luke..."
    print sys.argv[0], " hw_report_filename.txt"
    exit(0)

for report_arg in range(1, (len(sys.argv))):
    xml_line = []
    servers_num = 0
    print colored("Parsing ", 'cyan'), sys.argv[report_arg]
    document = sys.argv[report_arg]
    # try to open report file
    try:
        xml_report = open(document, 'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        continue
    for line in xml_report:
        if line.startswith('Date:'):            # Date field
            line.strip()
            twodots = line.find(':')            # search for :
            v_date = line[twodots+1:].strip()   # get value after :
            continue
        if line.startswith('Fuel version'):
            line.strip()
            twodots = line.find(':')
            v_fuel = line[twodots+1:].strip()
            continue
        if line.startswith('<?xml'):            # search for starting of xml
            xml_line.append(line)
            xml_started = 1
            continue
        if (xml_started == 1 and line.strip().startswith('<') and line.strip() != '</list>'):      # xml
            xml_line[servers_num] += line                    # add xml lines to str
            continue
        if (xml_started == 1 and line.strip() == '</list>'):           # xml ends
            xml_line[servers_num] += line
            servers_num += 1
            xml_started = 0
    for srv_report in xml_line:
        if len(srv_report.strip()) > 0:               # if xml String size not null
            parse_server(session_ex, v_date, v_fuel, srv_report)                  # parse xml
        else:
            print report_arg, " is not xml file"


