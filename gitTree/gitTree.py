#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

C_GREEN = '\033[92m'
C_BLUE = '\033[94m'
C_END = '\033[00m'


def grouping(fileList):
    root = {}
    for path in fileList:
        current = root
        for p in path.rstrip('\n').split('/'):
            current.setdefault(p, {})
            current = current[p]
    return root


def displayItems(items, path, prefix, color):
    for index, item in enumerate(sorted(items.keys())):
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


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})

    dic = dic.setdefault(keys[-1], value)


def execute(cmd):
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    p.wait()
    stdout_data = p.stdout.readlines()
    stderr_data = p.stderr.read()
    return stdout_data, stderr_data, p


def isOnGitRepository():
    cmd = "git rev-parse"
    stdout_data, stderr_data, p = execute(cmd)

    return p.returncode is 0


def getFileListWithoutGit():
    filesList = {}
    for root, dirs, files in os.walk(".", topdown=False):
        roots = root.split("/")
        del roots[0]

        for name in files:
            nested_set(filesList, roots + [name], {})
        for name in dirs:
            nested_set(filesList, roots + [name], {})

        print filesList

    return filesList


def getFileListWithGit():
    cmd = 'git ls-files'
    stdout_data, stderr_data, _ = execute(cmd)
    if len(stderr_data) > 0:
        print stderr_data,
    else:
        group = grouping(stdout_data)
    return group


def main():
    if isOnGitRepository():
        group = getFileListWithGit()
    else:
        group = getFileListWithoutGit()
    color = True
    currentDir = os.path.split(os.getcwd())
    print appendColor(currentDir[0], currentDir[1], color)
    displayItems(group, '.', '', color)


if __name__ == '__main__':
    main()
