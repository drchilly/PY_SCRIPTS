import napalm
import ciscosparkapi
import env_user
import sys
import os
from time import gmtime, strftime
import json

def main():
    """Grab a config for the device."""

    time = strftime("%Y-%m-%d@%H-%M", gmtime())
    # Use the appropriate network driver to connect to the device:
    driver = napalm.get_network_driver('ios')

    # Connect: PUT ADEQUATE USERNAME AND password
    device = driver(hostname='192.168.24.1', username='dragan.ilic',
                    password='wersdf123!')

    spark = ciscosparkapi.CiscoSparkAPI(access_token=env_user.SPARK_ACCESS_TOKEN)
    print ('Opening ...')
    device.open()
    ios_facts = device.get_facts()
    running_config = device.get_config()
    runn_final = running_config.get("running")
    #print (runn_final) --> CHECK RUNN BEFORE PUTING INSIDE FILE

    ###TRY TO FORMAT OUTPUT RUNNING CONFIG###
    #run2file = json.dumps(running_config, indent=4)
    #run2file = run2file.replace("\\n", "")
    #run2file = run2file.strip(' \t\n\r')
    #run2file2 = run2file.get("running")
    #print (run2file2)

    #with open(run2file) as run2file2:
        #run2fileFinal = run2file2.read().splitlines()
            #print (lines)
    #running_config = running_config.strip(' \t\n\r')
    #print (running_config)

    #checkpoint = device._get_checkpoint_file()
    #print(checkpoint)

    #create the directory if it does not exist
    if not os.path.exists("Backup"):
      os.makedirs("Backup")

    f = open("Backup/" + ios_facts['hostname'] + "." + time, 'w')
    f.write(runn_final)
    f.close
    message = spark.messages.create(env_user.SPARK_ROOM_ID,
              #files=[next_data_file],
              text='BACKUP COMPLETED')
    print(message)
    device.close()
if __name__ == '__main__':
    main()
