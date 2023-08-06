##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\.costngn\config.toml


import os, sys
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
from termcolor import colored 
from ngn.config.classes import *

##### Acceess to DO and scan all available regions and instances 
#def do_main(nick, ce_enable:bool):
def do_main(acc,nick,tag,do_prices):    
    #print("Reading configuration file") #config.toml
    global DO_ACCESS_KEY ; global DO_SECRET_KEY; global DO_AUTH_REGION 
    DO_ACCESS_KEY=''; DO_SECRET_KEY=''; DO_AUTH_REGION=''
    DO_SECRET_KEY=acc['SECRET_KEY']
    DO_AUTH_REGION=acc['AUTH_REGION']
    #print('')
    #print("Scanning all instances (wait please)")
    if tag==None:          
        print("Scanning all instances, wait please",end=' '); sys.stdout.flush()
        tag=''
    else:
        print(f"Scanning instances with tag {colored(tag, 'yellow')}, wait please",end=' '); sys.stdout.flush()
        
    
    global company; global do_prices_g; global tag_g
    company='do'
    #url = 'https://api.digitalocean.com/v2/droplets'
    url = 'https://api.digitalocean.com/v2/droplets?tag_name='+tag

    r = requests.get(url, headers={'Authorization':'Bearer %s' % DO_SECRET_KEY})
    droplets = r.json()
    droplet_list = []
    #for i in range(len(droplets['droplets'])):
    #    droplet_list.append(droplets['droplets'][i])
    rep=copy.deepcopy(RepBase)             

    for droplet in droplets['droplets']:
        #pp.pprint(droplet)
        print(colored('.','green'),end=''); sys.stdout.flush()
        inst=copy.deepcopy(InstBase)
        #print(droplet["tags"])        
        #Convert tag list to dict
        for tag in droplet["tags"]:
            #print(tag)
            inst['tags'][tag]=tag
   
        
        inst['id']=str(droplet['id'])

        inst['provider']=company.upper()
        region= droplet['region']['name']
        inst['region']=region
        inst['name']= droplet['name']
        #inst['name']= droplet['tags']
        inst['status']= droplet['status']
        # normalize datetime created
        birth_obj = datetime.strptime(droplet['created_at'], '%Y-%m-%dT%H:%M:%SZ')        
        inst['birthday']= birth_obj.strftime(birth_format)
        inst['memory']= droplet['memory']
        inst['image']= droplet['image']['id']
        inst['os']= droplet['image']['distribution']
        inst['type']= droplet['size']['description']
        inst['cpus']= droplet['vcpus']
        inst['vpc_id']= droplet['vpc_uuid']
        inst['ihprice']= droplet['size']['price_hourly']
        inst['imprice']= droplet['size']['price_monthly']
        inst['avzone']='Multiple'
        for network in droplet['networks']['v4']:
            if network['type']=='private':
                inst['ipv4priv']=network['ip_address']
            elif network['type']=='public':
                inst['ipv4pub']=network['ip_address']

        rep['instances'].append(inst)

        #droplet_list.append(droplets['droplets'][i])
        #pp.pprint(inst)
        #pp.pprint(inst['tags'])
        #print('____________________')
    #rep['month_cost']=round(rep['month_cost'],2)
    #pp.pprint(rep)

    return(rep)
 

        
        
  
   
    #return droplet_list
    #pp.pprint(droplet_list)

    #print(droplet_list[0]['id'])




'''
# call function
if __name__ == "__main__":
    aws_main()
'''