#
#Connect and backup cisco device configs using python
#
import paramiko
import ftplib
import time
import os

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

# Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

if __name__ == '__main__':

# VARIABLES THAT NEED CHANGED
#ip = 'x.x.x.x'
#ipaddress = open('list.txt')
    username = 'dragan.ilic'
    password = '?????'
    port = '22'

with open (r'list.txt', 'r') as ip_input:
    for ip in ip_input:
        ip = ip.strip()

# Create instance of SSHClient object
        remote_conn_pre = paramiko.SSHClient()

# Automatically add untrusted hosts (make sure okay for security policy in your environment)
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# initiate SSH connection
        remote_conn_pre.connect(ip, port=port, username=username, password=password)
        print '#################################################'
        print "SSH connection established to %s" % ip

# Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
# print "Interactive SSH session established"

# Strip the initial router prompt
        output = remote_conn.recv(1000)


# Turn off paging
disable_paging(remote_conn)

# Send the router a command
# remote_conn.send("\n")
# remote_conn.send("show ip int brief\n")

# Required if you need an enable password to login
# remote_conn.send("en\n")
# remote_conn.send("cisco\n")

remote_conn.send("\n")
output = remote_conn.recv(0)
#output = ''
remote_conn.send("show run\n")

remote_conn.send("copy running-config ftp://netvirtexpert.zapto.org/cme-backup\n")

# Wait for the command to complete
time.sleep(2)

output = remote_conn.recv(500000000)

# print output
# print output

##################
#OUTPUT GENERATED FOR FILES
###########################
mytime = time.strftime('%Y-%m-%d-%H-%M-%S')
#Remove the trailing /n from varible ip this is required for file creation
ip = ip.strip(' \t\n\r')
print
print ip + ' config backup in place'
print
#filename = 'tas_%s.txt' % str(ip)
#filename = os.path.join('GigaKOM-', mytime)
filename = ("GigaKOM-" + mytime)
filepath = os.path.join('configs', ip, filename)

if not os.path.exists(os.path.dirname(filepath)):
    os.makedirs(os.path.dirname(filepath))
with open(filepath, "w") as f:
    f.write(output)
    f.close()

###FTP UPLOAD na NETVIRT###
def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in (".txt", ".htm", ".html"):
        ftp.storlines("STOR " + file, open(file))
    else:
        ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

ftp = ftplib.FTP('netvirtexpert.zapto.org','ra_ftp_user','?????')
os.chdir(os.path.dirname(filepath))
upload(ftp, filename)


#disconnect
remote_conn.send("exit\n")
print "SSH connection closed to %s" % ip
print '#################################################'
