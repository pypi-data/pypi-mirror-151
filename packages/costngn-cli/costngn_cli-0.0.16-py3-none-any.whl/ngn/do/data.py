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
def do_main(company, nick,config_file,result_path):    
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
    #for i in range(len(droplets['droplets'])):
    #    droplet_list.append(droplets['droplets'][i])
    rep=copy.deepcopy(RepBase)             

    for droplet in droplets['droplets']:
        #pp.pprint(droplet)
   
        inst=copy.deepcopy(InstBase)
        inst['id']=droplet['id']
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
        """
        #hours elapsed since creation date
        #print(inst['birthday'])
        birth_obj = datetime.strptime(inst['birthday'], birth_format)
        period= (datetime.now()-birth_obj).total_seconds()//3600
        inst['life_cost']= round(period *float(inst['ihprice']),2)
        #hours elapsed on current month
        #period_start=date.today().replace(day=1)
        month_first_day=date.today().replace(day=1)
        zero_hour=datetime.min.time()
        period_start= datetime.combine(month_first_day,zero_hour)
        print(period_start)        
        if period_start<=birth_obj:period_start=birth_obj
        #period_end=date.today()
        period= (datetime.now()-period_start).total_seconds()//3600      
        #period = (period_end - period_start).days * 24 + datetime.now().hour 

        inst['month_cost']= round(period *float(inst['ihprice']),2)  
        rep['month_cost']+= inst['month_cost']
        rep['life_cost']+= inst['life_cost']
        """

        inst['avzone']='Multiple'
        for network in droplet['networks']['v4']:
            if network['type']=='private':
                inst['ipv4priv']=network['ip_address']
            elif network['type']=='public':
                inst['ipv4pub']=network['ip_address']

        rep['instances'].append(inst)

        #droplet_list.append(droplets['droplets'][i])
        #pp.pprint(inst)
        #print('____________________')
    #rep['month_cost']=round(rep['month_cost'],2)
    #pp.pprint(rep)

    return(rep)
 

        
        
  
   
    #return droplet_list
    #pp.pprint(droplet_list)

    #print(droplet_list[0]['id'])



    """
    

    #print('Soon it will be added an option to display detailed actual costs from cost explorer')
    print('Unordered unformatted dictionary output by now')

    pp.pprint(aws_rep)#just to see how it works, format will be improved later
    print('______________________________________________________________')
    if len(my_ids) == 1:
        print(f"You have {len(my_ids)} instance here M.J!",'\n')
    elif len(my_ids) > 1:
        print(f"You have {len(my_ids)} instances here M.J.!",'\n')
    else:
        print(f"You have no instances here M.J.!",'\n')    
    
    
    #Generate report json file
    aws_json = json.dumps(aws_rep,indent=2)
    with open('report01.json', 'w') as outfile:
        outfile.write(aws_json)
    
    print('Saved to report01.json in current folder, good bye!')
    """

'''
# call function
if __name__ == "__main__":
    aws_main()
'''