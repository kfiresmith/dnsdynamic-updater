#!/usr/bin/python3

import os
import requests
import configparser


# in-script variables
myipobj = requests.get(ip_provider)
my_ip = myipobj.text
update_required = False


os.chdir("/")
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'etc', 'dnsdynamic-updater', 'dnsdynamic-updater.conf'))

#configparser bits here
dyn_account = config['main']['dyn_account']
dyn_passwd = config['main']['dyn_passwd']
dyn_hostname = config['main']['dyn_hostname']
ip_provider = config['main']['ip_provider']
api_update_string = config['main']['api_update_string']
debug_enabled = config['main'].getboolean('debug_enabled')
last_known_ip = config['state']['last_known_ip']


myipobj = requests.get(ip_provider)
my_ip = myipobj.text

def check_update():
    global update_required
    if my_ip != last_known_ip:
        update_required = True

def update_ddns():
    post_string = 'https://' + dyn_account + ':' + dyn_passwd + api_update_string + dyn_hostname + '&myip=' + my_ip
    requests.post(post_string)
    if debug_enabled:
        print(post_string)
    

    
check_update()
if update_required:
    update_ddns()

