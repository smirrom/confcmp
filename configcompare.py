#!/usr/bin/python3

import re
from tabulate import tabulate

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


valid_items=re.compile("^(?P<parameter>\w+)(?:\s+)?=(?:\s+)(?P<value>(?:'(?:.*)')|(?:\S+))", re.MULTILINE)

conf1text = open("pg94.conf", "r").read()
conf2text = open("pg96.conf", "r").read()

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

print("Общие параметры:\n----------------")
print ("\n",tabulate(commonvalues, headers=["Параметр","Значение в файле 1", "Значение файле 2"]))

print("\nУникальне параметры файла 1:\n----------------------------")
#for uentry in conf1.difference(conf2):
#    print(uentry[0],'=',uentry[2])

print ("\n",tabulate(paramlist_difference(conf1, conf2), headers=["Параметр", "Значение"]))

print("\nУникальне параметры файла 2:\n----------------------------")
print ("\n",tabulate(paramlist_difference(conf2, conf1), headers=["Параметр", "Значение"]))

#print (lines1)

