from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)    # create a Flask WSGI application
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:isak@localhost/moviedb' # database (ORM) configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'AJHD@*$&JHAHK#&*@*JH$#'
db = SQLAlchemy(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False