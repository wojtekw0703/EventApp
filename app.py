from flask import Flask, flash, render_template, request, redirect, url_for, session
import mysql.connector
import bcrypt

app = Flask(__name__)

connection = mysql.connector.connect(
host="localhost",
user="root",
passwd="nowe_haslo",
database="event_app_database"
)

cur = connection.cursor()
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("login.html")

@app.route('/userpage')
def userpage():
    return render_template("home.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and request.form['action'] == "Log in":
        email = request.form['email']
        password = request.form['pass']
        
        cur.execute("SELECT email FROM users WHERE email=%s", (email,))
        result_email = cur.fetchone()
        
        cur.execute("SELECT password FROM users WHERE password=%s", (password,))
        result_password = cur.fetchone()

        if result_email and result_password != None:
            return redirect(url_for('userpage'))
        
        flash("Wrong email or password")
    return render_template('login.html')
    
    

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
            sql = "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)"
            args = (new_user.name,new_user.email,new_user.password)
            cur.execute(sql,args)
            connection.commit()
            flash(u"Successful","success")
    return render_template("register.html")

if __name__ == '__main__':
    app.secret_key = "^A%DEventApp"
    app.run(debug=True)
