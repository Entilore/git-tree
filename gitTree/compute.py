#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import re


def grouping(fileList, ignore):
    regex = re.compile(ignore)
    root = {}
    for path in fileList:
        current = root
        for p in path.rstrip('\n').split('/'):
            if not regex.match(p) or not ignore:
                current.setdefault(p, {})
                current = current[p]
            else:
                break
    return root


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


def getFileListWithoutGit(ignore):
    regex = re.compile(ignore)
    filesList = {}
    for root, dirs, files in os.walk(".", topdown=False):
        roots = root.split("/")
        del roots[0]

        for name in files:
            if not regex.match(name) or not ignore:
                nested_set(filesList, roots + [name], {})
        for name in dirs:
            if not regex.match(name) or not ignore:
                nested_set(filesList, roots + [name], {})

    return filesList


def getFileListWithGit(ignore):
    cmd = 'git ls-files'
    stdout_data, stderr_data, _ = execute(cmd)
    if len(stderr_data) > 0:
        print stderr_data,
    else:
        group = grouping(stdout_data, ignore)
    return group
