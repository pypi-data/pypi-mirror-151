##### Logs-in and extract all instances data grouped by regions #####
#it needs config file $home\costngn\config.toml

import os, sys, time
#from os.path import exists
#from pathlib import Path
#from itertools import count
#from datetime import date, datetime
import copy
#import pprint as pp
import boto3
#import json
#import toml
from botocore.config import Config
from botocore.exceptions import ClientError
from termcolor import colored
#from ngn.aws.cred01 import * #now from config.toml
from ngn.config.classes import *
from ngn.aws.prices00 import *


##### Perform START, STOP or REBOOT actions over instances
def aws_action(acc,rep,action):
    global AWS_ACCESS_KEY ; global AWS_SECRET_KEY; global AWS_AUTH_REGION
    AWS_ACCESS_KEY= acc['ACCESS_KEY']
    AWS_SECRET_KEY=acc['SECRET_KEY']
    AWS_AUTH_REGION=acc['AUTH_REGION']
    #print('Action to do -->', action.upper())
    
    for inst in rep['instances']:
        id=inst['id']
        region= inst['region']        
        #ec2_res = boto3.resource('ec2',
        ec2_cli = boto3.client('ec2',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY, 
            region_name= region)
        
        i_d = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]
        status=i_d["Instances"][0]["State"]["Name"]

        header= 'Instance: '+id+' - Region: '+region+' - Status before action: '+status.upper()
        #sep_line= '_' * len(header)
        print('_' * len(header))      
        print(header)


        #print('Instance:',id,'- Region:', region, '- Status before action:',status.upper())
        
        #inst = ec2_res.Instance(id)
        #inst = ec2_cli.Instance(id)
        #print(region,id,inst.state['Name'])                
        #pp.pprint(inst.tags)
        #pp.pprint(dir(inst))
        #print(inst.state['Name'])
        #ec2_res.instances.filter(InstanceIds=[id]).start();print('ACTION--> START')
        #ec2_res.instances.filter(InstanceIds=[id]).stop();print('ACTION--> STOP')
        print(f'ACTION--> {action.upper()}')
        if action=='start': ############ START ###############
            # Do a dryrun first to verify permissions            
            try:
                ec2_cli.start_instances(InstanceIds=[id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise 
            # Dry run succeeded, run without dryrun
            try:
                response = ec2_cli.start_instances(InstanceIds=[id], DryRun=False)
                #response=response['StartingInstances'][0]['CurrentState']['Name']
                #print(f'Status after action: {response.upper()}')
                #i_d = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]["Instances"][0]
                #print(f'Status after action: {i_d["State"]["Name"].upper()}', end='')
                #print(' with IPV4 public address',i_d.get("PublicIpAddress",'not assigned'))

            except ClientError as e:
                print(e)                       
        
        elif action=='stop': ############ STOP ###############
            # Do a dryrun first to verify permissions            
            try:
                ec2_cli.stop_instances(InstanceIds=[id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise 
            # Dry run succeeded, run without dryrun
            try:
                response = ec2_cli.stop_instances(InstanceIds=[id], DryRun=False)
                #response=response['StoppingInstances'][0]['CurrentState']['Name']
                #print(f'Status after action: {response.upper()} ')
                #i_d = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]["Instances"][0]
                #print(f'Status after action: {i_d["State"]["Name"].upper()},', end='')
                #print(' with IPV4 public address',i_d.get("PublicIpAddress",'not assigned'))
            except ClientError as e:
                print(e)   
                
        elif action=='reboot': ############ REBOOT ###############
            # Do a dryrun first to verify permissions            
            try:
                ec2_cli.reboot_instances(InstanceIds=[id], DryRun=True)
            except ClientError as e:
                if 'DryRunOperation' not in str(e):
                    raise 
            # Dry run succeeded, run without dryrun
            try:
                response = ec2_cli.reboot_instances(InstanceIds=[id], DryRun=False)
                #tw=1; print(f'Wait {tw} seconds'); time.sleep(tw)
                #i_d = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]["Instances"][0]
                #print(f'Status after action: {i_d["State"]["Name"].upper()}', end='')
                #print(' with IPV4 public address',i_d.get("PublicIpAddress",'not assigned'))
            except ClientError as e:
                print(e)

        i_d = ec2_cli.describe_instances(InstanceIds=[inst['id']])["Reservations"][0]["Instances"][0]
        print(f'Status after action: {i_d["State"]["Name"].upper()}')
        #print(' with IPV4 public address',i_d.get("PublicIpAddress",'not assigned'))

        print()
      
