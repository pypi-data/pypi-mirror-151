import pprint as pp
from linode_api4 import LinodeClient

token="ab4c2fc2f7e2f50bb841bcaecb0ade9515578a36986b20db94cf07e863558c01"

client = LinodeClient(token)


linodes = client.linode.instances()

for linode in linodes:
    print('______________') 
    print(linode.id)   
    print(linode.label)
    pp.pprint(dir(linode) )



"""

    print(server.data_model)
    print(server.id)
    print(server.name)
    print(server.status)
    #pp.pprint(dir(server.public_net.ipv4))
    print(server.public_net.ipv4.ip)
    
    #pp.pprint(dir(server.private_net.data_model))
    #print(server.private_net[0]) # IndexError ???
    #print


    for i,item in enumerate(server.private_net):
        print(item.ip)
        #pp.pprint(dir(item))
    
    #pp.pprint(dir(server.image))
    #print(server.image)
    print(server.datacenter.location)
    
    
    #print(dir(server.server_type.data_model))
    print('CPUs:',server.server_type.data_model.cores)
    #print(server._client)
    #pp.pprint(dir(server))
    #pp.pprint(dir(server.data_model))
    
    
    #print(server.__dict__)
    #print(server._client.__dict__)


"""