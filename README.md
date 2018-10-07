latex2jax
=========

We have latex2wp and [mse2wp](http://github.com/davidlowryduda/mse2wp), but
Wordpress is restrictive.

This is the first tool towards a more independent, freer site. There are a few
fundamental assumptions:

    1. You have an AMS-LaTeX file, and you want it displayed on a website
    2. The site uses Mathjax
    3. You want to be able to manipulate things like Theorem environments with css

This is the very beginning, and very much in development.


Basic Usage
-----------

Clone this repo or download latex2wp. Then in a terminal, type

    python3 latex2jax.py yourfile.tex

or, more generally,

    python3 <path/to/latex2jax.py> <path/to/yourfile.tex>

I would recommend running this from the same directory as `yourfile.tex`.


Additional Notes
----------------

There are sometimes little errors, especially if the tex document includes
manual formatting. In these cases, it may be necessary to correct these
discrepancies by hand (but this should be much easier than converting the whole
document manually).

If you detect routine errors, raise an issue or send an email.



Implementation
--------------

This is implemented in python, similar to mse2wp.
