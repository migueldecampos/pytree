# this is the file that will be run in order to launch pytree
import os
import argparse
import re

def print_spaces_and_bars(levels, last, explanations):
	# see print_entry() for info on arguments
	if len(levels) == 0:
		return
	i = 0
	while i < max(levels) + 4:
		if not explanations and i == levels[-1]:
			if not last:
				print('├', end='')
			else:
				print('└', end='')
		elif i == max(levels) + 3:
			print(' ', end='')
		elif not explanations and i > levels[-1]:
			print('─', end='')
		elif i in levels:
			print('|', end='')
		else:
			print(' ', end='')
		i = i + 1

def manage_entry(path, name, levels, last, args, uncertain_prints, certain_prints):
	# path -> (string) path to file / directory
	# name -> (string) name to be printed
	# levels -> (list of ints) 
	# last -> (boolean) false if 'name' is the last element of its parent directory
	# args -> options
	# uncertain_prints -> (list of tuples) directories we are not sure we will print
	#                     tuple = (name, levels, last, explanations)
	# certain_prints -> (list of tuples) files / directories / comments we are sure we will print
	
	if path == None:
		certain_prints.append((name, levels[:], last, False))
		return
	if os.path.isdir(path):
		if not args.py:
			certain_prints.append((name, levels[:], last, False))
		else:
			uncertain_prints.append((name, levels[:], last, False))
		# launching manage_entry() for all files and directories 
		# inside the directory we are dealing with
		children = os.listdir(path)
		if '__pycache__' in children:
			children.remove('__pycache__')
		if not args.invisibles:
			while len(children) > 0 and (children[0])[0] == ".":
				children.pop(0)
		if args.explain and 'pyexplain.txt' in children:
			for t in uncertain_prints:
				certain_prints.append(t)
			while len(uncertain_prints) > 0:
				uncertain_prints.pop()

			with open(path + '/' + 'pyexplain.txt') as f:
				for line in f:
					certain_prints.append((' " ' + line[:-1], levels[:], last, True))
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
			manage_entry(path + '/' + children[i], children[i], levels[:], last, args, uncertain_prints, certain_prints)
			i = i + 1
		if len(uncertain_prints) > 0 and uncertain_prints[-1][0] == name:
			uncertain_prints.pop()
	else:
		if not args.py or re.match('[\S]{0,}.py$', name):
			for t in uncertain_prints:
				certain_prints.append(t)
			while len(uncertain_prints) > 0:
				uncertain_prints.pop()
			certain_prints.append((name, levels[:], last, False))

	if (args.comments or args.functions) and re.match('[\S]{0,}.py$', name):
		# print comment and functions for .py files
		fns = []
		with open(path) as f:
			first = True
			for line in f:
				if first and args.comments and line[0] == '#':
					certain_prints.append((line[:-1], levels[:], last, True))
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
				manage_entry(None, fns[i], levels[:], last, args, uncertain_prints, certain_prints)
				i = i + 1

def clean_printables(to_print):
	# tuple = (name, levels, last, explanations)
	activ_levels = []
	i= len(to_print) - 1
	while i > 0:
		if len(activ_levels) == 0 or (max(activ_levels) < to_print[i][1][-1]):
			ln = len(to_print[i][1])
			j = 0
			while j < ln:
				if to_print[i][1][j] not in activ_levels:
					to_print[i][1][j] = to_print[i][1][-1]
				j = j + 1
			activ_levels.append(to_print[i][1][-1])
			to_print[i] = (to_print[i][0], to_print[i][1], True, to_print[i][3])
		else:
			if max(activ_levels) < to_print[i][1][-1] and len(activ_levels) > 1:
				activ_levels.remove(max(activ_levels))
			if to_print[i][1][-1] not in activ_levels:
				activ_levels.append(to_print[i][1][-1])
				to_print[i] = (to_print[i][0], to_print[i][1], True, to_print[i][3])
			ln = len(to_print[i][1])
			j = 0
			while j < ln:
				if to_print[i][1][j] not in activ_levels:
					to_print[i][1][j] = to_print[i][1][-1]
				j = j + 1
		i = i - 1



def pytree_main():
	parser = argparse.ArgumentParser(description='Show the directory tree of a Python project.')
	parser.add_argument('-c', '--comments', dest='comments', action='store_true', help='print first line of every .py file if it is a comment')
	parser.add_argument('-e', '--explain', dest='explain', action='store_true', help='print pyexplain.txt for every directory that has one')
	parser.add_argument('-f', '--functions', dest='functions', action='store_true', help='print name of functions defined in each .py file')
	parser.add_argument('-i', '--invisibles', dest='invisibles', action='store_true', help='include invisibles except . and ..')
	parser.add_argument('-p', '--py', dest='py', action='store_true', help='print only .py files and their folders')
	parser.add_argument('directory', nargs='?', default='.', help='root directory, if none is given Pytree will start at \'.\'')
	args = parser.parse_args()

	if not os.path.isdir(args.directory):
		print('usage: pytree.py [-h] [-s] [directory]')
		print(f"pytree.py: error: {args.directory} is not a directory")
		exit()
	to_print = []
	manage_entry(args.directory, args.directory, [], False, args, [], to_print)
	clean_printables(to_print)
	# tuple = (name, levels, last, explanations)
	# print_spaces_and_bars(levels, last, explanations):
	for t in to_print:
		print_spaces_and_bars(t[1], t[2], t[3])
		print(t[0])


if __name__ == '__main__':
	pytree_main()

