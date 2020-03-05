from flask import Flask, flash, render_template, request, redirect
import os
import add
import find
import sendFile
import analytics

path = '/Users/nayana/projects/WarehouseManagement/static/graphs/'

app = Flask(__name__)
app.secret_key = b'_5q35$2qfiqu783b3#'
app.debug = True

def getFiles():
   imagePaths = []
   for subdir, dirs, files in os.walk(path):
       for file in files:
           filepath = os.path.join(subdir, file)
           statinfo = os.stat(filepath)
           if statinfo.st_size!=0:
               if filepath.endswith('.jpg') or filepath.endswith('.JPG') or filepath.endswith('.png') or filepath.endswith('.PNG'):
                   if filepath not in imagePaths:
                       imagePaths.append('../static/graphs/'+filepath.replace(path, ''))
   return imagePaths

@app.route('/', methods=['GET','POST'])
def index():
   analytics.graph1()
   analytics.graph2()
   analytics.graph3()
   analytics.graph4()
   analytics.graph5()
   analytics.graph6()
   analytics.graph7()
   
   images = getFiles()
   return render_template('index.html', stats = images) 
 
@app.route('/addproduct', methods=['GET','POST'])      
def add_product():
   form_id = request.form['ID']
   form_name = request.form['Name']
   form_desc = request.form['Description']
   form_price = request.form['Price']
   form_supplier = request.form['SupplierID']
   form_lead = request.form['Lead']
   form_vol = request.form['Volume']
   form_shape = request.form['Shape']
   form_fragile = request.form['Fragile']
   
   msg = add.addProduct(form_id, form_name, form_desc, form_price, form_supplier, form_lead, form_vol, form_shape,form_fragile)
   print(msg)
   flash(msg)
   
   return redirect("/")
   
@app.route('/adddetails', methods=['GET','POST'])      
def add_details():
   form_id = request.form['ID']
   form_sid = request.form['SupplierID']
   form_price = request.form['Price']
   form_lead = request.form['Lead']
   
   msg = add.addDetails(form_id, form_sid, form_price, form_lead)
   print(msg)
   flash(msg)
   
   return redirect("/")

@app.route('/addstock', methods=['GET','POST'])      
def add_stock():
   form_id = request.form['ID']
   form_RFID = request.form['RFID']
   
   msg = add.addStock(form_id, form_RFID)
   print(msg)
   flash(msg)
   
   return redirect("/")
   
@app.route('/addsupplier', methods=['GET','POST'])      
def add_supplier():
   form_id = request.form['SupplierID']
   form_name = request.form['Name']
   
   msg = add.addSupplier(form_id, form_name)
   print(msg)
   flash(msg)
   
   return redirect("/")
   
@app.route('/finditem', methods=['GET','POST'])      
def find_item():
   form_id = request.form['ID']
   
   _, ids = find.findItem(form_id)
   
   if len(ids)!=0:
      print("IDs being sent:", ids)
   
      find.writeRFIDs(ids)
   
      sendFile.sendFile()
   
      msg = find.updateDatabase()
   
      print("After updates")
   else:
      msg = "Product not found"
   print(msg)
   flash(msg)
   return redirect("/")
   
@app.route('/findpid', methods=['GET','POST'])      
def find_pid():
   form_name = request.form['Name']
   
   msg, ids = find.findPID(form_name)
   listToStr = ', '.join([str(elem) for elem in ids]) 
   #if len(ids)>1:
       #listToStr = listToStr[0:len(listToStr)-1]
   flash(msg + " Product IDs: "+ listToStr)
   print(msg)
   return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)