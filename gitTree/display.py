#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

C_GREEN = '\033[92m'
C_BLUE = '\033[94m'
C_END = '\033[00m'


def __getForestFormated(items, prefix=""):
	res = ""
	for index, item in enumerate(sort(items)):
		if items[item]:
			res += "{2}[\\path{{{0}}}\n{1}{2}]\n".format(item, __getForestFormated(items[item], prefix + "\t"), prefix)
		else:
			res += prefix + "[\\path{{{}}}]\n".format(item)

	return res


def formatInLatex(items, output, path=".", ):
	forest = """\\documentclass[tikz, border=5pt, multi]{{article}}
\\usepackage[edges]{{forest}}
\\usepackage{{url}}
\\begin{{document}}
\\begin{{forest}}
for tree={{%
    folder,
    grow'=0,
    fit=band,
    %s sep-=2mm
  }}
{}
\\end{{forest}}
\\end{{document}}"""
	forest = forest.format("[\\path{{{}}}\n{}]".format(path, __getForestFormated(items, "\t")))

	with open(output, "w") as file:
		file.write(forest)


def sort(enumeration):
	keys = enumeration.keys()
	keys.sort(key=lambda i: "\0" + i if enumeration[i] else i)
	return keys


def displayItems(items, path, prefix, color):
	for index, item in enumerate(sort(items)):
		if index == len(items) - 1:
			print prefix + '└── ' + appendColor(path, item, color)
			nextPrefix = prefix + '    '
		else:
			print prefix + '├── ' + appendColor(path, item, color)
			nextPrefix = prefix + '│   '
		if len(items[item]) > 0:
			nextpath = os.path.join(path, item)
			displayItems(items[item], nextpath, nextPrefix, color)


def appendColor(path, item, color=False):
	filepath = os.path.join(path, item)
	colorCode = ''
	endCode = C_END if color else ''
	indicator = ''
	if color:
		if os.path.isdir(filepath):
			colorCode = C_BLUE
		elif os.access(filepath, os.X_OK):
			colorCode = C_GREEN
		else:
			colorCode = C_END

	if os.path.isdir(filepath):
		indicator = '/'

	return colorCode + item + endCode + indicator


def display(group, output):
	currentDir = os.path.split(os.getcwd())
	if not output:
		color = True
		print appendColor(currentDir[0], currentDir[1], color)
		displayItems(group, '.', '', color)
	elif output.endswith(".tex"):
		path = currentDir[1]
		formatInLatex(group, output, path)
