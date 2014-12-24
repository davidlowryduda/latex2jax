# latex2jax

import re
from sys import argv



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
def reformat_escapes_prelim(body):
    """Swaps \$, \%, \&, <, > for placeholders, to be handled later"""
    for e in ESC:
        body = body.replace(e[0], e[1])
    return body

def reformat_escapes_text(body):
    """Swaps the ESC placeholders in the text document."""
    for e in ESC:
        body = body.replace(e[1], e[2])
    return body

def reformat_escapes_math(math_piaces):
    """Swaps the ESC placeholders in the math document."""
    for e in ESC:
        body = body.replace(e[1], e[3])
    return body


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
    return body

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
#TODO reformat_fontstyles
def reformat_fontstyles(body):
    """Replace TeX fontstyles with HTML fontstyles"""
    pass

#TODO reformat_subsections
def reformat_sections(body):
    """Replaces sections, subsections, and subsubsections with html"""
    pass

#TODO enclose_math_environments
def separate_math(body):
    """Returns math, text split in body"""
    math_re = re.compile(r"\$+.*?\$+" +
                         r"|\\begin\{equation*?\}.*?\\end\{equation*?\}" +
                         r"|\\begin\{align*?\}.*?\\end\{align*?\}" +
                         r"|\\\[.*?\\\]",
                         flags=re.DOTALL)
    math = math_re.findall(body)
    text = math_re.split(body)
    return math, text

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
def handle_theorem_environments(body):
    """Handles the theorem environments in body"""
    envs_re = re.compile(r"\\begin\{\w+}" +
                                 r"|\\end\{\w+}")
    backbody = envs_re.split(body)
    env_flags = envs_re.findall(body)
    text = backbody[0]
    i = 0
    while i < len(env_flags):
        found = False
        for ThmEnv in ThmEnvs:
            if env_flags[i].find("{"+ThmEnv+"}") != -1:
                print "Found " + ThmEnv, env_flags[i]
                found = True
                if env_flags[i].find("begin") != -1:
                    text = text + add_open_theorem_div(ThmEnv)
                elif env_flags[i].find("end") != -1:
                    text = text + "</div>\n"
                else:
                    print "Error! Type ENVFLAG"
        if not found:
            text = text + env_flags[i]
        text += backbody[i+1]
        i += 1
    return text

def add_open_theorem_div(theorem_type):
    open_div = '\n<div class="'+theorem_type+'">'
    return open_div

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

    text = reformat_escapes_prelim(text)
    text = reformat_accents(text)

    text = clean_whitespace(text)
    preamble, body = separate_body(text)


    math, body = separate_math(body)
#    print math
#    print body

    math = [str(m) for m in math]
#    math = "\n".join(math)
    body = [str(t) for t in body]
#    body = "\n".join(body)

    # Reconcatenate the text with placeholders for math.
    text = body[0]
    for i in range(len(math)):
        text = text + "__math"+str(i)+"__" + body[i+1]

    debug_out = open("debugger.txt", "w")
    debug_out.write(text)

    # Handle theorem environments, I suppose.
    text = handle_theorem_environments(text)

    debug_out2 = open("postdebugger.txt", "w")
    debug_out2.write(text)

    #Handle Math
    #Handle Text




    # Replace math into text
    for i in range(len(math)):
        text = text.replace("__math"+str(i)+"__", math[i])

    out = open(outputfile, "w")
    #out.write(title + "\n\n" + preamble + "\n\n" + body)
    out.write(title + "\n\n" + preamble + "\n\n")
#    out.write(math)
#    out.write(body)
    out.write(text)




    out.close()
    print "The output is now in " + str(outputfile)




if __name__=="__main__":
    driver()

"""
currently hanging:
    1. title, preamble, body currently unused in driver()
    2. handle `\\\\`, as in ACCENTS, but I removed
"""
