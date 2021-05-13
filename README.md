# Tcl magic

[IPython](https://ipython.org) extension which adds [Tcl](https://www.tcl.tk) magics.

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
