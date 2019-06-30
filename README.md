# Tcl magic

Usage
=====

Load the extension:

    In[1]: %load_ext tclmagic

Use the extension:

    In[2]: %%tcl
           set tcl_precision 17
           expr acos(-1)

    Out[2] 3.141592653589793

