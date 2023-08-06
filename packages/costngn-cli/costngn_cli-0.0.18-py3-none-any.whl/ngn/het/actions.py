import requests
import os
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
from pytz import HOUR
import copy
import pprint as pp
import json
import toml
from hcloud import Client
#from hcloud.images.domain import Image
#from hcloud.server_types.domain import ServerType
from ngn.config.classes import *

def het_action(acc,rep,action):    
    HET_SECRET_KEY=acc['SECRET_KEY']
    client = Client( token=HET_SECRET_KEY) 

    act_dict={        
        'start':    client.servers.power_on,
        'stop':     client.servers.shutdown,
        'poweroff': client.servers.power_off,
        'reboot':   client.servers.reboot,
        'powercycle':   client.servers.reset,
    }
 
    #servers = client.servers.get_all(label_selector='=prod')
    #server=act_dict['pru']()
    #pp.pprint(server)
    #print(server.id)
    
    for inst in rep['instances']:
        id=inst['id']; region= inst['region']; status=inst['status']
        header= 'Instance: '+id+' - Region: '+region+' - Status before action: '+status.upper()
        print('_' * len(header)); print(header)
        print(f'ACTION--> {action.upper()}')
        server= client.servers.get_by_id(id)
        #client.servers.shutdown(server)
        try:
            act_dict[action](server)
        except Exception as e:
            print(e)
        #server=act_dict['pru']()
        print(f"Status after action: {server.status.upper()}")
    