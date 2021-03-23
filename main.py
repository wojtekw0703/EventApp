from flask import Flask, flash, render_template, request, redirect, url_for, session
import mysql.connector


app = Flask(__name__)

app.secret_key = 'your secret key'


conn = mysql.connector.connect(
host="localhost",
user="root",
passwd="nowe_haslo",
database="event_app_database"
)

cur = conn.cursor(buffered=True)

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

@app.route('/')
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST' and request.form['action'] == "Login":
        email = request.form['email']
        password = request.form['pass']
        
        conn.ping()
        cur.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password,))
        account = cur.fetchone()
        conn.ping()
        
        if account:
            # global session
            session['loggedin'] = True
            session['id'] = account[0]
            session['email'] = account[1]
            return render_template('profile.html', account=account)
        else:
             flash("Wrong email or password","danger")
    return render_template('index.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))
    
    

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
            
            conn.ping() 
            cur.execute("SELECT email FROM users WHERE email=%s", (email,))
            result_email = cur.fetchone()
            
            conn.ping()     
            cur.execute("SELECT password FROM users WHERE password=%s", (password,))
            result_password = cur.fetchone()

            if result_email and result_password != None:
                flash(u"An account already exists","danger")
                return render_template('index.html')
            else:
                sql = "INSERT INTO users (name, email, password) VALUES (%s,%s,%s)"
                conn.ping()  # reconnecting mysql
                args = (new_user.name,new_user.email,new_user.password)
                cur.execute(sql,args)
                conn.commit()

                flash(u"Your account has been created. Sign in now","success")
    return render_template('index.html')


    

if __name__ == '__main__':
    app.secret_key = "^A%DEventApp"
    app.run(debug=True)
