from faker import Faker
fake=Faker()
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

import random
import sqlController
import requests
import string


def phoneNumber():
    p=list('(876)-000-0000')
    p[6] = str(random.randint(1,9))
    for i in [7,8,10,11,12,13]:
        p[i] = str(random.randint(0,9))

    p = ''.join(p)
    return p[:5]+ ''+ p[5:9] +''+ p[9:]

def year():
    p=list('2000')
    p[2] = str(random.randint(2,3))
    p[3] = str(random.randint(0,9))
    p = ''.join(p)
    return p[:2]+''+ p[2:]

def cardNum():
    p=list('0000000000000000')
    p[0] = str(random.randint(1,9))
    for i in range(1,16):
         p[i] = str(random.randint(0,9))
    p = ''.join(p)
    return p[:1]+''+ p[1:]

def cardSC():
    p=list('000')
    for i in range(0,3):
         p[i] = str(random.randint(0,9))
    p = ''.join(p)
    return int(p[0:])

# use to populate the CustomerAccount table in the CompuStoreDB
gender=['Male','Female']
parish = ['Portland','St Mary','St Thomas','St Ann','Kingston','St Andrew','St Catherine','St Jame','Manchester','Hanover','Clarendon','Westmoreland','Trelawny','St Elizabeth']
#CustomerAccount(account_id, email, password, fname, lname, gender, date_of_birth, street, city, parish, telephone, created_on)
def insertCusAcc(times):
    try:
       connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
       cursor = connection.cursor(prepared=True)

       for _ in range(times):
           gen=gender[random.randint(0,1)]
           sql_insert_data_query="INSERT INTO CustomerAccount(email,password,fname,lname,gender,date_of_birth,street,city,parish,telephone,created_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
           if gen=='Male':
               insert_tuple=(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_male(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today"))
           else:
               insert_tuple=(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_female(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today") )

           cursor.execute(sql_insert_data_query,insert_tuple)
       connection.commit()
       print ("Date Record inserted successfully into CustomerAccount table")
    except mysql.connector.Error as error :
        print("Failed inserting date object into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

## use to populate the CreditCardDetails table and CustomerCeditCard in the CompuStoreDB
#CreditCardDetails(card_num,name_on_card,card_security_code,expiration_month, expiration_year, billing_street, billing_city, billing_parish)
#CustomerCreditCard(account_id, card_num)
def insertCard(start,end):
    try:
        connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
        cursor = connection.cursor(prepared=True)
        for i in range(start,end):
            # fetching information about customer from CustomerAccount table
            cursor.execute("SELECT account_id, fname, lname, street, city, parish FROM CompuStore.CustomerAccount where account_id={}".format(i))
            result = cursor.fetchone()
            name=result[1].decode()+" "+result[2].decode()

            # insert data into the CreditCardDetail table
            card=cardNum()
            sql_insert_data_query="INSERT INTO CreditCardDetails(card_num,name_on_card,card_security_code,expiration_month,expiration_year,billing_street,billing_city,billing_parish) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            insert_tuple=(card,name,cardSC(),fake.month(),year(),result[3].decode(),result[4].decode(),result[5].decode())
            cursor.execute( sql_insert_data_query,insert_tuple)

            # insert data into the CustomerCreditCard table
            sql_insert_data_query="INSERT INTO CustomerCreditCard(account_id,card_num) VALUES (%s,%s)"
            insert_tuple=(result[0],card)
            cursor.execute( sql_insert_data_query,insert_tuple)

        connection.commit()
        print ("Date Record inserted successfully CreditCardDetails and CustomerCreditCard into tables")
    except mysql.connector.Error as error :
        print("Failed inserting date object into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#Branch(br_id, name, street, city, parish, telephone)
def insertBranch():
    connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
    cursor = connection.cursor(prepared=True)
    sql_insert_data_query="insert into Branch(br_id, name, street, city, parish, telephone) values('B01','branch1','williams','Stony Hill','Portland','(876)-799-7900')"
    cursor.execute( sql_insert_data_query)
    sql_insert_data_query="insert into Branch(br_id, name, street, city, parish, telephone) values('B02','branch2','Cherry','Hill city','Kingston','(876)-999-7911')"
    cursor.execute( sql_insert_data_query)
    sql_insert_data_query="insert into Branch(br_id, name, street, city, parish, telephone) values('B03','branch3','organe',' Big city','Westmoreland','(876)-745-7934')"
    cursor.execute( sql_insert_data_query)
    connection.commit()
    print ("Date Record inserted successfully Branch into tables")
    cursor.close()
    connection.close()
    print("MySQL connection is closed")  

# Warehouse(wh_id, street, city, parish, telephone)
def insertWarehouse(times):
    try:
        connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
        cursor = connection.cursor(prepared=True)
        for _ in range(0,times):
            sql_insert_data_query="INSERT INTO Warehouse(street,city,parish,telephone) VALUES (%s,%s,%s,%s)"
            insert_tuple=(fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber())
            cursor.execute( sql_insert_data_query, insert_tuple)

        connection.commit()
        print ("Date Record inserted successfully into Warehouse table")
    except mysql.connector.Error as error :
        print("Failed inserting date object into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

#WarehouseStock(warehouse_id, model_id, quantity) 
#WarehouseModelItem(warehouse_id, model_id, product_id)
def insertWarehouseStock(times):
    try:
        connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
        cursor = connection.cursor(prepared=True)
        sql_insert_data_query="insert into WarehouseStock(warehouse_id, model_id, quantity) VALUES (%s,%s,%s)"
        sql_insert_data_query2="insert into WarehouseModelItem(warehouse_id, model_id, product_id) VALUES (%s,%s,%s)"
        cursor.execute("SELECT model_id FROM CompuStore.LaptopModel")
        result = cursor.fetchall()

        for i in range(1,times):
            for model_id in result:
                
                modelID=model_id[0].decode()
                quantity = random.randint(250,500)
                
                insert_tuple=(i,modelID,quantity)
                cursor.execute( sql_insert_data_query, insert_tuple)
                
                for _ in range(quantity): 
                    product_id = random.randint(1,2147483647)
                    insert_tuple2=(i,modelID,product_id)
                    cursor.execute( sql_insert_data_query2, insert_tuple2)
                    
        connection.commit()
        print ("Date Record inserted successfully into WarehouseStore and WarehouseModelItem table")
    except mysql.connector.Error as error :
        print("Failed inserting date object into MySQL table {}".format(error))
    finally:
        #closing database connection.
        if(connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")    

if __name__ == '__main__':
    
    insertWarehouseStock(11)
 
 
#--------------------------------not important----------------------------------------------------------------------------------------------------            
# #CustomerAccount(acc_id, email, password, fname, lname, gender, date_of_birth, street, city, parish, telephone, created_on)
# def updateCusAcc(start,end):
#     try:
#       connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
#       cursor = connection.cursor(prepared=True)

#       for i in range(start,end):
#           gen=gender[random.randint(0,1)]
#           sql_insert_data_query=""
#           #sql_insert_data_query="INSERT INTO CustomerAccount(email,password,fname,lname,gender,date_of_birth,street,city,parish,telephone,created_on) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#           if gen=='Male':
#               #insert_tuple=(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_male(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today"))
#               sql_insert_data_query="UPDATE CustomerAccount set email='{}', password ='{}', fname='{}', lname='{}', gender='{}', date_of_birth='{}', street='{}', city='{}', parish='{}', telephone ='{}', created_on='{}' where acc_id ={}".format(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_male(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today"),i)

#           else:
#               #insert_tuple=(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_female(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today") )
#               sql_insert_data_query="UPDATE CustomerAccount set email='{}', password ='{}', fname='{}', lname='{}', gender='{}', date_of_birth='{}', street='{}', city='{}', parish='{}', telephone ='{}', created_on='{}' where acc_id ={}".format(fake.email(),generate_password_hash(fake.password(),"sha256"),fake.first_name_female(),fake.last_name(),gen,fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=50),fake.street_address(),fake.city(),parish[random.randint(0,13)],phoneNumber(),fake.date_between(start_date="-10y", end_date="today"),i)
#           print(sql_insert_data_query)
#           cursor.execute(sql_insert_data_query)

#       connection.commit()
#       print ("Date Record inserted successfully into CustomerAccount table")
#     except mysql.connector.Error as error :
#         print("Failed inserting date object into MySQL table {}".format(error))
#     finally:
#         #closing database connection.
#         if(connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")

#CreditCardDetails(card_num,name_on_card,card_security_code,expiration_month, expiration_year, billing_street, billing_city, billing_parish)
#CustomerCreditCard(acc_id, card_num)
# def insertCard(start,end):
#     try:
#         connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
#         cursor = connection.cursor(prepared=True)
#         for i in range(start,end):
#             # fetching information about customer from CustomerAccount table
#             cursor.execute("SELECT acc_id, fname, lname, street, city, parish FROM CompuStore.CustomerAccount where acc_id={}".format(i))
#             result = cursor.fetchone()
#             name=result[1].decode()+" "+result[2].decode()
#
#             # insert data into the CreditCardDetail table
#             card=cardNum()
#             sql_insert_data_query="INSERT INTO CreditCardDetails(card_num,name_on_card,card_security_code,expiration_month,expiration_year,billing_street,billing_city,billing_parish) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#             insert_tuple=(card,name,cardSC(),fake.month(),year(),result[3].decode(),result[4].decode(),result[5].decode())
#             cursor.execute( sql_insert_data_query,insert_tuple)
#
#             # insert data into the CustomerCreditCard table
#             sql_insert_data_query="INSERT INTO CustomerCreditCard(acc_id,card_num) VALUES (%s,%s)"
#             insert_tuple=(result[0],card)
#             cursor.execute( sql_insert_data_query,insert_tuple)
#
#         connection.commit()
#         print ("Date Record inserted successfully CreditCardDetails and CustomerCreditCard into tables")
#     except mysql.connector.Error as error :
#         print("Failed inserting date object into MySQL table {}".format(error))
#     finally:
#         #closing database connection.
#         if(connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")
#


# def insertBranch(start, end):
#     for i in range(start,end):
#         now = datetime.datetime.now()
#         brid = "'{}'".format(str(i) + str(int(now.microsecond)))
#         p = random.choice(parish)
#         name = "\"{}Branch\"".format(p)
#         address = fake.address()
#         street = address.split(',')[0]+'
#         phone = "'{}'".format(phoneNumber())
#         city = "'{}'".format(fake.city())
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     conn.addRecord([brid, name, street, city, p, phone], "Branch")

#procedure calls
#PROCEDURE for orderByPrice(argument varchar)
# def orderByPrice(ordr):
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     records = conn.orderByPrice(ordr)
#     return records

# '''
# def getByName(name):
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     records = conn.getByName(name)
#     return records
# '''

#PROCEDURE for getByModel(argument varchar)
# def getByModel(model):
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     records = conn.getByModel(model)
#     return records

#PROCEDURE for getByBrand(argument varchar)
# def getByBrand(brand):
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     records = conn.getByBrand(brand)
#     return records

#PROCEDURE for addPurchasedItem(argument int, argument int, argument varchar, argument double )
# def addPurchasedItem(arg1, arg2, arg3, arg4):
#     conn = sqlController.databaseGenerator("CompuStore", sqlController.columns)
#     conn.addPurchasedItem(arg1, arg2, arg3, arg4)

# Laptop(model_num, model, brand, description, thumbnail, price)

# CustomerCart(acc_id, item_count, value)

# CartItems(acc_id, model_id, br_id, quantity, cost,date_added)

# WarehouseStock(wh_id, model_id, quantity) need editing
# def insertWaresStock(start,end):
#     try:
#         connection= mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
#         cursor = connection.cursor(prepared=True)
#         for _ in range(start,end):
#             sql_insert_data_query="INSERT INTO Warehouse(model_id,quantity) VALUES (%s,%s)"
#             insert_tuple=()
#             cursor.execute( sql_insert_data_query, insert_tuple)

#         connection.commit()
#         print ("Date Record inserted successfully into WareStock table")
#     except mysql.connector.Error as error :
#         print("Failed inserting date object into MySQL table {}".format(error))
#     finally:
#         #closing database connection.
#         if(connection.is_connected()):
#             cursor.close()
#             connection.close()
#             print("MySQL connection is closed")

# Receipt(track_num, invoice)

# Checkout(acc_id, track_num, total_cost, transaction_date)

# PurchasedItem(product_id,acc_id,br_id, quantity, cost, date_purchased)

# WriteReview(acc_id,model_id, rev_text, date_written)

#Branches Database
#Laptop(model_id, model, brand, description, thumbnail)
#ModelStockInfo(model_id, amt_in_stock, amt_sold)
#ModelItems(product_id, model_id)

#MultiLink
#CreditCardDetails(card_num, name_on_card, card_security_code, expiration_month, expiration_year, billing_street, billing_city, billing_parish) */


