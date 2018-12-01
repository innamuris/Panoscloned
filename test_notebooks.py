#!/usr/bin/env python
# coding: utf-8

# In[8]:


import os
import subprocess
import tempfile

import nbformat

def notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """

    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
          "--ExecutePreprocessor.timeout=60",
          "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout.name, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
                     for output in cell["outputs"]\
                     if output.output_type == "error"]

    return nb, errors


# In[9]:


from os import listdir
from os.path import isfile, join, isdir

def test_notebooks(path):
    
    notebooks = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ipynb') and f!='test_notebooks']
    directories = [f for f in listdir(path) if isdir(join(path, f))]
    
    for notebook in sorted(notebooks):
        print(notebook)
        nb, errors = notebook_run(join(path, notebook))
        assert errors == []
    
    for directory in sorted(directories):
        print(directory)


# In[12]:


test_notebooks('.')


# In[ ]:




