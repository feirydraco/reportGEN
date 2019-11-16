import json
import os
import re


class Report():
    def __init__(self, filename, subject, keywords):
        self.PATH = os.getcwd()
        self.name = filename

        self.authors = "{latexGEN}"

        self.titlepath = os.path.join(
            os.getcwd(), "latex_dump", "cover", "title.tex")
        print(self.titlepath)
        self.subject = subject
        self.keywords = "{{{}}}".format(", ".join(keywords))
        self.filepath = os.path.join(
            self.PATH, "latex_dump", filename + ".tex")
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

    def addpackage(self, package):
        """
            package: string, name of package. #Must be isntalled in TeX.#
        """
        with open(self.filepath, "a") as file:
            file.write("\n\\usepackage{{{}}}".format(package))

    def defineColor(self, colorname, RGB):
        """
        colorname: user-defined colorname.
        RGB: integer tuple values in form of (R, G, B)

        #TODO: only do this if "color" package is installed.
        """
        with open(self.filepath, "a") as file:
            file.write("\n\\definecolor{{{}}}{{RGB}}{{{}, {}, {}}}".format(
                colorname, RGB[0], RGB[1], RGB[2]))
            print("Defining color:", colorname, RGB)

    def add_packages(self, packages):
        """
        packages: list of packages to be set up for report. #Must be isntalled in TeX.#
        """

        print("Adding {} packages.".format(len(packages)))

        for package_name in packages:
            print("Adding:", package_name, type(package_name))
            self.addpackage(package_name)
            # package name can have multiple formats for adding different kinds of packages.

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

    def addTitlePage(self, students, teachers):
        """
        Creates the title page, expects members to be present in self.authors;
        students: a list consisting of upto four strings for student names.
        teachers: a list consisting of upto three strings for teacher names.
        """
        edit = None
        with open("./static/titlepage.txt", "r") as titlepage:
            with open(self.titlepath, "w+") as texfile:
                for line in titlepage.readlines():
                    if edit is not None:
                        if edit == "student":
                            texfile.write("\\begin{tabular}{l l}")
                            for student in students['members']:
                                print("Writing:",
                                      student["Name"], student["USN"])
                                texfile.write("\n\\textcolor{{blue}}{{\\textbf{{{}}}}} & \\textcolor{{blue}}{{\\hspace{{2.7cm}}\\textbf{{{}}}}}\\\ \
".format(student["Name"], student["USN"]))
                            edit = None

                        elif edit == "teacher":
                            texfile.write(
                                "\\begin{tabularx}{\\linewidth}{" + "X " * len(teachers['members']) + "}")
                            # patched to not write "&" because it messes it up.
                            cur_t = 0
                            for teacher in teachers['members']:
                                print(
                                    "Writing:", teacher["Name"], teacher["Designation"], teacher["Department"])
                                texfile.write("\n\\textbf{{{}}}\\linebreak\\textbf{{{}}}\\linebreak\\textbf{{{}}}\\linebreak ".format(
                                    teacher["Name"], teacher["Designation"], teacher["Department"]))
                                if cur_t != len(teachers['members']) - 1:
                                    texfile.write("& ")
                                cur_t += 1
                            edit = None
                    else:
                        if "\\begin{tabular}{l l}" in line:
                            edit = "student"
                            continue
                        elif "\\begin{tabularx}{\\linewidth}{X X X}" in line:
                            edit = "teacher"
                            continue
                        else:
                            texfile.write(line)
        with open(self.filepath, "a") as file:
            file.write("\n\\input{./cover/title.tex}")

    def mainContent(self, state):
        with open(self.filepath, "a") as file:
            if state:
                file.write("\n\\begin{document}")
            else:
                file.write("\n\\end{document}")

    def setBaseStyle(self):
        """
        Adds headers and footers as required by RNSIT, as of 2019.
        """
        with open(self.filepath, "a") as file:
            file.write("".join(open("./static/config.txt", "r")))

    def generate(self):
        os.chdir("./latex_dump/")
        print(os.getcwd())
        print(os.listdir())
        os.system("pdflatex {}.tex".format(self.name))


if __name__ == "__main__":
    report = Report("report", "Web", ("Scripting", "Python", "Flask"))

    packages = json.load(open("./json_dump/packages.json"))['packages']
    report.add_packages(packages)

    colors = json.load(open("./json_dump/colors.json"))['colors']
    print(colors)
    for color in colors:
        report.defineColor(color['colorname'], color['RGB'])

    report.setGeometry()  # left, right, bot, top (inches)

    report.set_linespread(1.3)

    report.setBaseStyle()

    report.mainContent(True)

    students = json.load(open("./json_dump/titlepage.json"))['students']
    teachers = json.load(open("./json_dump/titlepage.json"))['teachers']

    report.addTitlePage(students, teachers)

    report.mainContent(False)

    report.generate()
