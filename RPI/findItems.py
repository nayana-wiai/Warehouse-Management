import paramiko
from scp import SCPClient
import RPi.GPIO as GPIO
import rfid

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def FindItem():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.IN)

    f = open("transfers/rfids.txt","r")
    ids = []
    for line in f:
        line = line.replace("[","").replace("]","").replace("\n","")
        id = line.split(", ")
        ids.append(id)
    print(ids)
    f.close()

    while(1):
        #print GPIO.input(4)
        foundID = None
        if GPIO.input(4) == 0:
            foundID = rfid.readIDs(ids)
        if foundID is not None:
            print("Item with RFID ", foundID, " has been found.")
            print("Sending back: ", foundID)
            return foundID
        else:
            print("Wrong item. Continue.")

def Final():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.1.3", 22, "nayana","nayana1999")
    scp = SCPClient(ssh.get_transport())

    ret = FindItem()

    f = open("transfers/check.txt","w")
    f.write(str(ret))
    f.close()

    ftp_client=ssh.open_sftp()
    ftp_client.put('/home/pi/transfers/check.txt','/Users/nayana/projects/WarehouseManagement/transfers/check.txt')
    ftp_client.close()

Final()
