from flask import Flask, flash, render_template, request, redirect, url_for, session
from db import mysql
import pymysql
from app import app
conn = mysql.connect()
cur = conn.cursor(pymysql.cursors.DictCursor)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@app.route('/')
def start():
    return render_template("index.html")

@app.route('/userpage')
def userpage():
    return render_template("userpage.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and request.form['action'] == "Login":
        email = request.form['email']
        password = request.form['pass']
        
        cur.execute("SELECT email FROM users WHERE email=%s", (email,))
        result_email = cur.fetchone()
        
        cur.execute("SELECT password FROM users WHERE password=%s", (password,))
        result_password = cur.fetchone()
        
        if result_email and result_password != None:
            return redirect(url_for('userpage'))
            cur.close()
            conn.close()
        
        flash("Wrong email or password","danger")
    return render_template('index.html')
    
    

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST' and request.form['action'] == "Sign up":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name,email,password)
        if name == "" or email == "" or password == "":
            flash(u"Complete all fields","danger")
        else:
            email = request.form['email']
            password = request.form['password']
        
            cur.execute("SELECT email FROM users WHERE email=%s", (email,))
            result_email = cur.fetchone()
        
            cur.execute("SELECT password FROM users WHERE password=%s", (password,))
            result_password = cur.fetchone()

            if result_email and result_password != None:
                flash(u"An account already exists","danger")
                return render_template('index.html')
            else:
                sql = "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)"
                args = (new_user.name,new_user.email,new_user.password)
                cur.execute(sql,args)
                cur.close()
                conn.close()

                flash(u"Your account has been created. Sign in now","success")
    return render_template('index.html')
    

if __name__ == '__main__':
    app.secret_key = "^A%DEventApp"
    app.run(debug=True)
