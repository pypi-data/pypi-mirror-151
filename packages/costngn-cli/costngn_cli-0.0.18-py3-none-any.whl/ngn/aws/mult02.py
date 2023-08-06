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
import boto3.session
import threading, concurrent.futures
from botocore.config import Config
import json, toml
from termcolor import colored
#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
from ngn.aws.prices00 import *
#from resource00 import *

thread_local = threading.local()

# load all regions in list regions
def available_regions(service):
    regions = []
    client = boto3.client(service,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,        
        region_name= 'us-east-2', 
    )
    response = client.describe_regions()
    for item in response["Regions"]:
        #print(item["RegionName"])
        regions.append(item["RegionName"])
    return regions


##### Access to AWS and scan all available regions and instances 
#def aws_main(some_a:str):
def aws_main(region):
    company='aws'
    #print('.',end=''); sys.stdout.flush()
    #get_res_data(region)
    #try:
    print('Region:',region)
    ec2_res = boto3.resource('ec2',            
        region_name= region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY)

    instances = ec2_res.instances.all()   
    region_has_inst=False
    global inst_ids       
    inst_ids=[]
    for instance in instances:
        region_has_inst=True
        inst_ids.append(instance.id)
        print(instance.id)
        '''
        #print('__________________________________________')
        print(colored('*','green'),end=''); sys.stdout.flush()            
        #Initiate Reg and Inst dictios
        inst=copy.deepcopy(InstBase)
        #pp.pprint(instance)
        try: #look for the name, if exists
            for tag in instance.tags:
                if 'Name'in tag['Key']:
                    ##i1.name = tag['Value']
                    inst['name']=tag['Value']
        except: pass
            
        inst['id']= instance.id
        inst['provider']=company.upper()
        inst['region']= region 
        #print(inst['id'],inst['name'],'VPC:', instance.vpc )
        inst['status']= instance.state['Name']

        # normalize datetime created
        birth_obj = instance.launch_time
        #datetime.strptime(server.created, '%Y-%m-%dT%H:%M:%SZ')        
        inst['birthday']= birth_obj.strftime(birth_format)
        #inst['birthday']=str(instance.launch_time)
        
        inst['ipv4priv']=instance.private_ip_address 
        inst['ipv4pub']= instance.public_ip_address 
        inst['type']= instance.instance_type
        inst['cpus']=instance.cpu_options.get(u'CoreCount','1')
        inst['image']=instance.image_id           
        inst['os']='Linux' if 'Linux' in instance.platform_details else 'Windows'
        
        # Get Name, Memory, avzone, vps (need client)
        ec2_cli = boto3.client('ec2',    
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name= region)              

        #r_inst = ec2_cli.describe_instances(InstanceIds=[i1.id])["Reservations"][0]
        r_inst = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]

        #r_inst=response["Reservations"][0]
        inst['avzone']=r_inst["Instances"][0]["Placement"]["AvailabilityZone"]
        inst['vpc_id']=r_inst["Instances"][0]["VpcId"]

        #Get memory size from _types
        
        r_typ =ec2_cli.describe_instance_types(InstanceTypes=[inst['type']])
        
        inst['memory']=r_typ["InstanceTypes"][0]["MemoryInfo"]["SizeInMiB"]

        #Get nominal hourly price from AWS Pricing (call prices, which is free)
        region_code = inst['region']
        instance_type = inst['type']
        operating_system = inst['os']
        
        #print('before hourly prices')
        inst['ihprice']=get_ec2_instance_hourly_price(
            AWS_ACCESS_KEY,
            AWS_SECRET_KEY,
            region_code=region_code, 
            instance_type=instance_type, 
            operating_system=operating_system,                
        )

        #print('after hourly prices') 
                    
        if inst['ihprice']is not None:
            inst['imprice']=inst['ihprice']*744
        else:            
        #if inst['ihprice']is None:
            inst['imprice']=0
            inst['ihprice']= 0
            #print('nothing')         
        
        #Store the instance id and data in lists 
        my_ids.append(inst['id'])

        rep['instances'].append(inst)
        '''

    return()

# call action function
if __name__ == "__main__":
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    global AWS_ACCESS_KEY ; global AWS_SECRET_KEY; global AWS_AUTH_REGION 
    AWS_ACCESS_KEY=''; AWS_SECRET_KEY=''; AWS_AUTH_REGION=''
    #config_file=os.path.join(Path.home(), 'costngn','config.toml')    
    prof=toml.load(config_file)
    #Load the account for the given nickname
    nick='awsmj01'     
    acc=prof[nick]
    AWS_ACCESS_KEY= acc['ACCESS_KEY']
    AWS_SECRET_KEY=acc['SECRET_KEY']
    AWS_AUTH_REGION=acc['AUTH_REGION']
    #print('')
    print("Scanning all instances (wait please)")
    #print("Next version we'll add an option for accessing only previously scanned instances")
    #regions = available_regions("ec2")   
    
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
    
    # Scan all of EC2 in each region
    cnt = 0
    my_ids=[]; insts={}


    rep=copy.deepcopy(RepBase)     
    start_time = time.time()
    #for region in regions:    
    #    aws_main(region)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(aws_main, regions)
    pp.pprint(inst_ids)
    duration = time.time() - start_time
    print(f"It took {round(duration,4)} seconds")
    #pp.pprint(rep)
    print('')
    


    """
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
    
    start_time = time.time()
    aws_main('aws', 'awsmj01', config_file)
    duration = time.time() - start_time
    print(f"It took {round(duration,4)} seconds")
    """

"""
# call region function
if __name__ == "__main__":
    global config_file
    config_file=os.path.join(Path.home(), 'costngn','.config','config.toml')
    global result_path
    result_path=os.path.join(Path.home(), 'costngn','results')
    regions=available_regions('ec2')
    pp.pprint(regions)
    
"""