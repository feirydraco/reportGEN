from flask import Flask, render_template, request, redirect, url_for, jsonify
from jinja2 import Template
import os
import json
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = './static'


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/ref")
def bibliography():
    references = json.load(open("./parser/report.json", "r"))['ref']
    return render_template("ref.html", refs=references)


@app.route("/addref", methods=["POST"])
def addref():
    data = request.form.to_dict()
    json_file = json.load(open("./parser/report.json", "r"))

    json_file['ref'].append(
        {"caption": data['caption'], "link": data['link']})

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return redirect(url_for("bibliography"))


@app.route("/deleteref/<string:caption>")
def deleteref(caption):
    json_file = json.load(open("./parser/report.json", "r"))
    for item in json_file['ref']:
        if item['caption'] == caption:
            json_file['ref'].remove(item)
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return redirect(url_for("bibliography"))

# @app.route("/chapters/<target>/<int:selector>", methods=["GET", "POST"])
# def chapters(target, selector):
#     if request.method == "GET":
#         if target == "remove":
#             json_file = json.load(open("./parser/report.json", "r+"))
#             for chapter in json_file['chapters']:
#                 if chapter['number'] == selector:
#                     json_file['chapters'].remove(chapter)
#             with open("./parser/report.json", "w") as f:
#                 json.dump(json_file, f)

#         json_file = json.load(open("./parser/report.json", "r"))
#         return render_template("chapters.html", data=json_file)
#     if request.method == "POST":
#         print(target)
#         response = request.form.to_dict()
#         json_file = json.load(open("./parser/report.json", "r+"))
#         if target == "add":
#             n = len(json_file['chapters']) + 1
#             json_file['chapters'].append({"name": response['message'], "number": n, "content": []})
#         if target == "addcontent":
#             for chapter in json_file['chapters']:
#                 if chapter['number'] == selector:
#                     chapter['content'] = response['message']

#         print(json_file['chapters'])
#         with open("./parser/report.json", "w") as f:
#             json.dump(json_file, f)

    json_file = json.load(open("./parser/report.json", "r"))
    return render_template("chapters.html", data=json_file)


@app.route("/generate")
def home():
    os.chdir('parser')
    # os.system("python3 GEN.py >/dev/null 2>&1")
    os.system("python3 GEN.py")
    os.chdir('..')
    json_file = json.load(open("./parser/report.json", "r"))
    return render_template("index.html", data=json_file)


@app.route("/add_student")
def add_student():
    json_file = json.load(open("./parser/report.json", "r"))
    students = json_file['coverpage']['title']['students']['members']
    if len(students) <= 4:
        students.append({"Name": "", "USN": ""})
        with open("./parser/report.json", "w") as f:
            json.dump(json_file, f)
    return redirect(url_for('/cover'))


@app.route("/delete/<string:instance>/<int:pos>")
def delete(instance, pos):
    json_file = json.load(open("./parser/report.json", "r"))

    if instance == "student":
        students = json_file['coverpage']['title']['students']['members']
        students[pos] = {"Name": "", "USN": ""}
        tab = "title"
    elif instance == "teacher":
        teachers = json_file['coverpage']['title']['teachers']['members']
        teachers[pos] = {"Name": "", "Designation": "", "Department": ""}
        tab = "title"
    elif instance == "guide":
        teachers = json_file['coverpage']['certificate']['members']
        teachers[pos] = {"Name": "", "Designation": "", "Department": ""}
        tab = "certificate"
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    coverpage = json.load(open("./parser/report.json", "r"))['coverpage']
    return render_template("cover.html", coverpage=coverpage, tab=tab)


@app.route("/chapters")
def chapters():
    chapters = json.load(open("./parser/report.json", "r"))['chapters']
    return render_template("chapters.html", chapters=chapters)


@app.route("/chapter/<int:chapnum>")
def chapter(chapnum):
    chapter = json.load(open("./parser/report.json", "r")
                        )['chapters'][chapnum - 1]
    return render_template("chapter.html", chapter=chapter)


@app.route("/addchapter")
def add_chapter():
    json_file = json.load(open("./parser/report.json", "r"))
    num_of_chapters = len(json_file['chapters'])

    json_file['chapters'].append({
        'name': request.args.get('newchapter'),
        'number': num_of_chapters + 1,
        'content': []
    })
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect(url_for("chapters"))


@app.route("/deletechapter/<int:chapternum>")
def delete_chapter(chapternum):
    x = 0
    json_file = json.load(open("./parser/report.json", "r"))

    for chapter in json_file['chapters']:
        if chapter['number'] == chapternum:
            x = chapter['number']
            json_file['chapters'].remove(chapter)
            break

    for chapter in json_file['chapters']:
        if chapter['number'] > x:
            chapter['number'] -= 1

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect(url_for("chapters"))


@app.route("/deletecontent/<int:chapternum>/<int:contentnum>")
def delete_content(chapternum, contentnum):
    json_file = json.load(open("./parser/report.json", "r"))
    for part in json_file['chapters'][chapternum - 1]['content']:
        if part['id'] == contentnum:
            json_file['chapters'][chapternum - 1]['content'].remove(part)
    i = 1
    for part in json_file['chapters'][chapternum - 1]['content']:
        part['id'] = i
        i += 1

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect("/chapter/{}".format(chapternum))


@app.route("/savechapter/<int:chapternum>", methods=["POST"])
def save_chapter(chapternum):
    json_file = json.load(open("./parser/report.json", "r"))
    print(request.form.to_dict().items())
    for inp, val in request.form.to_dict().items():
        json_file['chapters'][chapternum -
                              1]['content'][int(inp) - 1]['content'] = val

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect("/chapter/{}".format(chapternum))


@app.route("/addtext/chapter<int:chapternum>")
def addtext(chapternum):
    json_file = json.load(open("./parser/report.json", "r"))
    json_file['chapters'][chapternum - 1]['content'].append({'type': 'text', 'id': len(
        json_file['chapters'][chapternum - 1]['content']) + 1, 'content': ''})

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect("/chapter/{}".format(chapternum))


@app.route("/addimage/chapter<int:chapternum>")
def addimage(chapternum):
    json_file = json.load(open("./parser/report.json", "r"))

    json_file['chapters'][chapternum - 1]['content'].append({'type': 'image', 'id': len(
        json_file['chapters'][chapternum - 1]['content']) + 1, 'content': ''})

    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)

    return redirect("/chapter/{}".format(chapternum))


@app.route("/addtable/<int:chapternum>")
def addtable(chapternum):
    pass
    return redirect('/chapter/{}'.format(chapternum))


@app.route("/cover")
def coverpage():
    coverpage = json.load(open("./parser/report.json", "r"))['coverpage']
    return render_template("cover.html", coverpage=coverpage, tab="title")


@app.route("/addabstract", methods=["POST"])
def addabstract():
    json_file = json.load(open("./parser/report.json", "r"))
    coverpage = json_file['coverpage']
    response = request.form.to_dict()
    coverpage['abstract']['content'] = response['abstract']
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return render_template("cover.html", coverpage=coverpage, tab="abstract")


@app.route("/addack", methods=["POST"])
def addack():
    json_file = json.load(open("./parser/report.json", "r"))
    coverpage = json_file['coverpage']
    response = request.form.to_dict()
    coverpage['acknowledgements']['content'] = response['acknowledgements']
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return render_template("cover.html", coverpage=coverpage, tab="acknowledgements")


@app.route("/addcertificate", methods=["POST"])
def addCertificate():
    json_file = json.load(open("./parser/report.json", "r"))
    coverpage = json_file['coverpage']
    for it, val in request.args.items():
        if "tname" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['certificate']['members'][pos]["Name"] = val
        if "tdesignation" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['certificate']['members'][pos]["Designation"] = val
        if "tdepartment" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['certificate']['members'][pos]["Department"] = val
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return render_template("cover.html", coverpage=coverpage, tab="certificate")


@app.route("/addtitle", methods=["GET", "POST"])
def addtitle():
    json_file = json.load(open("./parser/report.json", "r"))
    coverpage = json_file['coverpage']
    coverpage['title']['subject']['topic'] = request.args.get('topic')
    coverpage['title']['subject']['title'] = request.args.get('title')
    coverpage['title']['subject']['semester'] = request.args.get('semester')

    for it, val in request.args.items():
        if "sname" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['title']['students']['members'][pos]["Name"] = val
        if "susn" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['title']['students']['members'][pos]["USN"] = val
        if "tname" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['title']['teachers']['members'][pos]["Name"] = val
        if "tdesignation" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['title']['teachers']['members'][pos]["Designation"] = val
        if "tdepartment" in it:
            if val is not "":
                pos = int(it[-1:])
                coverpage['title']['teachers']['members'][pos]["Department"] = val
    with open("./parser/report.json", "w") as f:
        json.dump(json_file, f)
    return render_template("cover.html", coverpage=coverpage, tab="title")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
