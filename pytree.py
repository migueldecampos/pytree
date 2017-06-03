# this is the file that will be run in order to launch pytree
import os
import argparse
import re

def print_spaces_and_bars(levels, last, explanations):
	# see print_entry() for info on arguments
	if len(levels) == 0:
		return
	i = 0
	while i < levels[-1] + 4:
		if not explanations and i == levels[-1]:
			if not last:
				print('├', end='')
			else:
				print('└', end='')
		elif i == levels[-1] + 3:
			print(' ', end='')
		elif not explanations and i > levels[-1]:
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
	print_spaces_and_bars(levels, last, False)
	print(name)
	if path == None:
		return
	if os.path.isdir(path):
		children = os.listdir(path)
		if not args.invisibles:
			while len(children) > 0 and (children[0])[0] == ".":
				children.pop(0)
		if args.explain and 'pyexplain.txt' in children:
			with open(path + '/' + 'pyexplain.txt') as f:
				for line in f:
					print_spaces_and_bars(levels, last, True)
					print(' " ' + line, end='')
			children.remove('pyexplain.txt')
		if len(levels) > 0:
			new_level = levels[-1] + 4
		else:
			new_level = 0
		if last:
			levels.pop()
		levels.append(new_level)
		ln = len(children)
		i = 0
		last = False
		while i < ln:
			if i == ln - 1:
				last = True 
			print_entry(path + '/' + children[i], children[i], levels[:], last, args)
			i = i + 1
	elif (args.comments or args.functions) and re.match('[\S]{0,}.py$', name):
		first = True
		fns = []
		with open(path) as f:
			for line in f:
				if first and args.comments and line[0] == '#':
					print_spaces_and_bars(levels, last, True)
					print(line, end='')
					if not args.functions:
						break
				if args.functions:
					m = re.search('(?<=^def )\S+(?=\()', line)
					if m:
						fns.append(m.group() + '()')
				first = False
			if len(fns) > 0:
				if len(levels) > 0:
					new_level = levels[-1] + 4
				else:
					new_level = 0
				if last:
					levels.pop()
				levels.append(new_level)
				i = 0
				ln = len(fns)
				last = False
				while i < ln:
					if i == ln - 1:
						last = True
					print_entry(None, fns[i], levels[:], last, args)
					i = i + 1



def pytree_main():
	parser = argparse.ArgumentParser(description='Show the directory tree of a Python project.')
	parser.add_argument('-c', '--comments', dest='comments', action='store_true', help='print first line of every .py file if it is a comment')
	parser.add_argument('-e', '--explain', dest='explain', action='store_true', help='print pyexplain.txt for every directory that has one')
	parser.add_argument('-f', '--functions', dest='functions', action='store_true', help='print name of functions defined in each .py file')
	parser.add_argument('-i', '--invisibles', dest='invisibles', action='store_true', help='include invisibles except . and ..')
	parser.add_argument('directory', nargs='?', default='.', help='root directory, if none is given Pytree will start at \'.\'')
	args = parser.parse_args()

	if not os.path.isdir(args.directory):
		print('usage: pytree.py [-h] [-s] [directory]')
		print(f"pytree.py: error: {args.directory} is not a directory")
		exit()
	print_entry(args.directory, args.directory, [], False, args)

if __name__ == '__main__':
	pytree_main()

