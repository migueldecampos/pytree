#this is the file that will be run in order to launch pytree
import os
import argparse
from sys import argv

def print_spaces_and_bars(levels, last):
	# see print_entry() for info on arguments
	
	if len(levels) == 0:
		return
	i = 0
	while i < levels[-1] + 4:
		if i == levels[-1]:
			if not last:
				print('├', end='')
			else:
				print('└', end='')
		elif i == levels[-1] + 3:
			print(' ', end='')
		elif i > levels[-1]:
			print('─', end='')
		elif i in levels:
			print('|', end='')
		else:
			print(' ', end='')
		i = i + 1

def print_entry(path, name, levels, last, args):
	# path -> (string) path to file / directory
	# name -> (string) name to be printed
	# levels -> (list of ints) 
	# last -> (boolean) false if 'name' is the last element of its parent directory
	# args -> options
	
	print_spaces_and_bars(levels, last)
	print(name)
	if os.path.isdir(path):
		if len(levels) > 0:
			new_level = levels[-1] + 4
		else:
			new_level = 0
		if last:
			levels.pop()
		levels.append(new_level)
		children = os.listdir(path)
		ln = len(children)
		i = 0
		last = False
		while i < ln:
			if i == ln - 1:
				last = True
			print_entry(path + '/' + children[i], children[i], levels[:], last, args)
			i = i + 1

def pytree_main():
	parser = argparse.ArgumentParser(description='Show the directory tree of a Python project.')
	parser.add_argument('-c', '--comments', dest='simple', action='store_true', help='print first line of every .py file if it is a comment')
	parser.add_argument('-e', '--explain', dest='simple', action='store_true', help='print pyexplain.txt for every directory that has one')
	parser.add_argument('-f', '--functions', dest='simple', action='store_true', help='print name of functions defined in each .py file')
	parser.add_argument('-i', '--invisibles', dest='simple', action='store_true', help='include invisibles except . and ..')
	parser.add_argument('directory', nargs='?', default='.', help='root directory, if none is given Pytree will start at \'.\'')
	args = parser.parse_args()

	if not os.path.isdir(args.directory):
		print('usage: pytree.py [-h] [-s] [directory]')
		print(f"pytree.py: error: {args.directory} is not a directory")
		exit()
	print_entry(args.directory, args.directory, [], False, args)

if __name__ == '__main__':
	pytree_main()

