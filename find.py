import mysql.connector
import os
import datetime
import time
from pathlib import Path

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql73my2019#",
  database="warehouse"
)

def findItem(pid):
   #print("FIND ITEMS")
   mycursor = mydb.cursor()
   id_list = []
   msg = "Finding IDs was successful."
   sql1 = "SELECT RFID FROM ITEM I,EVENTS E WHERE I.INVENTORYID = E.INVENTORYID AND PRODUCTID = %s AND DESTOCKING IS NULL"
   flag = 0
   try:
      val = (pid,)
      mycursor.execute(sql1, val)
      result = mycursor.fetchall()
      #print(result)
      for x in result:
         id_list.append(x[0])
   except mysql.connector.Error as err:
      #print("ERROR: "+err)
      msg = "Unknown error occurred."
   mycursor.close()
   #print(msg, id_list)
   return msg, id_list

def findPID(name):
   mycursor = mydb.cursor()
   id_list = []
   msg = "Done searching."
   sql1 = "SELECT PRODUCTID FROM PRODUCT WHERE NAME = %s"
   flag = 0
   try:
      val = (name,)
      mycursor.execute(sql1, val)
      result = mycursor.fetchall()
      print(result)
      for x in result:
         id_list.append(x[0])
   except mysql.connector.Error as err:
      print("ERROR: "+err)
      msg = "Unknown error occurred."
   mycursor.close()
   #print(msg)
   return msg, id_list
   
def writeRFIDs(ids):
   #print("WRITE IDS")
   f = open("transfers/rfids.txt", "w")
   
   for rfid in ids:
      f.write(rfid)
      f.write("\n")
      
   f.close()
   
def updateDatabase():
   print("UPDATE DATABASE")
   idfile = Path("/Users/nayana/projects/WarehouseManagement/transfers/check.txt")
   tempfile = Path("/Users/nayana/projects/WarehouseManagement/transfers/check1.txt")
   
   while(1):
      ftemp = open("transfers/check1.txt","r")
      if(ftemp.read(1)=="1"):
         break
   
   f = open("transfers/check.txt", "r")
   
   ids = []
   
   for line in f:
      ids.append(line)
   
   for rfid in ids:
      mycursor = mydb.cursor()
      msg = "Product removal was successful."
      print(rfid)
      sql1 = "SELECT INVENTORYID FROM ITEM WHERE RFID = %s"
      sql2 = "UPDATE EVENTS SET DESTOCKING = %s WHERE INVENTORYID = %s" 
      flag = 0
      destock = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
      try:
         val1 = (rfid,)
         mycursor.execute(sql1, val1)
         res = mycursor.fetchone()
         val2 = (destock, res[0])
         mycursor.execute(sql2, val2)
         if mycursor.rowcount==0:
            flag = 1
            msg = "Removal unsuccessful."
         else:
            mydb.commit()
            open('transfers/check.txt', 'w').close()
            ftemp = open("transfers/check1.txt","w")
            ftemp.write("0")
      except mysql.connector.Error as err:
         print("ERROR: "+err)
         msg = "Unknown error occurred."
      mycursor.close()
      #print(msg)
      return msg
