import os, sys
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
from termcolor import colored


def het_main(acc, nick,tag,do_prices):    
    #print("Reading configuration file") #config.toml
    global HET_ACCESS_KEY ; global HET_SECRET_KEY; global HET_AUTH_REGION 
    HET_ACCESS_KEY=''; HET_SECRET_KEY=''; HET_AUTH_REGION=''
    company='het'

    if tag==None:          
        print("Scanning all instances, wait please",end=' '); sys.stdout.flush()
        #tag=''
    else:
        print(f"Scanning instances with tag {colored(tag, 'yellow')}, wait please",end=' '); sys.stdout.flush()
    

    HET_SECRET_KEY=acc['SECRET_KEY']
    client = Client( token=HET_SECRET_KEY)  
    #servers = client.servers.get_all(label_selector='=prod')
    servers = client.servers.get_all()
    #print(servers)
    rep=copy.deepcopy(RepBase)
    for server in servers:
        if tag is None:                
            print(colored('.','green'),end=''); sys.stdout.flush()
        elif tag in server.labels.values():
            print(colored('.','green'),end=''); sys.stdout.flush()
        else:
            print(colored('.','red'),end=''); sys.stdout.flush()
            continue
        
        inst=copy.deepcopy(InstBase)
        inst['id']=str(server.id)        
        inst['provider']=company.upper()

        inst['region']=server.datacenter.location.network_zone
        inst['name']= server.name
        inst['tags']= server.labels
        #inst['name']= droplet['tags']
        inst['status']= server.status
        inst['ipv4pub']= server.public_net.ipv4.ip
        for i,item in enumerate(server.private_net):
            inst['ipv4priv']=item.ip   

        # normalize datetime created
        birth_obj = server.created
        #datetime.strptime(server.created, '%Y-%m-%dT%H:%M:%SZ')        
        inst['birthday']= birth_obj.strftime(birth_format)

        inst['memory']= server.server_type.data_model.memory
        inst['image']= server.image.id
        #inst['os']= server.image.os_flavor
        inst['os']= server.image.name
        inst['type']= server.image.type
        inst['cpus']=server.server_type.data_model.cores
        inst['vpc_id']= server.datacenter.name
        inst['ihprice']= round(float(server.server_type.prices[0]['price_hourly']['net']),5)
        inst['imprice']= round(float(server.server_type.prices[0]['price_monthly']['net']),5)

        #print(server.data_model)
        #print(dir(server.server_type.data_model))
        #print(server._client)
        
        #pp.pprint(dir(server))
        #pp.pprint(dir(server.data_model))
        #print(server.__dict__)
        #print(server._client.__dict__) 
               
        """
        #days elapsed on current month as period
        period_start=date.today().replace(day=1)
        period_end=date.today()        
        period = (period_end - period_start).days * 24 + datetime.now().hour 
        inst['month_cost']= round(period *float(inst['ihprice']),5)        
        rep['month_cost']+= inst['month_cost'] 
        """
        rep['instances'].append(inst)
        
        #pp.pprint(inst)
             
        # TRIAL ZONE
        #pp.pprint(dir(server.server_type.data_model))
        #print(server.server_type.id)
        #print(server.server_type.id_or_name)
        #print(server.server_type.name)
        #pp.pprint(vars(server.data_model))
        #print(server.server_type.prices[0]['price_hourly']['net'])
        #print(json.dumps(server.server_type.prices))
    #rep['month_cost']=round(rep['month_cost'],5)
    print()
    return(rep)


