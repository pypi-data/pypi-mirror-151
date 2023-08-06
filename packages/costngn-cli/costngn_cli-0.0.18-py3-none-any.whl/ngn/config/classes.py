#Instance Dictionary Structure


RepBase={
    'instances':    [],
    #'user':        '',
    'month_cost':   0,
    'life_cost':    0,
    'priceunit':    '',
    }

awsRegBase={
    'id':       '',
    'inst':     [],
    'rmprice':  '',
    'rhprice':  '',
    }

InstBase={
        'id'  :     '',
        'name':     '',
        'tags':     {},
        'provider': '',
        'prov_full':'',
        'region':   '',
        'status':   '',
        'birthday': '',
        'ipv4priv': '',
        'ipv4pub':  '',
        'type':     '',
        'cpus':     '',
        'os':       '',
        'memory':   '',
        'image':    '',
        'vpc_id':   '',
        'avzone':   '',
        'ihprice':  '',        
        'imprice':  '',        
        'month_cost': '',
        'life_cost':   '',        
    }

lab_dict={
        'id'  :     'Id',
        'name':     'Name',
        'tags':     'Tags',
        'provider': 'Company',
        'prov_full':'Company',
        'region':   'Region',
        'status':   'Status',
        'birthday': 'Create Day',
        'ipv4priv': 'IPV4 Priv Add',
        'ipv4pub':  'IPV4 Pub Add',
        'type':     'Type',
        'cpus':     'CPUs',
        'os':       'Oper.System',
        'memory':   'Memory',
        'image':    'Image',
        'vpc_id':   'VPC',
        'avzone':   'Avail.Zone',
        'ihprice':  'Hourly Price',        
        'imprice':  'Monthly Price',        
        'month_cost': 'M.Cost(estim)',
        'life_cost':'Life Cost',        
    }

inst_out_list_base=[
    'id',
    'name',

    #'tags',
    #'provider',
    'prov_full',    
    'region',    
    'status',
    'birthday',
    'ipv4priv',
    'ipv4pub',
    'type',
    'cpus',
    #'os',
    'memory',
    'image',
    'vpc_id',
    'avzone',
    'ihprice',    
    'imprice',    
    'month_cost',
    'life_cost',
]

# Normalized format for birthday date and time
birth_format='%Y-%m-%d %H:%M:%S'

