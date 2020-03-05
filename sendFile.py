import paramiko
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client
    
def sendFile():
   print("SEND FILE")
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect("192.168.43.164", 22, "pi","raspberry")
   #scp = SCPClient(ssh.get_transport())
   ftp_client=ssh.open_sftp()
   ftp_client.put('/Users/nayana/projects/WarehouseManagement/transfers/rfids.txt','/home/pi/transfers/rfids.txt')
   ftp_client.close()