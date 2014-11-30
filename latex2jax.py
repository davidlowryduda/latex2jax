# latex2jax

import re
from sys import argv

# list of theorem-like environments
ThmEnvs = [
    "theorem",
    "definition",
    "lemma",
    "proposition",
    "corollary",
    "claim",
    "remark",
    "example",
    "exercise"
]

fontstyle = {
  r'{\em ' : 'em',
  r'{\bf ' : 'b',
  r'{\it ' : 'i',
  r'{\sl ' : 'i',
  r'\textit{' : 'i',
  r'\textsl{' : 'i',
  r'\emph{' : 'em',
  r'\textbf{' : 'b',
}

esc = [
    ["\\$","_dollar_","&#36;","\\$"],
    ["\\%","_percent_","&#37;","\\%"],
    ["\\&","_amp_","&amp;","\\&"],
    [">","_greater_",">","&gt;"],
    ["<","_lesser_","<","&lt;"]
]

Mnomath =[
    ["\\\\","<br/>\n"],
    ["\\ "," "],
    ["\\`a","&agrave;"],
    ["\\'a","&aacute;"],
    ["\\\"a","&auml;"],
    ["\\aa ","&aring;"],
    ["{\\aa}","&aring;"],
    ["\\`e","&egrave;"],
    ["\\'e","&eacute;"],
    ["\\\"e","&euml;"],
    ["\\`i","&igrave;"],
    ["\\'i","&iacute;"],
    ["\\\"i","&iuml;"],
    ["\\`o","&ograve;"],
    ["\\'o","&oacute;"],
    ["\\\"o","&ouml;"],
    ["\\`o","&ograve;"],
    ["\\'o","&oacute;"],
    ["\\\"o","&ouml;"],
    ["\\H o","&ouml;"],
    ["\\`u","&ugrave;"],
    ["\\'u","&uacute;"],
    ["\\\"u","&uuml;"],
    ["\\`u","&ugrave;"],
    ["\\'u","&uacute;"],
    ["\\\"u","&uuml;"],
    ["\\v{C}","&#268;"]
]

def clean_whitespace(textbody):
    """Removes excess whitespaces"""
    pass
    #begin_re = re.compile(r"\\begin\s*")
    #end_re = re.compile(r"\\end\s*")
    #return

def extract_title(textbody):
    """
    Returns the title of the .tex file, assuming that the
    title is set in \title{TITLE}. Otherwise, returns "TITLE"
    """
    title_re = re.compile(r"^\s*\\title{([^}]*)}", re.MULTILINE)
    title = title_re.findall(textbody)
    if title:
        return title[0]
    return "TITLE"

def main():
    inputfile = "input.tex"
    outputfile = "output.html"
    if len(argv) > 1 :
        inputfile = argv[1]
        if len(argv) > 2 :
            outputfile = argv[2]
    f = open(inputfile)
    s = f.read()
    f.close()

    title = extract_title(s)
    print title


if __name__=="__main__":
    main()
