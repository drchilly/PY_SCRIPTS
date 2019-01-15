import napalm
import ciscosparkapi
import env_user
import sys
import os
import time
from time import gmtime, strftime
import json

def main():
    """Grab a config for the device."""

    time = strftime("%Y-%m-%d@%H-%M", gmtime())
    spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)
    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver('ios')

    with open (r'ios_list.txt', 'r') as ip_input:
        for ip in ip_input:
            ip = ip.strip()

    # Connect: PUT ADEQUATE USERNAME AND password
            device = driver(hostname=ip, username='???',
                    password='???')


            print ('Opening ...')
            device.open()
            ios_facts = device.get_facts()
            running_config = device.get_config()
            runn_final = running_config.get("running")
    #print (runn_final) --> CHECK RUNN BEFORE PUTING INSIDE FILE

    ##################
    #OUTPUT GENERATED FOR FILES
    ###########################
    #mytime = time.strftime('%Y-%m-%d-%H-%M-%S')
    #Remove the trailing /n from varible ip this is required for file creation
            ip = ip.strip(' \t\n\r')
            print
            print (ip + ' config backup in place')
            print
    #filename = 'tas_%s.txt' % str(ip)
    #filename = os.path.join('NETVIRT-', mytime)
            filename = ("NETVIRT-" + time)
            filepath = os.path.join('configs', ip, filename)

            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            with open(filepath, "w") as f:
                f.write(runn_final)
                f.close()


    #create the directory if it does not exist
    #if not os.path.exists("Backup"):
      #os.makedirs("Backup")

    #f = open("Backup/" + ios_facts['hostname'] + "." + time, 'w')
    #f.write(runn_final)
    #f.close
            message = spark.messages.create(env_user.SPARK_ROOM_ID,
              #files=[next_data_file],
              text='BACKUP COMPLETED')
            print(message)
            device.close()
if __name__ == '__main__':
    main()
