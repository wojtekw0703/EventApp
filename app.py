from flask import Flask, render_template, request, redirect, url_for, session
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
    def __init__(self, name, email, hash_password):
        self.name = name
        self.email = email
        self.hash_password = hash_password

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        cur.execute("SELECT email FROM users WHERE email=%s", (email,))
        data = cur.fetchone()
        
       
        
        # cursor_email = connection.cursor()
        # cursor_password = connection.cursor()

        # cursor_email.execute(sql_query_email)
        # cursor_password.execute(sql_query_password)

        # records_email = cursor_email.fetchone()
        # records_password = cursor_password.fetchone()

        if data != None:
            return render_template("home.html")
        if data == None:
            return render_template("register.html")
    else:
        return render_template("login.html")
    

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    # else:
    #     name = request.form['name']
    #     email = request.form['email']
    #     password = request.form['password'].encode('utf-8')
    #     hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    #     User(name, email, hash_password)

        
    #     # db_connection.execute("INSERT INTO Users (name, email, password) VALUES (%s,%s,%s)",(User.name,User.email,User.hash_password))
    #     # mysql.connection.commit()
    #     session['name'] = request.form['name']
    #     session['email'] = request.form['email']
    else:
        return redirect("login.html")

if __name__ == '__main__':
    app.secret_key = "^A%DEventApp"
    app.run(debug=True)
