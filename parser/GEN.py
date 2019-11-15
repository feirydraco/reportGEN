import json
import os


class Report():
    def __init__(self, filename, author, subject, keywords):
        self.PATH = os.getcwd()
        self.name = filename
        self.author = author
        self.subject = subject
        self.keywords = "{{{}}}".format(", ".join(keywords))
        self.filepath = os.path.join(
            self.PATH, "latex_dump", filename + ".tex")
        with open(self.filepath, "w+") as file:
            file.write("\\documentclass[12pt, oneside]{report}")
            file.write("\n\\usepackage{color}")
            file.write(""" \
            \n\\usepackage[bookmarks, colorlinks=false, pdfborder={{0 0 0}}, 
            pdftitle={{Report}}, 
            pdfauthor={}, 
            pdfsubject={}, 
            pdfkeywords={}]{{hyperref}}""".format(self.author, self.subject, self.keywords))

    def addpackage(self, package):
        """
            package[0]: string, name of package. #Must be isntalled in TeX.#
            package[1]: extra variables, (usually enclosed in [] brackets in latex)
        """
        with open(self.filepath, "a") as file:
            if type(package).__name__ == "str":
                file.write("\n\\usepackage{{{}}}".format(package))
            else:
                file.write("\n\\usepackage[{}]{{{}}}".format(
                    package[1], package[0]))

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

    def setBaseStyle(self):
        """
        Adds headers and footers as required by RNSIT, as of 2019.
        """
        with open(self.filepath, "a") as file:
            file.write("""\n
\\renewcommand\\bibname{Bibliography}
\\titleformat{\\chapter}[display]
  {\\normalfont\\Large\\bfseries}{\\filright\\chaptertitlename\\ \\thechapter}
  {20pt}{\LARGE\filcenter}
\\setlength{\\headheight}{25pt}

\\renewcommand{\\headrulewidth}{5pt}
\\renewcommand{\\footrulewidth}{5pt}
\\renewcommand{\\headrule}{\\hbox to\\headwidth{\\color{darkbrown}\\leaders\\hrule height \\headrulewidth\\hfill}}
\\renewcommand{\\footrule}{\\hbox to\\headwidth{\\color{darkbrown}\\leaders\\hrule height \\footrulewidth\\hfill}}

\\fancyhf{}

\\fancyhead[L]{\\thechapter}
\\fancyhead[R]{\\nouppercase{\\rightmark}}
\\fancyfoot[L]{RNSIT, Dept. of CSE}
\\fancyfoot[C]{2019-20}
\\fancyfoot[R]{Page \\thepage}

\\renewcommand{\\contentsname}{\\centering Contents}

\\AtBeginDocument{%
  \\addtocontents{toc}{\\protect\\thispagestyle{empty}}%
  \\addtocontents{lof}{\\protect\\thispagestyle{empty}}%
}

\\fancypagestyle{plain}{%
  \\fancyhf{}
  \\fancyhead[L]{}
  \\fancyhead[R]{}
  \\renewcommand{\headrulewidth}{0pt}% Line at the header 
  \\fancyfoot[L]{RNSIT, Dept. of CSE}
  \\fancyfoot[C]{2019-20}
  \\fancyfoot[R]{Page \\thepage}
}
""")


if __name__ == "__main__":
    report = Report("report", "Yash", "Web", ("Scripting", "Python", "Flask"))

    packages = ["xcolor", "tikz", "multicol", "titletoc", "ragged2e",
                "fancyhdr", "url", "verbatim", "float", "titlesec", "listings", "mathptmx", (
                    "inputenc", "utf8"),
                "adjustbox", "titlesec", "tabularx"]

    report.add_packages(packages)
    report.defineColor("darkbrown", (128, 0, 0))
    report.defineColor("blue", (0, 51, 204))
    report.defineColor("black", (0, 0, 0))

    report.setGeometry()

    report.set_linespread(1.3)

    report.setBaseStyle()
