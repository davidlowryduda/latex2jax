
LaTeX to html+Mathjax with kind css conversion
==============================================

Order of operations
-------------------
  1. Extract title
      # Done
  2. Separate preamble and body
  3. Extract macros from the preamble
  4. Handle title
    - window name should incorporate title
    - make title heading h1
  5. Handle macros
    - place in invisible div for Mathjax
    - see "Macros div" below
  6. Handle the body. Everything below is for the body.
  7. Remove extra space and lines
  8. Swap escape sequences `\$`, `\%`, `\&`, and `<`, `>`
  9. Swap manual newlines `\\`, spaces `\ `, and accents
  10. Swap fontstyles `\em`, `bf`, etc.
  11. Convert text tables into html tables
    - Completely inessential, low priority of implementation
  12. Convert itemize, enumerate
  13. Put `<p> ... </p>` tags in
    - Excessively - remove excess later
  14. Handle the \begin ... \end math.
    - equation, equationstar, align, alignstar
    - Enclose in `$` for mathjax
  15. Convert theorem environments
    - Handle both named and unnamed thms
    - Have a reference list, like "Theorem Environment List"
    - Remove labels, for now
      # Until we can handle the references better
  16. Convert section, sectionstar, subsection, subsectionstar


Macros div
----------
To define macros, we'll place them in an invisible div, but
still inside mathmode so that mathjax will interpret them.
In particular,

    <div style="display:none">
    \[
      \newcommand{\CC}{\mathbf{C}}
    \]
    </div>

Alternately, we could simply decide on preestablished macros
that seem worthwhile, and use no others. This would also keep
good portability with journals, etc.


Theorem Environment List
------------------------
A reasonable start is the following. Either stick to it, or

    ThmEnvs = ["theorem","definition","lemma",
               "proposition","corollary","claim",
               "remark","example","exercise"]

In short, keep with it at first.


Wishlist
--------
  1. Handle theorem numbering
  2. Handle theorem labeling and ref
  3. Handle `\cite` and bibliography


How to handle labels and ref
----------------------------
First thought:
  1. Go through document and make lists of theorem env labels
  2. Keep refs only for not theorem env labels
  3. Modify the others, as in mse2wp


vim: foldmethod=indent foldcolumn=2 ts=2 sw=2 sts=2
