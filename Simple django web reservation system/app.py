from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("SKJ rezervace")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ockovani.db"
app.secret_key = b"_5#y2LF4Q8z\n\xec]/"

db = SQLAlchemy(app)
