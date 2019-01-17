import napalm
import os
import sys

def change_config():
driver = napalm.get_network_driver('ios')


    #with open (r'router_list.txt', 'r') as ip_input:
     #   for ip in ip_input:
      #      ip = ip.strip()

    # Connect: PUT ADEQUATE USERNAME AND password
device = driver(hostname='x.x.x.x', username='???', password='???')
#print ('Openning...')
    #MAKE CONFIG CHANGE
device.open()
device.load_merge_candidate(config='interface Loopback201\ndescription TEST\nip address 111.111.111.111 255.255.255.0')
            
print (device.compare_config())
device.close()
if __name__ == '__change_config__':
    change_config()