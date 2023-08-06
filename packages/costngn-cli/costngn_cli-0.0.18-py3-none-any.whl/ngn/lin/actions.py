##### STARt, STOP, REBOOT ACTIONS #####


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

def lin_action(acc,rep,action): 
    #if tag is None: tag=''
    LIN_SECRET_KEY=acc['SECRET_KEY']    
    act_dict={
        'start':    'boot',
        'stop':     'shutdown',
        #'poweroff': 'power_off',
        'reboot':   'reboot',
        #'powercycle':   'power_cycle',
    }


    
    headers={'Authorization':'Bearer %s' % LIN_SECRET_KEY}

    #
    # EXECUTE ACTION
    #url = 'https://api.linode.com/v4/linode/instances/36195734/shutdown'###########
    #url = 'https://api.linode.com/v4/linode/instances'
    #json_body={"type": act_dict[action]}
    #a_r = requests.post(url, headers=headers) #########
    #a_r = requests.get(url, headers=headers)
    #pp.pprint(a_r.__dict__)
   
    #response = requests.post(url, headers=headers, json=json_body).json()
    #pp.pprint(response)    
    #print(response['action']['status'])

    for inst in rep['instances']:
        id=inst['id']; region= inst['region']; status=inst['status']
        header= 'Instance: '+id+' - Region: '+region+' - Status before action: '+status.upper()
        print('_' * len(header)); print(header)
        print(f'ACTION--> {action.upper()}')


        #pp.pprint(a_r.json())    
        #print(a_r['action']['status'])
        try:
            url = 'https://api.linode.com/v4/linode/instances/'+id+'/'+act_dict[action]
            a_r = requests.post(url, headers=headers)

            url = 'https://api.linode.com/v4/linode/instances/'+id
            a_r = requests.get(url, headers=headers).json()
            status=a_r['status'].replace('_',' ').upper()
            #status=status.replace('_',' ')
            #status=' '.join(filter(str.isalnum, status))
            #pp.pprint(a_r['_content'])
            print(f"Status after action: {status.upper()}")
        except Exception as e:
            print(e)

        
        
