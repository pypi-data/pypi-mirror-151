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
from botocore.config import Config

#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
#from ngn.aws.prices00 import *
#from resource00 import *


##### Acceess to DO and scan all available regions and instances 
#def do_main(nick, ce_enable:bool):
def do_act_main(company, nick,config_file,result_path):    
    #print("Reading configuration file") #config.toml
    global DO_ACCESS_KEY ; global DO_SECRET_KEY; global DO_AUTH_REGION 
    DO_ACCESS_KEY=''; DO_SECRET_KEY=''; DO_AUTH_REGION=''
    prof=toml.load(config_file)
    #Load the account for the given nickname    
    acc=prof[nick]   
    #print(f"Account Nickname: {nick}")
    #print(f"Service Provider: {acc['provider'].upper()}")
    #print(f"Data Output Format: {acc['out_format']}")
    #print(f"Secret Key: XXX HIDDEN XXX") 
    #print(f"Secret Key: {acc['SECRET_KEY']}")
    DO_SECRET_KEY=acc['SECRET_KEY']
    DO_AUTH_REGION=acc['AUTH_REGION']
    #print('')
    print("Scanning all instances (wait please)")
    url = 'https://api.digitalocean.com/v2/droplets'
    r = requests.get(url, headers={'Authorization':'Bearer %s' % DO_SECRET_KEY})
    droplets = r.json()
    droplet_list = []

    
    

    return()
 

        
        
  
   
    #return droplet_list
    #pp.pprint(droplet_list)

    #print(droplet_list[0]['id'])



    


# call function
if __name__ == "__main__":
    do_act_main()
