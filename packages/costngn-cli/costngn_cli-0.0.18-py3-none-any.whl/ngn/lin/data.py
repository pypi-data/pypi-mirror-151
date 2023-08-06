from ipaddress import ip_address
import os, sys
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
from pytz import HOUR
import copy
import pprint as pp
from termcolor import colored
from linode_api4 import LinodeClient
from ngn.config.classes import *
from ngn.config.base_dict import *

def lin_main(acc,nick,tag,do_prices):
    global LIN_SECRET_KEY  
    #Load the account for the given nickname    
    LIN_SECRET_KEY=acc['SECRET_KEY']    
    if tag==None:          
        print("Scanning all instances, wait please",end=' '); sys.stdout.flush()
        #tag=''
    else:
        print(f"Scanning instances with tag {colored(tag, 'yellow')}, wait please",end=' '); sys.stdout.flush()
        
    

    global company; global do_prices_g; global tag_g
    company='lin'

    client = LinodeClient(LIN_SECRET_KEY)
    linodes = client.linode.instances()
    types = client.linode.types()   

    rep=copy.deepcopy(RepBase)
    
    for linode in linodes:                
        inst=copy.deepcopy(InstBase)        
        ld=linode.__dict__

        if tag is None:                
            print(colored('.','green'),end=''); sys.stdout.flush()
        elif tag in ld["tags"]:
            #print('is', tag, ld["tags"])
            print(colored('.','green'),end=''); sys.stdout.flush()
        else:
            print(colored('.','red'),end=''); sys.stdout.flush()
            continue

        #Convert tag list to dict
        for tag_aux in ld["tags"]:            
            inst['tags'][tag_aux]=tag_aux

        for atype in types.__dict__['lists'][0]:
            #pp.pprint(atype)
            if str(atype)== str(linode.type):
                #pp.pprint(atype.__dict__)
                type_obj=atype.__dict__ 
                break        

        inst['id']=str(ld['id'])           
        inst['provider']=company.upper()
        inst['region']=linode.region.__dict__['id']         
        inst['name']= linode.label
        inst['status']= linode.status        
        for ip_add in linode.ipv4:            
            ip= ip_address(ip_add)
        #    print(ip, ip.is_private,ip.is_global)
            if ip.is_private: inst['ipv4priv']=ip_add
            elif ip.is_global: inst['ipv4pub']=ip_add

        # normalize datetime created
        birth_obj = linode.created
        #datetime.strptime(server.created, '%Y-%m-%dT%H:%M:%SZ')        
        inst['birthday']= birth_obj.strftime(birth_format)        
        #inst['birthday']= str(linode.created)
        inst['memory']= linode.specs.memory
        inst['image']= linode.image.__dict__['id']
        inst['os']= inst['image'].replace('linode/','')
        #inst['type']= atype.__dict__['id'] #linode.type has payload
        inst['type']=linode.type.__dict__['id']
        inst['cpus']= linode.specs.vcpus
        #inst['vpc_id']= server.datacenter.name        
        inst['ihprice']= type_obj['_raw_json']['price']['hourly']
        inst['imprice']= type_obj['_raw_json']['price']['monthly']

        """
        # Estimated cost based on hours elapsed on current month
        period_start=date.today().replace(day=1)
        period_end=date.today()        
        period = (period_end - period_start).days * 24 + datetime.now().hour 
        inst['month_cost']= round(period *float(inst['ihprice']),5)
        inst['month_cost']=min(inst['month_cost'],inst['imprice']) #because max cost is monthly value
        rep['month_cost']+= inst['month_cost']  
        """
        rep['instances'].append(inst)
        
        #pp.pprint(inst)

             
        # TRIAL ZONE
        #pp.pprint(types.__dict__)
        #for data in types:
        #    pp.pprint(data)
        #pp.pprint((types.__dict__['lists'][0]  ))
        #pp.pprint(dir(types.__dict__['lists'][0].__getitem__('Type: g6-nanode-1')  ))
        #print('INDEX',types.__dict__['lists'][0].index(linode.type))
     
        #pp.pprint((types[0].__dict__['_raw_json']['price']['hourly'] ))
        #print((types[0].__dict__['_raw_json']['price']['monthly'] ))
        
        #for item in vars(types[0]):
        #    pp.pprint((item.label))

        #pp.pprint(json.loads(linode)) # not for instance
        #pp.pprint('specs',vars(linode.specs))

        #pp.pprint(linode.ipv4)
        #for ip_add in linode.ipv4:            
        #    ip= ip_address(ip_add)
        #    print(ip, ip.is_private,ip.is_global)


        #pp.pprint((linode.__dict__)) #this converts the instance in a dict
        #pp.pprint(vars(linode))
        #pp.pprint((linode.region.__dict__['id']))
        #pp.pprint((ld.region))
        #pp.pprint((linode.type.__dict__))
        #pp.pprint((linode.type.__getattribute__))
        
        #pp.pprint(json.dumps(linode.properties)) #no serializable
    #rep['month_cost']=round(rep['month_cost'],5)
    #pp.pprint(rep)
    print()
    return(rep)
    

