import requests
import string
import random

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

if __name__ == '__main__':

    compuStoreConnection = mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
    compuStoreCursor = compuStoreConnection.cursor(prepared=True)
    
    ##LaptopModelLaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail, price)
    compustoreInsertLaptop = "INSERT INTO LaptopModel VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
   
    branch1Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch1")
    branch1Cursor = branch1Connection.cursor(prepared=True)
   
    branch2Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch2")
    branch2Cursor = branch2Connection.cursor(prepared=True)
   
    branch3Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch3")
    branch3Cursor = branch3Connection.cursor(prepared=True)
    
    ##LaptopModelLaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail)
    branchInsertLaptop = "INSERT INTO LaptopModel VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    ##ModelStockInfo(model_id, amt_in_stock)
    branchInsertModelStockInfo = "INSERT INTO ModelStockInfo VALUES (%s, %s)"
    
    ##ModelItem(model_id, product_id)
    branchInsertModelItem = "INSERT INTO ModelItem VALUES (%s, %s)"
    
    pID = set()
    mID = set()
    
    k = 0
    
    laptopFile=open("laptops.txt", "r")
    print("Start...")
    
    lines = laptopFile.readlines()
    
    for line in lines:
        line = line.split(",")
        
        model = line[0]
        
        brand = line[1]
        
        model_id = brand + ''.join(random.choice(string.digits) for _ in range(5))
        while model_id in mID:
            model_id = brand + ''.join(random.choice(string.digits) for _ in range(5))
        mID.add(model_id)
        
        cpu = line[2]
        displaySize = float(line[3])
        resolution = line[4]
        os = line[5]
        gpu = line[6]
        launchDate = line[7] 
                
        thumbnail = line[8]

        price = float(line[9]) * 130.00
        
        ##LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail, price)
        compuStoreLaptopValues = (model_id, model, brand, cpu, displaySize, resolution, os, gpu, launchDate, thumbnail, price)
        
        compuStoreCursor.execute(compustoreInsertLaptop, compuStoreLaptopValues)
        
        ##LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail)
        branchLaptopValues = (model_id, model, brand, cpu, displaySize, resolution, os, gpu, launchDate, thumbnail)
        
        branch1Cursor.execute(branchInsertLaptop, branchLaptopValues)
        branch2Cursor.execute(branchInsertLaptop, branchLaptopValues)
        branch3Cursor.execute(branchInsertLaptop, branchLaptopValues)
        
        ##ModelStockInfo(model_id, amt_in_stock)
        amt_in_stock = random.randint(250,280)
        
        branchModelStockInfoValues = (model_id, amt_in_stock)
        
        branch1Cursor.execute(branchInsertModelStockInfo, branchModelStockInfoValues)
        
        for _ in range(amt_in_stock):
            
            ##Branch1 item
            product_id1 = random.randint(1,2147483647)
            while product_id1 in pID:
                product_id1 = random.randint(1,2147483647)
            pID.add(product_id1)
            
            ##ModelItem(model_id, product_id)
            branchModelItemValues = (model_id, product_id1)
            
            branch1Cursor.execute(branchInsertModelItem, branchModelItemValues)
        
        ##ModelStockInfo(model_id, amt_in_stock, amt_sold)
        amt_in_stock = random.randint(250,280)
        
        branchModelStockInfoValues = (model_id, amt_in_stock)
        
        branch2Cursor.execute(branchInsertModelStockInfo, branchModelStockInfoValues)
        
        for _ in range(amt_in_stock):
            
            ##Branch2 item
            product_id2 = random.randint(1,2147483647)
            while product_id2 in pID:
                product_id2 = random.randint(1,2147483647)
            pID.add(product_id2)
            
            ##ModelItem(model_id, product_id)
            branchModelItemValues = (model_id, product_id2)
            
            branch2Cursor.execute(branchInsertModelItem, branchModelItemValues)
        
        ##ModelStockInfo(model_id, amt_in_stock, amt_sold)
        amt_in_stock = random.randint(250,280)
        
        branchModelStockInfoValues = (model_id, amt_in_stock)
        
        branch3Cursor.execute(branchInsertModelStockInfo, branchModelStockInfoValues)
        
        for _ in range(amt_in_stock):
            
            ##Branch3 item
            product_id3 = random.randint(1,2147483647)
            while product_id3 in pID:
                product_id3 = random.randint(1,2147483647)
            pID.add(product_id3)
            
            ##ModelItem(model_id, product_id)
            branchModelItemValues = (model_id, product_id3)
            
            branch3Cursor.execute(branchInsertModelItem, branchModelItemValues)
    
        k+=1
        compuStoreConnection.commit()
        branch1Connection.commit()
        branch2Connection.commit()
        branch3Connection.commit()
        print ("Laptop Items added")
        print("Got model info ... %s." % k)

    #closing database connection.
    if(compuStoreConnection.is_connected()):
        compuStoreCursor.close()
        compuStoreConnection.close()
        print("MySQL compuStoreConnection is closed and %s laptop model added." %k) 
        
    if(branch1Connection.is_connected()):
        branch1Cursor.close()
        branch1Connection.close()
        print("MySQL branch1Connection is closed and %s laptop model added." %k) 
        
    if(branch2Connection.is_connected()):
        branch2Cursor.close()
        branch2Connection.close()
        print("MySQL branch2Connection is closed and %s laptop model added." %k) 
    
    if(branch3Connection.is_connected()):
        branch3Cursor.close()
        branch3Connection.close()
        print("MySQL branch3Connection is closed and %s laptop model added." %k) 