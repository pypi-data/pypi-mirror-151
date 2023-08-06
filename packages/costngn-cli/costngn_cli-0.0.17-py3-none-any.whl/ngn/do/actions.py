##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\.costngn\config.toml


import os
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
from pytz import HOUR
import requests
import copy
import pprint as pp
import json
import toml
#from botocore.config import Config

#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
#from ngn.aws.prices00 import *
#from resource00 import *


##### START - STOP - REBOOT

def do_action(acc,rep,tag,action): 
    if tag is None: tag=''
    #print("Reading configuration file") #config.toml
    global DO_ACCESS_KEY ; global DO_SECRET_KEY; global DO_AUTH_REGION 
    DO_ACCESS_KEY=''; DO_SECRET_KEY=''; DO_AUTH_REGION=''
    DO_SECRET_KEY=acc['SECRET_KEY']
    DO_AUTH_REGION=acc['AUTH_REGION']
    act_dict={
        'start':    'power_on',
        'stop':     'shutdown',
        'poweroff': 'power_off',
        'reboot':   'reboot',
        'powercycle':   'power_cycle',
    }

    print('')
    print("ACTIONS")
    
    headers={'Authorization':'Bearer %s' % DO_SECRET_KEY}

 
    """
    # EXECUTE ACTION
    id= '143913689'
    #id= '299692275'
    url = 'https://api.digitalocean.com/v2/droplets/143913689/actions'
    #json_body={"type": "power_on"} 
    #json_body={"type": "shutdown"}
    json_body={"type": "power_off"}
    
    response = requests.post(url, headers=headers, json=json_body).json()
    #pp.pprint(response)
    
    print(response['action']['status'])
    #Get Droplet
    url = 'https://api.digitalocean.com/v2/droplets/'+id
    droplet = requests.get(url, headers=headers).json()['droplet']
    pp.pprint(droplet)

        
    # CREATE TAG
    url = 'https://api.digitalocean.com/v2/tags'
    #url = 'https://api.digitalocean.com/v2/tags/ENV/resources'
    json_body={"name": "test"}

    #response = requests.get(url, headers=headers).json()
    response = requests.post(url, headers=headers, json=json_body).json()
    pp.pprint(response)
    
    # TAG DROPLET
    url = 'https://api.digitalocean.com/v2/tags/env/resources'
    #url = 'https://api.digitalocean.com/v2/tags/ENV/resources'
    json_body={"resources":[{"resource_id":"299692275","resource_type":"droplet"}]}

    #response = requests.get(url, headers=headers).json()
    #response = requests.post(url, headers=headers, json=json_body).json()
    response = requests.post(url, headers=headers, json=json_body)
    pp.pprint(response) 
    """

    
    # EXECUTE ACTION
    #url = 'https://api.digitalocean.com/v2/droplets/143913689/actions'
    #url = 'https://api.digitalocean.com/v2/droplets/actions?tag_name='+tag
    json_body={"type": act_dict[action]}

   
    #response = requests.post(url, headers=headers, json=json_body).json()
    #pp.pprint(response)    
    #print(response['action']['status'])
    
    for inst in rep['instances']:
        id=inst['id']; region= inst['region']; status=inst['status']
        header= 'Instance: '+id+' - Region: '+region+' - Status before action: '+status.upper()
        print('_' * len(header)); print(header)
        print(f'ACTION--> {action.upper()}')
        url = 'https://api.digitalocean.com/v2/droplets/'+id+'/actions'
        a_r = requests.post(url, headers=headers, json=json_body).json()
        #pp.pprint(a_r)    
        #print(a_r['action']['status'])
        try:
            print(f"Status after action: {a_r['action']['status'].upper()}")
        except:
            print(a_r)
        
        """
        url = 'https://api.digitalocean.com/v2/droplets/'+id
        droplet = requests.get(url, headers=headers).json()['droplet']
        #pp.pprint(droplet)
        
        for network in droplet['networks']['v4']:
            if network['type']=='public':
                ipv4=network['ip_address']
        #print(f"Status after action: {a_r['action']['status'].upper()}", end='')
        print(f"Status after action: {droplet['status'].upper()}", end='')
        #print(' with IPV4 public address',i_d.get("PublicIpAddress",'not assigned'))
        print(' with IPV4 public address',ipv4)
        """
        print()
        

"""
# call function
if __name__ == "__main__":
    do_action()
    
"""