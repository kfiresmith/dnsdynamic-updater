#!/usr/bin/python3
#
# A simple python script to keep DnsDynamic.net entries fresh.
#
# Kodiak Firesmith <kfiresmith@gmail.com>
#  Released to the world without license, do what you will.
# 
#  Bugs / To-do:  
#    - Write the state back to the conf file
#    - Allow for many subdomains rather than just the 1

import configparser
import os
import os.path
import requests
import socket
import sys
"""
Read in config file (/etc/dnsdynamic-updater/dnsdynamic-updater.conf), check current external IP, and if necessary, update
 the current one.
"""
os.chdir("/")
config = configparser.ConfigParser()
conf_abs_path = "/etc/dnsdynamic-updater/dnsdynamic-updater.conf"

if os.path.exists(conf_abs_path) is False:
    print("dnsdynamic-updater.conf file appears to be missing.")
    sys.exit(2)

config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'etc', 'dnsdynamic-updater', 'dnsdynamic-updater.conf'))

dyn_account = config['main']['dyn_account']
dyn_passwd = config['main']['dyn_passwd']
dyn_hostname = config['main']['dyn_hostname']
ip_provider = config['main']['ip_provider']
api_update_string = config['main']['api_update_string']
debug_enabled = config['main'].getboolean('debug_enabled')
last_known_ip = config['state']['last_known_ip']

myipobj = requests.get(ip_provider)
my_ip = myipobj.text
my_record = socket.gethostbyname(dyn_hostname)


def check_update():
    global update_required
    if my_ip != my_record:
        update_required = True
        if debug_enabled:
            print('Update is required; our current IP is ' + str(my_ip) + ', and our record currently lists ' + str(my_record))

def update_ddns():
    post_string = 'https://' + dyn_account + ':' + dyn_passwd + api_update_string + dyn_hostname + '&myip=' + my_ip
    requests.post(post_string)
    if debug_enabled:
        print(post_string)
    
update_required = False

check_update()
if update_required:
    update_ddns()


