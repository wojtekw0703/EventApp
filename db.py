from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b7876263fb4ab0'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ef019fb3'
app.config['MYSQL_DATABASE_DB'] = 'heroku_e8e06c5096341cd'
app.config['MYSQL_DATABASE_HOST'] = 'eu-cdbr-west-03.cleardb.net'
mysql.init_app(app)