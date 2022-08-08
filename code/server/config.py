import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app
CORS(app)

# Build the ULR for SqlAlchemy
dbase_url = "mysql://root:root@127.0.0.1:3307/handball_dbase"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = dbase_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize my_conn
ma = Marshmallow(app)
connection = db.engine.connect()
