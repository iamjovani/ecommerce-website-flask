from flask import Flask, session, redirect, render_template, request, url_for, flash
from forms import SignupForm, LoginForm
from random import sample
from werkzeug.security import check_password_hash,generate_password_hash

import sqlGenerator
import os

app = Flask(__name__)

app.secret_key = "kniajj3m747m2y2378y3h2h8sda"


import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

# connection to the databases
compuStoreConnection = mysql.connector.connect(host="localhost", user="root", password="", database="CompuStore")
compuStoreCursor = compuStoreConnection.cursor(prepared=True)
    
branch1Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch1")
branch1Cursor = branch1Connection.cursor(prepared=True)

branch2Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch2")
branch2Cursor = branch2Connection.cursor(prepared=True)

branch3Connection = mysql.connector.connect(host="localhost", user="root", password="", database="Branch3")
branch3Cursor = branch3Connection.cursor(prepared=True)

MultiLinkConnection = mysql.connector.connect(host="localhost", user="root", password="", database="MultiLink")
MultiLinkCursor = MultiLinkConnection.cursor(prepared=True)

@app.route("/")
def index():
    form = LoginForm()
    compuStoreCursor.execute("SELECT * FROM LaptopModel")
    models = compuStoreCursor.fetchall()
    return render_template("index.html", models=sample(models, 9), form=form)

@app.route("/cart")
def cart():
    form = LoginForm()
    cart_id = session['cart_id']
    compuStoreCursor.execute("SELECT * FROM CartItems c JOIN LaptopModel l on l.model_id = c.model_id  WHERE cart_id = {}".format(cart_id))
    items = compuStoreCursor.fetchall()
    compuStoreCursor.execute("SELECT * FROM ShoppingCart WHERE cart_id = {}".format(cart_id))
    cart = compuStoreCursor.fetchone()
    return render_template("cart.html", cart=cart, items=items, form=form)

@app.route("/account")
def account():
    form = LoginForm()
    compuStoreCursor.execute("SELECT * FROM CustomerAccount where={}".format(session["account_id"]))
    user = compuStoreCursor.fetchone()
    return render_template("index.html",user=user,form=form)
    
@app.route("/checkout")
def checkout():
    form = LoginForm()
    compuStoreCursor.execute("SELECT * FROM CartItems c JOIN LaptopModel l on l.model_id = c.model_id  WHERE cart_id = {}".format(cart_id))
    items = compuStoreCursor.fetchall()
    for i in items:
        branch1Cursor.execute("SELECT amt_in_stock FROM ModelStockInfo WHERE model_id = {}".format(i[1]))
        b1 = (int(branch1Cursor.fetchone()[0]),"b1")
        
        branch2Cursor.execute("SELECT amt_in_stock FROM ModelStockInfo WHERE model_id = {}".format(i[1]))
        b2 = (int(branch2Cursor.fetchone()[0]),"b2")
        
        branch3Cursor.execute("SELECT amt_in_stock FROM ModelStockInfo WHERE model_id = {}".format(i[1]))
        b3 = (int(branch3Cursor.fetchone()[0]),"b3")
        
        m = max([b1,b2,b3])
        if m[1] == "b1":
            for _ in range(m[0]):
                branch1Cursor.execute("call purchaseItem({}, @pid)".format(i[1]))
                branch1Cursor.execute("@pid")
                pid = branch1Cursor.fetchone()
                
        compuStoreCursor.execute("call addPurchasedItem(IN product_id int, IN model_id varchar(100), IN account_id int, IN branch_id varchar(50), IN cost double(20,2))".format(pid, i[1], session["account_id"], ))
                
    return render_template("index.html", models=models, form=form)


@app.route("/product/<model_id>")
def product(model_id):
    form = LoginForm()
    return render_template("product.html",form=form)

@app.route("/add/<model_id>/<quantity>/<price>", methods=["POST"])
def addToCart(model_id, quantity, price):
    form = LoginForm()
    cost = int(quantity) * float(price)
    
    sql_insert_data_query= "INSERT INTO CartItems VALUES ('{}','{}','{}','{}', curdate())".format(session['cart_id'],model_id,int(quantity),cost)
    compuStoreCursor.execute(sql_insert_data_query)
    compuStoreConnection.commit()
    return ""

@app.route("/registration", methods=["GET", "POST"])
def registration():   
    form = LoginForm()
    signform = SignupForm()
    # Signup and validate the user.
 
    if request.method == 'POST':
        if signform.validate_on_submit():
            
            # Query our database to see if the username and password entered
            # match a user that is in the database.
            firstname = signform.firstname.data
            lastname=signform.lastname.data
            email= signform.email.data
            gender= signform.gender.data
            dof= signform.date_of_birth.data
            street= signform.street.data
            city = signform.city.data
            parish= signform.parish.data
            telephone= signform.telephone.data
            password = signform.password.data
            confirmpassword = signform.confirmpassword.data
    
    
            compuStoreCursor.execute("select * from CustomerAccount where email like '{}' limit 1".format(email))
            test = compuStoreCursor.fetchone()

            if test is None :
                sql_insert_data_query= "INSERT INTO CustomerAccount(email,password,fname,lname,gender,date_of_birth,street,city,parish,telephone, created_on) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', curdate())".format(email,generate_password_hash(password,"sha256"),firstname,lastname,gender,dof,street,city,parish,telephone)
                compuStoreCursor.execute(sql_insert_data_query)
                compuStoreConnection.commit()
                
                sql_data_query = ("SELECT account_id FROM CustomerAccount where email like '{}'".format(email))
                compuStoreCursor.execute(sql_data_query)
                user = compuStoreCursor.fetchone()
             
                session["account_id"] = user[0]
                compuStoreCursor.execute("SELECT cart_id FROM CustomerCart where account_id = {} LIMIT 1".format(session["account_id"]))
                cart = compuStoreCursor.fetchone()
                
                session["cart_id"] = cart[0]
                if session["account_id"] == 1:
                    session["type"] = "admin"
                else:
                    session["type"] = "normal"
                    
                flash('Sign-up was successfully.', 'success')
                next_page = request.args.get('next')
    
    
                return redirect(url_for('index'))
    
            else:
                flash("already a member", 'danger')
    return render_template("registration.html", form=form, sform=signform)
        
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        print("work1")
        if form.validate_on_submit():
            print("work2")
            email = form.email.data
            password = form.password.data 

            compuStoreCursor.execute("SELECT account_id, password FROM CustomerAccount where email like '{}' LIMIT 1".format(email))
            user = compuStoreCursor.fetchone()
            print(user)
            if check_password_hash(user[1].decode(), password):
                print("work3")
                session["account_id"] = user[0]
                compuStoreCursor.execute("SELECT cart_id FROM CustomerCart where account_id = {} LIMIT 1".format(user[0]))
                cart = compuStoreCursor.fetchone()
                
                session["cart_id"] = cart[0]
                if session["account_id"] == 1:
                    session["type"] = "admin"
                else:
                    session["type"] = "normal"
                flash('You have logged in successfully.', 'success')
                return redirect(url_for("index"))
    return redirect(url_for("index"))  # they should be redirected to a secure-page route instead

@app.route("/logout")
def logout():
    session.pop('account_id', None)
    session.pop('cart_id', None)
    session.pop('type', None)
    flash('You have been logged out.', 'logout')
    return redirect(url_for('index'))









@app.route("/", methods=["GET", "POST"])
def get_data():
    if request.method == "GET":
        pass # do something
'''
@app.context_processor
def context_processor():
    return dict(name='vale')

'''
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
if __name__ == '__main__':
    app.run()
    app.debug(True)