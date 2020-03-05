import mysql.connector
import matplotlib
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt
import cv2

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'sql73my2019#',
    database = 'Warehouse')

mycursor = mydb.cursor()

def graph1():
    mycursor.execute("SELECT PRODUCTID,AVG(TIMESTAMPDIFF(SQL_TSI_DAY,STOCKING,DESTOCKING)) FROM ITEM I, EVENTS E WHERE I.INVENTORYID = E.INVENTORYID AND DESTOCKING IS NOT NULL GROUP BY PRODUCTID")
    res = mycursor.fetchall()
    #print(res)
    for x in res:
        plt.scatter(x[0],int(x[1]))
    plt.ylabel('Average Warehouse time')
    plt.xlabel('Product ID')
    plt.title('Average Warehouse Time for Various Products')
    plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph1.png')
    plt.clf()
    plt.cla()
    return None
    
def graph2():
   mycursor.execute("SELECT PRICE, LEADTIME FROM HAS_SUPPLIER")
   res = mycursor.fetchall()
   #print(res)
   for x in res:
       plt.scatter(x[0],x[1])
   plt.ylabel('Lead Time')
   plt.xlabel('Price')
   plt.title('Price vs. Lead Time')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph2.png')
   plt.clf()
   plt.cla()
   return None
   
def graph3():
   """
   mycursor.execute("SELECT PRODUCTID, COUNT(SUPPLIERID) FROM HAS_SUPPLIER GROUP BY PRODUCTID")
   res = mycursor.fetchall()
   for x in res:
       plt.scatter(x[0],x[1])
   plt.ylabel('Number of Suppliers')
   plt.xlabel('Product ID')
   plt.title('Number of Suppliers for each Product')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph3.png')
   plt.clf()
   plt.cla()
   return None
   """
   mycursor.execute("SELECT PRODUCTID, COUNT(SUPPLIERID) FROM HAS_SUPPLIER GROUP BY PRODUCTID")
   res = mycursor.fetchall()
   arr = []
   labels = []
   for x in res:
       arr.append(x[1])
       labels.append(x[0])    
   length = list(range(1, len(labels)+1))
   plt.bar(length, height = arr, tick_label = labels)
   plt.ylabel('Number of Suppliers')
   plt.xlabel('Product ID')
   plt.title('Number of Suppliers for each Product')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph3.png')
   plt.clf()
   plt.cla()
   return None
   
def graph4():
   mycursor.execute("SELECT PRODUCTID,AVG(LEADTIME) FROM HAS_SUPPLIER GROUP BY PRODUCTID")
   res = mycursor.fetchall()
   for x in res:
       plt.scatter(x[0],x[1])
   plt.ylabel('Average Lead Time')
   plt.xlabel('Product ID')
   plt.title('Average Lead Time for each Product')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph4.png')
   plt.clf()
   plt.cla()
   return None
   
def graph5():
   mycursor.execute("SELECT MAX(LEADTIME) FROM HAS_SUPPLIER")
   res1 = mycursor.fetchone()
   maxlt = res1[0]
   m1 = int(maxlt/3)
   m2 = int(2*m1)
   sql1 = "SELECT COUNT(*) FROM HAS_SUPPLIER WHERE LEADTIME > %s"
   val1 = (m1,)
   mycursor.execute(sql1, val1)
   res2 = mycursor.fetchone()
   v1 = int(res2[0])
   sql2 = "SELECT COUNT(*) FROM HAS_SUPPLIER WHERE LEADTIME > %s AND LEADTIME < %s"
   val2 = (m1, m2)
   mycursor.execute(sql2, val2)
   res3 = mycursor.fetchone()
   v2 = int(res3[0])
   sql3 = "SELECT COUNT(*) FROM HAS_SUPPLIER WHERE LEADTIME > %s"
   val3 = (m2,)
   mycursor.execute(sql3, val3)
   res4 = mycursor.fetchone()
   v3 = int(res4[0])
   
   xvals = [v1, v2, v3]
   labels = ['Low lead time', 'Moderate lead time', 'Large lead time']
   plt.pie(xvals, labels=labels)
   plt.title('Lead Times')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph5.png')
   plt.clf()
   plt.cla()
   return None
   
def graph6():
    mycursor.execute("SELECT TIMESTAMPDIFF(SQL_TSI_DAY,STOCKING,DESTOCKING) FROM EVENTS WHERE DESTOCKING IS NOT NULL")
    res = mycursor.fetchall()
    arr = []
    for x in res:
        arr.append(x[0])
    plt.boxplot(arr)
    plt.title('Warehouse Shelf Times')
    plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph6.png')
    plt.clf()
    plt.cla()
    return None
    
def graph7():
   mycursor.execute("SELECT PRICE*LEADTIME FROM HAS_SUPPLIER")
   res = mycursor.fetchall()
   arr = []
   for x in res:
       arr.append(x[0])
   plt.boxplot(arr)
   plt.title('Product of Lead Time and Price')
   plt.savefig('/Users/nayana/projects/WarehouseManagement/static/graphs/graph7.png')
   plt.clf()
   plt.cla()
   return None


   
