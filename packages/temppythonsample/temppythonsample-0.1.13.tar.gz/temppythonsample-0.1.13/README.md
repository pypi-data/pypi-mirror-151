# Python-Sample-Library
This is custom library
    
# we first need to install build.
    pip install build twine

# To create a Python source package (.tar.gz) and the binary package (.whl) in the dist/ directory, do:
    python -m build

# Publish the python library on Pypi
    twine upload dist/*