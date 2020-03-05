import mysql.connector
import datetime
import time
import re

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql73my2019#",
  database="Warehouse"
)

def addProduct(pid, name, desc, price, supplierid, lead, vol, shape, fragile):
   flag = 0
   msg = "Product insert successful."
   if float(price)<=0:
      print("Negative price")
      msg = "Invalid price"
      flag = 1   
   if int(lead)<=0:
      msg = "Invalid lead time"
      flag = 1  
   mycursor = mydb.cursor()
   sql1 = "SELECT ProductID from PRODUCT WHERE ProductID = '"+pid+"'" 
   sql2 = "SELECT SupplierID from SUPPLIER WHERE SupplierID = '"+supplierid+"'"
   sql3 = "INSERT INTO PRODUCT(ProductID, Name, Description) VALUES(%s, %s, %s)"
   sql4 = "INSERT INTO HAS_SUPPLIER VALUES(%s, %s, %s, %s)"
   sql5 = "INSERT INTO CHARACTERISTICS VALUES(%s, %s, %s, %s)"
   if flag==0:
      try:
         mycursor.execute(sql1)
         res1 = mycursor.fetchall()
         if len(res1)>0:
            flag = 1
            msg = "This Product ID already exists."
         mycursor.execute(sql2)
         res2 = mycursor.fetchall()
         if len(res2)==0:
            flag = 1
            msg = "This Supplier ID does not exist."
         if flag==0:
            val = (pid, name, desc)
            mycursor.execute(sql3, val)
            #mydb.commit()
            val = (pid, supplierid, lead, price)
            mycursor.execute(sql4, val)
            val = (pid, vol, shape, fragile)
            mycursor.execute(sql5, val)
            mydb.commit()
      except mysql.connector.Error as err:
         print("ERROR: "+err)
         msg = "Unknown error occurred."
   mycursor.close()
   #print(msg)
   return msg
   
def addDetails(pid, sid, price, lead):
   if int(lead)<=0:
      msg = "Invalid lead time"
      return msg
   if int(price)<=0:
      msg = "Invalid price"
      return msg
   mycursor = mydb.cursor()
   msg = "Supplier update for product successful."
   sql1 = "SELECT ProductID from PRODUCT WHERE ProductID = '"+pid+"'" 
   sql2 = "SELECT SupplierID from SUPPLIER WHERE SupplierID = '"+sid+"'"
   sql3 = "INSERT INTO HAS_SUPPLIER VALUES (%s, %s, %s, %s)"
   flag = 0
   try:
      mycursor.execute(sql1)
      res1 = mycursor.fetchall()
      if len(res1)==0:
         flag = 1
         msg = "This Product ID does not exist."
      mycursor.execute(sql2)
      res2 = mycursor.fetchall()
      if len(res2)==0:
         flag = 1
         msg = "This Supplier ID does not exist."
      if flag==0:
         val = (pid, sid, lead, price)
         mycursor.execute(sql3, val)
         mydb.commit()
   except mysql.connector.Error as err:
      #print("ERROR: "+err)
      msg = "This combination already exists."
   mycursor.close()
   #print(msg)
   return msg
   
def checkRFID(rfid):
   pattern = '\[0[x,X][a-fA-F0-9]{1,2}, 0[x,X][a-fA-F0-9]{1,2}, 0[x,X][a-fA-F0-9]{1,2}, 0[x,X][a-fA-F0-9]{1,2}\]'
   check = re.search(pattern,rfid)
   if check.span()==(0,len(rfid)):
      return True
   else:
      return False

def addStock(pid, rfid):
   flag = 0
   msg = "Stock update successful."
   #if checkRFID(rfid)==False:
      #flag = 1
      #msg = "Invalid RFID"
   mycursor = mydb.cursor()
   sql1 = "SELECT ProductID from PRODUCT WHERE ProductID = '"+pid+"'"
   sql2 = "INSERT INTO ITEM(RFID, ProductID) VALUES (%s, %s)"
   sql3 = "INSERT INTO EVENTS(STOCKING, INVENTORYID) VALUES(%s, %s)"
   stock = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
   try:
      mycursor.execute(sql1)
      res1 = mycursor.fetchall()
      if len(res1)==0:
         flag = 1
         msg = "This Product ID does not exist."
      if flag==0:
         val = (rfid, pid)
         mycursor.execute(sql2, val)
         mycursor.execute("SELECT MAX(INVENTORYID) FROM ITEM")
         myresult = mycursor.fetchall()
         for x in myresult:
            inventoryid = x[0]
         val = (stock, inventoryid)
         mycursor.execute(sql3, val)
         mydb.commit()
   except mysql.connector.Error as err:
      print("ERROR: "+err)
      msg = "Unknown error occurred."
   mycursor.close()
   #print(msg)
   return msg

def addSupplier(sid, name):
   mycursor = mydb.cursor()
   msg = "Supplier insert successful."
   sql1 = "SELECT SupplierID from SUPPLIER WHERE SupplierID = '"+sid+"'"
   sql2 = "INSERT INTO SUPPLIER VALUES (%s, %s)"
   flag = 0
   try:
      mycursor.execute(sql1)
      res1 = mycursor.fetchall()
      if len(res1)>0:
         flag = 1
         msg = "This supplier already exists."
      if flag==0:
         val = (sid, name)
         mycursor.execute(sql2, val)
         mydb.commit()
   except:
      print("ERROR: "+err)
      msg = "Unknown error occurred."
   mycursor.close()
   #print(msg)
   return msg
