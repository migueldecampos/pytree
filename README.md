# pytree
Like tree but for Python projects

	usage: pytree.py [-h] [-c] [-e] [-f] [-i] [directory]
	
	Show the directory tree of a Python project.
	
	positional arguments:
 	 directory         root directory, if none is given Pytree will start at '.'

	optional arguments:
	  -h, --help        show this help message and exit
	  -c, --comments    print first line of every .py file if it is a comment
	  -e, --explain     print pyexplain.txt for every directory that has one
	  -f, --functions   print name of functions defined in each .py file
	  -i, --invisibles  include invisibles except . and ..
