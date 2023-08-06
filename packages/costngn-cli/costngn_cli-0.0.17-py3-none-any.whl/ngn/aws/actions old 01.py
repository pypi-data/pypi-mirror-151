##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\costngn\config.toml

import os, sys, time
from os.path import exists
from pathlib import Path
from itertools import count
from datetime import date, datetime
import copy
import pprint as pp
import boto3
import json
import toml
from botocore.config import Config
from termcolor import colored
#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
from ngn.aws.prices00 import *
#from resource00 import *

##### Access to AWS and scan all available regions and instances 
#def aws_main(some_a:str):
def aws_act_main(company, nick, config_file):
    global AWS_ACCESS_KEY ; global AWS_SECRET_KEY; global AWS_AUTH_REGION 
    AWS_ACCESS_KEY=''; AWS_SECRET_KEY=''; AWS_AUTH_REGION=''
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Load the account for the given nickname    
    acc=prof[nick]
    AWS_ACCESS_KEY= acc['ACCESS_KEY']
    AWS_SECRET_KEY=acc['SECRET_KEY']
    AWS_AUTH_REGION=acc['AUTH_REGION']
    #print('')
    #regions=available_regions()   
    # pp.pprint(regions)
    regions=[
        'eu-north-1',
        'ap-south-1',
        'eu-west-3',
        'eu-west-2',
        'eu-west-1',
        'ap-northeast-3',
        'ap-northeast-2',
        'ap-northeast-1',
        'sa-east-1',
        'ca-central-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'eu-central-1',
        'us-east-1',
        'us-east-2',
        'us-west-1',
        'us-west-2']

    cnt = 0
    """
    my_insts=[]
    # Get Name, Memory, avzone, vps (need client)
    #region= 'us-east-1'

    
    ec2_cli = boto3.client('ec2',    
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name= region)  
    ec2_res = boto3.resource('ec2',     
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name= region)
    """           

    #r_inst = ec2_cli.describe_instances(InstanceIds=[i1.id])["Reservations"][0]
    #re_inst = ec2_cli.describe_instances(InstanceIds=inst_ids)["Reservations"][0]
    #re_inst = ec2_cli.describe_instances(InstanceIds=['i-0a8e5f7096eaf3c7e'])["Reservations"][0]
    
    
    #pp.pprint(re_inst) 
 
    rep=copy.deepcopy(RepBase)
    print('_______ BEFORE ACTION ________')
    for my_inst in my_insts:        
        id=my_inst[0]
        region= my_inst[1]
        ec2_res = boto3.resource('ec2',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY, 
        region_name= region)
        inst = ec2_res.Instance(id)
        print(region,id,inst.state['Name'])
                
        #pp.pprint(inst.tags)
        #pp.pprint(dir(inst))
        #print(inst.state['Name'])
        #ec2_res.instances.filter(InstanceIds=[id]).start();print('ACTION--> START')
        ec2_res.instances.filter(InstanceIds=[id]).stop();print('ACTION--> STOP')
        print()
        

    print('_______ AFTER ACTION ________')
    tw=15; print('wait',tw,'seconds'); time.sleep(tw)

    
    for my_inst in my_insts:        
        id=my_inst[0]
        region= my_inst[1]
        ec2_res = boto3.resource('ec2',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY, 
        region_name= region)        
        inst = ec2_res.Instance(id)
        print(region,id,inst.state['Name'],'\n')
        print()



        #print(inst.state['Name'])


    """   
    for region in regions:
        print('.',end=''); sys.stdout.flush()
        #get_res_data(region)
        #try:
        #print('Region:',region)

    
        instances = ec2_res.instances.all()   
        region_has_inst=False      
        
        for instance in instances:
            my_inst=[instance.id,region,instance.tags]
            my_insts.append(my_inst)
            region_has_inst=True
            print('__________________________________________')
            print(colored('*','green'),end=''); sys.stdout.flush()            
            #Initiate Reg and Inst dictios
            inst=copy.deepcopy(InstBase)
            #print(instance.id)
            print('TAGS:')
            #pp.pprint(instance.tags)
            try: #look for the name, if exists
                for tag in instance.tags:
                    if 'Name'in tag['Key']:
                        ##i1.name = tag['Value']
                        inst['name']=tag['Value']
            except: pass
            """    
    #pp.pprint(my_insts)        
    return()
            





# call action function
if __name__ == "__main__":
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    global inst_ids
    inst_ids=[
        'i-0fd5af3e4a8d9ded0',
        'i-0fd5af3e4a8d9ded0',
        'i-0a8e5f7096eaf3c7e',
        'i-003aadd72635ae8ee',
        'i-08c70bd78035e81fb'        
        ]
    global my_insts
    my_insts=[
        ['i-0fd5af3e4a8d9ded0',
        'eu-west-1',
        [{'Key': 'env', 'Value': 'test'},
        {'Key': 'Name', 'Value': 'costngn-test-euwest1'},
        {'Key': 'purpose', 'Value': 'costngn'}]],
        ['i-056bac4d88febe5c0',
        'ap-southeast-2',
        [{'Key': 'Instance-ID', 'Value': 'i-056bac4d88febe5c0'},
        {'Key': 'Name', 'Value': 'costngn-test-apsoutheast2'},
        {'Key': 'purpose', 'Value': 'costngn'},
        {'Key': 'env', 'Value': 'dev'}]],
        ['i-0a8e5f7096eaf3c7e',
        'us-east-1',
        [{'Key': 'purpose', 'Value': 'costngn'},
        {'Key': 'Name', 'Value': 'costngn-test-useast1'},
        {'Key': 'env', 'Value': 'prod'},
        {'Key': 'Instance-ID', 'Value': 'i-0a8e5f7096eaf3c7e'}]],
        ['i-003aadd72635ae8ee',
        'us-east-2',
        [{'Key': 'env', 'Value': 'prod'},
        {'Key': 'purpose', 'Value': 'costngn'},
        {'Key': 'Name', 'Value': 'costngn-test-useast2'}]],
        ['i-08c70bd78035e81fb',
        'us-west-2',
        [{'Key': 'env', 'Value': 'dev'},
        {'Key': 'Instance-ID', 'Value': 'i-08c70bd78035e81fb'},
        {'Key': 'Name', 'Value': 'costngn-test-uswest2'},
        {'Key': 'purpose', 'Value': 'costngn'}]]]

    aws_act_main('aws', 'awsmj01', config_file)
"""

# call region function
if __name__ == "__main__":
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    regions=available_regions()
    pp.pprint(regions)
    
"""