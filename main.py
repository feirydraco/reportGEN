from flask import Flask, render_template, make_response, redirect, request
import os
import json
from parser.GEN import Report


app = Flask(__name__)
json_file = json.load(open("./parser/report.json", "r+"))
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0




@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/generate")
def home():
    global json_file
    os.chdir('parser')
    os.system("python3 GEN.py >/dev/null 2>&1")
    os.chdir('..')
    json_file = json.load(open("./parser/report.json", "r+"))
    return render_template("content.html", data=json_file)

@app.route("/content", methods=["GET","POST"])
def editCoverPage():
    if request.method == "POST":
        print(request.form.to_dict())
        json_file['title']['subject'] = request.form.to_dict()
        json.dump(json_file, open("./parser/report.json", "w+"))
        
        return render_template("content.html", data=json_file)
    
    return render_template("content.html", data=json_file)

if __name__ == "__main__":
    app.run(debug=True)
