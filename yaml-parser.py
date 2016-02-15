#!/usr/bin/python
import yaml
import sys
from sqlalchemy import create_engine, Table, MetaData, orm, Integer, ForeignKey, Column, String, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from termcolor import colored
from datetime import datetime

# db credentials
db_user = 'root'
db_pass = '123'
db_host = '192.168.27.10'
db_name = 'hcl_test'

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

fd = open(sys.argv[1])
server_info = yaml.load(fd)
fd.close()

print server_info['server']['name']
print server_info['server']['vendor']
for hw in server_info['components']:
    print hw['name']
    print hw['vendor']
    print hw['type']
    print hw['driver']['name']
    print hw['driver']['version']

for cert in server_info['certification']:
    print cert['date']
    print cert['fuel_version']
    print cert['status']
