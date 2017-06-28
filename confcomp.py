#!/usr/bin/python3
# Created by Smirrom (smirrom@gmail.com)
# GitHub: https://github.com/smirrom/confcomp

import re, sys
from tabulate import tabulate

if '--help' in sys.argv or '-h' in sys.argv:
   print('This is script that comparses two config file, uses parameter=value format. Comments ignored.\n\
Usage: confcomp.py <config_file1> <config_file2>')
   exit(0)

if len (sys.argv) < 3:
   print('Not enough parameters. Use -h or --help for help.')
   exit(1)

def isParameterExist(conf, parameter):
    exist=0
    for entry in conf:
        if entry[0] == parameter:
            exist=1
    return exist

def paramlist_difference(list1, list2):
    diff_list = []
    for item in list1:
        if not isParameterExist(list2, item[0]):
            diff_list.append(item)
    return diff_list

valid_items=re.compile("^(?:\s+)?(?P<parameter>\w+)(?:\s+)?=(?:\s+)(?P<value>(?:'(?:.*)')|(?:\S+))", re.MULTILINE)

filename1 = sys.argv[1]
filename2 = sys.argv[2]

conf1text = open(filename1, "r").read()
conf2text = open(filename2, "r").read()

m = valid_items.findall(conf1text)
if m:
    conf1 = set(m)
else:
    print('No valid entries in config file 1')

m = valid_items.findall(conf2text)
if m:
    conf2 = set(m)
else:
    print('No valid entries in config file 2')

commonvalues=set()
for c1entry in conf1:
    for c2entry in conf2:
        if c1entry[0] == c2entry[0]:
            commonvalues.add((c1entry[0], c1entry[1], c2entry[1]))

print("Common parameters:\n----------------")
print ("\n",tabulate(commonvalues, headers=["Parameter","Value in File 1", "Value in File 2"]))

print("\nUnique parameters of File 1:\n----------------------------")
print ("\n",tabulate(paramlist_difference(conf1, conf2), headers=["Parameter", "Value"]))

print("\nUnique parameters of File 2:\n----------------------------")
print ("\n",tabulate(paramlist_difference(conf2, conf1), headers=["Parameter", "Value"]))

