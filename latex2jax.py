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

def clean_whitespace(textbody):
    """Removes excess whitespaces and comments"""
    comment_re = re.compile("%.*?$", re.MULTILINE)
    textbody = comment_re.sub("", textbody)

    begin_re = re.compile(r"\\begin\s*")
    textbody = begin_re.sub(r"\\begin", textbody)

    end_re = re.compile(r"\\end\s*")
    textbody = end_re.sub(r"\\end", textbody)

    multi_returns_re = re.compile(r"\n\n+")
    textbody = multi_returns_re.sub(r"\n\n", textbody)

    return textbody

def separate_body(textbody):
    """Separates the preamble from the document body"""
    begin_end_doc_re = re.compile(r"\\begin\{document}|\\end\{document}")
    doc = begin_end_doc_re.split(textbody)
    if len(doc) == 1:
        preamble = None
        body = doc
    else:
        preamble = doc[0]
        body = doc[1]
    return preamble, body


ESC = [
    ["\\$","_dollar_","&#36;","\\$"],
    ["\\%","_percent_","&#37;","\\%"],
    ["\\&","_amp_","&amp;","\\&"],
    [">","_greater_",">","&gt;"],
    ["<","_lesser_","<","&lt;"]
]
def reformat_escapes(body):
    """Swaps \$, \%, \&, <, > for placeholders, to be handled later"""
    for e in ESC:
        body.replace(e[0], e[1])
    return True

ACCENTS = [
    #["\\\\","<br/>\n"],
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
def reformat_accents(body):
    """Replace TeX flavored accents with HTML compatible accents"""
    for s1, s2 in ACCENTS:
        body = body.replace(s1, s2)
    return True

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
def reformat_fontstyles(body):
    """Replace TeX fontstyles with HTML fontstyles"""
    pass




def driver():
    inputfile = "input.tex"
    outputfile = "output.html"
    if len(argv) > 1 :
        inputfile = argv[1]
        if len(argv) > 2 :
            outputfile = argv[2]
        else :
            if inputfile[-4:] == ".tex":
                outputfile = inputfile.replace(".tex",".html")
            elif inputfile[-3:] == ".md":
                outputfile = inputfile.replace(".md", ".html")
            else:
                outputfile = inputfile + ".html"

    f = open(inputfile)
    text = f.read()
    f.close()

    title = extract_title(text)
    print title

    text = clean_whitespace(text)
    preamble, body = separate_body(text)

    reformat_escapes(text)
    reformat_accents(text)



    out = open(outputfile, "w")
    out.write(title + "\n\n" + preamble + "\n\n" + body)
    out.close()
    print "The output is now in " + str(outputfile)



if __name__=="__main__":
    driver()

"""
currently hanging:
    1. title, preamble, body currently unused in driver()
    2. handle `\\\\`, as in ACCENTS, but I removed
"""
