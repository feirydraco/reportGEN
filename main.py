from flask import Flask, render_template, make_response
from pylatex import *

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/generate")
def compile():
    return render_template("base.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    
if __name__ == "__main__":
    app.run(debug=True)
