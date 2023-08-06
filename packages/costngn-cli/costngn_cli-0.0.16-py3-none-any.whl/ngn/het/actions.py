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


def het_act_main(company, nick,config_file,result_path):    
    #print("Reading configuration file") #config.toml
    global HET_ACCESS_KEY ; global HET_SECRET_KEY; global HET_AUTH_REGION 
    HET_ACCESS_KEY=''; HET_SECRET_KEY=''; HET_AUTH_REGION=''
    prof=toml.load(config_file)
    #Load the account for the given nickname    
    acc=prof[nick]   
    #print(f"Account Nickname: {nick}")
    #print(f"Service Provider: {acc['provider'].upper()}")
    #print(f"Data Output Format: {acc['out_format']}")
    LIN_SECRET_KEY=acc['SECRET_KEY']
    print("Scanning all instances (wait please)")
    client = Client( token=LIN_SECRET_KEY)  
    servers = client.servers.get_all()
    #print(servers)
    id_list=[]

    for server in servers:
        print('______________')
        print(server.id)
        id_list.append(server.id)
        print(server.status)

    #url = 'https://api.hetzner.cloud/v1'
    url='https://api.hetzner.cloud/v1/servers'

    r = requests.get(url, headers={'Authorization':'Bearer %s' % HET_SECRET_KEY})
    #droplets = r.json()
    pp.pprint(r)

    return()

# call function
if __name__ == "__main__":
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    het_act_main('het','pehet01',config_file,result_path)
