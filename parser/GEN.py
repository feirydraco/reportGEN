import json
import os

def processText(text):
    orig_text = text
    start_marker = text.find("**")
    while(text.find("**") != -1):
        if start_marker != -1:
            text = text.replace("**", "\\textbf{", 1)
            end_marker = text.find("**", start_marker)
            if end_marker == -1:
                print("To be implemented.")
            else:
                text = text.replace("**", "}", 1)
                orig_text = text 
    # print(text)
    return text


class Report():

    def __init__(self, filename, subject, keywords):

        self.PATH = os.getcwd()
        self.name = filename
        
        self.authors = "{latexGEN}"
        self.subject = subject
        self.keywords = "{{{}}}".format(", ".join(keywords))

        self.title = os.path.join(
            os.getcwd(), "latex_dump", "title.tex")
        self.certificate = os.path.join(
            os.getcwd(), "latex_dump", "certificate.tex")
        self.ack = os.path.join(os.getcwd(), "latex_dump", "ack.tex")
        self.abstract = os.path.join(os.getcwd(), "latex_dump", "abstract.tex")

        self.students = []

        self.filepath = os.path.join(self.PATH, "latex_dump", filename + ".tex")
        self.data = json.load(open(os.path.join(os.getcwd(), "report.json"), "r"))

        for member in self.data['title']['teachers']['members']:
            if member["Name"] == "" and member["Designation"] == "" and member["Department"] == "":
                self.data['title']['teachers']['members'].remove(member)

        with open(self.filepath, "w+") as file:
            file.write("\\documentclass[12pt, oneside]{report}")
            file.write("\n\\usepackage{color}")
            file.write("\n\\usepackage[utf8]{inputenc}")
            file.write(""" \
            \n\\usepackage[bookmarks, colorlinks=false, pdfborder={{0 0 0}}, 
            pdftitle={{Report}}, 
            pdfauthor={}, 
            pdfsubject={{{}}}, 
            pdfkeywords=[{}]{{hyperref}}""".format(self.authors, self.subject, self.keywords))
        
        if self.data['modifications']['packages'] is not None:
            self.add_packages((self.data['modifications']['packages']))
        if self.data['modifications']['colors'] is not None:
            self.defineColors((self.data['modifications']['colors']))
        self.setGeometry()
        self.set_linespread(1.3)
        with open(self.filepath, "a") as report:
            config = open("./static/config.txt", "r").read()
            report.write(config)

    def addpackage(self, package):
        """
            package: string, name of package. #Must be isntalled in TeX.#
        """
        with open(self.filepath, "a") as file:
            file.write("\n\\usepackage{{{}}}".format(package))

    def add_packages(self, packages):
            """
            packages: list of packages to be set up for report. #Must be isntalled in TeX.#
            """

            print("Adding {} packages.".format(len(packages)))

            for package_name in packages:
                self.addpackage(package_name)
                # package name can have multiple formats for adding different kinds of packages.

    def defineColors(self, colors):
        """
        colors: {
            colorname: user-defined colorname.
            RGB: integer tuple values in form of (R, G, B)
        }
        """
        with open(self.filepath, "a") as file:
            for i in range(len(self.data['modifications']['colors'])):
                file.write("\n\\definecolor{{{}}}{{RGB}}{{{}, {}, {}}}".format(
                    colors[i]["colorname"], colors[i]["RGB"][0], colors[i]["RGB"][1], colors[i]["RGB"][2]))
                    
    def setGeometry(self, lmargin=1.25, rmargin=1.0, top=0.75, bottom=0.75):
        """
        sets geometry of margins.
        """
        with open(self.filepath, "a") as file:
            file.write("\n\\usepackage{geometry}")
            file.write("""\n\\geometry{{
            lmargin = {}in,
            rmargin = {}in,
            top = {}in, 
            right = {}in,
            }}""".format(lmargin, rmargin, top, bottom))

    def set_linespread(self, linespread):
        """
        linespread: not the same as MS WORD.
        """
        with open(self.filepath, "a") as file:
            file.write("\n\\linespread{{{}}}".format(linespread))
    
    def MainContent(self, start):
        with open(self.filepath, "a") as file:
            if start:
                file.write("\n\\begin{document}")
            else:
                file.write("\n\\end{document}")
    
    def replaceTag(self, pattern, text, content):
        if text.find(pattern) != -1:
            text = text.replace(pattern, content)
        return text

    def format_horizontal(self, members):
        val = []

        num = len(members)
        
        for member in members:

            text = "\n\\textbf{{{}}}\\linebreak\\textbf{{{}}}\\linebreak\\textbf{{{}}}\\linebreak".format(member['Name'], member['Designation'], member['Department'])
            if num > 1:
                text += " &"
                num -= 1
            val.append(text)
        return ''.join(val)

    def format_vertical(self, members):
        val = []
        for member in members:
            val.append("\n\\textcolor{{blue}}{{\\textbf{{{}}}}} & \\textcolor{{blue}}{{\\hspace{{2.5cm}}\\textbf{{{}}}}}\\\\".format(member['Name'], member['USN']))     
        return ''.join(val)

    def formatStudentData(self, members):
        text = ""
        num = len(members)
        for member in members:
            if member['Name'] == "" and member['USN'] == "":
                num -= 1
                continue
            else:
                num -= 1
                text += "\\textbf{{{}}} bearing USN \\textbf{{{}}}".format(member['Name'], member['USN'])
                if num > 0:
                    text += ";  "
                    num -= 1
        return text

    def formatAck(self, data):
        students = []
        
        for member in data:
            if member['Name'] != "" and member['USN'] != "":
                students.append(member)
        # print(students)
        n = len(students)
        for _ in range(4 - n):
            students.append({'Name': "", 'USN': ""})
        
        return " & {{\\hfill}}\\textup{{{} {}}}\\\\ \n  & {{\\hfill}}\\textup{{{} {}}}\\\\ \n \\textup{{Date:}} & {{\\hfill}}\\textup{{{} {}}}\\\\\n\\textup{{Place:}} & {{\\hfill}}\\textup{{{} {}}}\\\\".format(students[3]['Name'], students[3]['USN'], students[2]['Name'], students[2]['USN'], students[1]['Name'], students[1]['USN'], students[0]['Name'], students[0]['USN'])



    def addTitle(self):
        with open("./static/titlepage.tex", "r") as title:
            with open(self.title, "w+") as titlepage:
                for line in title:
                    line = self.replaceTag("<TOPIC>", line, self.data['title']['subject']['topic'])
                    line = self.replaceTag("<TITLE>", line, self.data['title']['subject']['title'])
                    line = self.replaceTag("<SEMESTER>", line, self.data['title']['subject']['semester'])
                    line = self.replaceTag("<STUDENTS>", line, self.format_vertical(self.data['title']['students']['members']))
                    line = self.replaceTag("<TEACHERS>", line, self.format_horizontal(self.data['title']['teachers']['members']))
                    line = self.replaceTag("<NUM_TEACHERS>", line, "X " * len(self.data['title']['teachers']['members']))
                    titlepage.write(line)
        with open(self.filepath, "a") as report:
            report.write("\n\\include{./title}\n")

    def addCertificate(self):
        with open("./static/certificate.tex", "r") as certificate:
            with open(self.certificate, "w+") as certificatepage:
                for line in certificate:
                    line = self.replaceTag("<TITLE>", line, self.data['title']['subject']['title'])
                    line = self.replaceTag("<TOPIC>", line, self.data['title']['subject']['topic'])
                    line = self.replaceTag("<SEMESTER>", line, self.data['title']['subject']['semester'])
                    line = self.replaceTag("<GUIDES>", line, self.format_horizontal(self.data['certificate']['Guides']))
                    line = self.replaceTag("<NUM_GUIDES>", line, "X " * len(self.data['certificate']['Guides']))
                    line = self.replaceTag("<STUDENTS>", line, self.formatStudentData(self.data['title']['students']['members']))

                    certificatepage.write(line)
        with open(self.filepath, "a") as report:
            report.write("\n\\include{./certificate}\n")
    
    def addAck(self):
        with open("./static/ack.tex", "r") as ack:
            with open(self.ack, "w+") as ackpage:
                for line in ack:
                    line = self.replaceTag("<CONTENT>", line, processText(self.data['ack']['content']))
                    line = self.replaceTag("<STUDENT>", line, self.formatAck(self.data['title']['students']['members']))
                    ackpage.write(line)
        with open(self.filepath, "a") as report:
            report.write("\n\\include{./ack}\n")
    
    def addAbstract(self):
        with open("./static/abstract.tex", "r") as abstract:
            with open(self.abstract, "w+") as abstractpage:
                for line in abstract:
                    line = self.replaceTag("<CONTENT>", line, processText(self.data['abstract']['content']))
                    abstractpage.write(line)
        with open(self.filepath, "a") as report:
            report.write("\n\\include{./abstract}\n")

    def generate(self):
            os.chdir("./latex_dump/")
            os.system("pdflatex {}.tex".format(self.name))
            # os.system("rm ./../../static/report.pdf")
            os.system("cp -R report.pdf ./../../static/report.pdf")


if __name__ == "__main__":
    report = Report("report", "Web", ("Scripting", "Python", "Flask"))
    report.MainContent(True)
    report.addTitle()
    report.addCertificate()
    report.addAck()
    report.addAbstract()
    report.MainContent(False)
    report.generate()

