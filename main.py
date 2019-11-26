from flask import Flask, render_template, make_response, redirect, request
import os
import json
from parser.GEN import Report

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/generate")
def home():

    os.chdir('parser')
    # os.system("python3 GEN.py >/dev/null 2>&1")
    os.system("python3 GEN.py")
    os.chdir('..')
    json_file = json.load(open("./parser/report.json", "r"))
    return render_template("content.html", data=json_file)


@app.route("/content/<edit>", methods=["GET", "POST"])
def editCoverPage(edit):

    if request.method == "GET":
        pass
    if request.method == "POST":
        response = request.form.to_dict()
        json_file = json.load(open("./parser/report.json", "r+"))
        if edit == "title":
            print(response)
            json_file['title']['subject']['topic'] = response['topic']
            json_file['title']['subject']['title'] = response['title']
            json_file['title']['subject']['semester'] = response['semester']

            json_file['title']['students']['members'][0]['Name'] = response['name0']
            json_file['title']['students']['members'][0]['USN'] = response['usn0']

            json_file['title']['students']['members'][1]['Name'] = response['name1']
            json_file['title']['students']['members'][1]['USN'] = response['usn1']

            json_file['title']['students']['members'][2]['Name'] = response['name2']
            json_file['title']['students']['members'][2]['USN'] = response['usn2']

            json_file['title']['students']['members'][3]['Name'] = response['name3']
            json_file['title']['students']['members'][3]['USN'] = response['usn3']
    
            json_file['title']['teachers']['members'][0]['Name'] = response['n0']
            json_file['title']['teachers']['members'][0]['Designation'] = response['d0']
            json_file['title']['teachers']['members'][0]['Department'] = response['g0']

            json_file['title']['teachers']['members'][1]['Name'] = response['n1']
            json_file['title']['teachers']['members'][1]['Designation'] = response['d1']
            json_file['title']['teachers']['members'][1]['Department'] = response['g1']

            json_file['title']['teachers']['members'][2]['Name'] = response['n2']
            json_file['title']['teachers']['members'][2]['Designation'] = response['d2']
            json_file['title']['teachers']['members'][2]['Department'] = response['g2']

        elif edit == "certificate":
            print(response)
            json_file['certificate']['Guides'][0]['Name'] = response['n0']
            json_file['certificate']['Guides'][0]['Designation'] = response['d0']
            json_file['certificate']['Guides'][0]['Department'] = response['g0']

            json_file['certificate']['Guides'][1]['Name'] = response['n1']
            json_file['certificate']['Guides'][1]['Designation'] = response['d1']
            json_file['certificate']['Guides'][1]['Department'] = response['g1']
        elif edit == "ack":
            print(response['message'])
            json_file['ack']['content'] = response['message']
    
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return render_template("content.html", data=json_file)  


if __name__ == "__main__":
    app.run(debug=True)
