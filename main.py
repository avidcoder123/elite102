import db
import functions as f
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return "<h1>Hello 123</h1>"