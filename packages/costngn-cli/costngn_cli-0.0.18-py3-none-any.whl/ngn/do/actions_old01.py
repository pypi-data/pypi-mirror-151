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


##### Acceess to DO and scan all available regions and instances 
#def do_main(nick, ce_enable:bool):
def do_action(acc,rep,action): 

    #print("Reading configuration file") #config.toml
    global DO_ACCESS_KEY ; global DO_SECRET_KEY; global DO_AUTH_REGION 
    DO_ACCESS_KEY=''; DO_SECRET_KEY=''; DO_AUTH_REGION=''
    DO_SECRET_KEY=acc['SECRET_KEY']
    DO_AUTH_REGION=acc['AUTH_REGION']
    print('')
    print("ACTIONS")
    
    headers={'Authorization':'Bearer %s' % DO_SECRET_KEY}
    """
    #GET DROPLETS DATA
    url = 'https://api.digitalocean.com/v2/droplets'
    #r = requests.get(url, headers={'Authorization':'Bearer %s' % DO_SECRET_KEY})
    response = requests.get(url, headers=headers).json()
    #response = r.json()
    
    droplet_ids = []
    #pp.pprint(droplets)
    #pp.pprint(rep)
    for droplet in response['droplets']:
        #pp.pprint(droplet)        

        print(droplet['id'])
        droplet_ids.append(droplet['id'])

    
    #GET ACTIONS HISTORY

    #url='https://api.digitalocean.com/v2/actions?page=1&per_page=1'
    url='https://api.digitalocean.com/v2/actions?'
    # = requests.get(url, headers=headers)
    response = requests.get(url, headers=headers).json()
    #pp.pprint(response)
    for action in response['actions']:
        #pp.pprint(action)  
        print(action['type'],action['completed_at'])
    return()
      
    # EXECUTE ACTION
    id= '143913689'
    id= '299692275'
    url = 'https://api.digitalocean.com/v2/droplets/143913689/actions'
    json_body={"type": "power_on"} 
    #json_body={"type": "shutdown"}
    
        # = requests.get(url, headers=headers)
    response = requests.post(url, headers=headers, json=json_body).json()
    #pp.pprint(response)
    
    print(response['action']['status'])
 


    #print(droplet_list[0]['id'])

    
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
"""
# call function
if __name__ == "__main__":
    do_action()
    
"""