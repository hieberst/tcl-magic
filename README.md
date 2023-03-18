# Tcl magic

[IPython](https://ipython.org) extension which adds [Tcl](https://www.tcl.tk) magics.

The trigger for the development of this IPython extension was the support of a new colleague during his induction, whereby this extension helped as follows:

1. Demonstrate using Tcl from within Python.
2. Allow to use [Jupyter Notebook](https://jupyter.org) as a common environment for a short introduction to both [Python](https://www.python.org) and Tcl.

My play instinct to just write a simple IPython extension was of course reason enough.

## Installation

Install or upgrade with `pip`:

    pip install -U tcl-magic

## Usage

Load the extension:

    In[1]: %load_ext tclmagic

Use the line magic `%tcl` to execute external Tcl code:

    In[2]: %tcl pi.tcl

    Out[2] 3.141592653589793

Use the cell magic `%%tcl` to execute inline Tcl:

    In[3]: %%tcl
           set tcl_precision 17
           expr acos(-1)

    Out[3] 3.141592653589793
