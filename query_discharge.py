#Usage:
#python query_to_indri.py <input query> <ds root folder> <output query file>

import os
from xml.dom import minidom
import sys
import enchant
import subprocess
import re

q_file_name = sys.argv[1]
ds_root = sys.argv[2]
out_file_name = sys.argv[3]

fr = open("stopwords.txt",'r')
stopwords = []
for line in fr:
    if(line.strip() != ""):
        line=line.replace(',','')
        stopwords.append(line.strip())

xmldoc = minidom.parse(q_file_name)
idlist = xmldoc.getElementsByTagName('id')
dslist = xmldoc.getElementsByTagName('discharge_summary')
qlist = xmldoc.getElementsByTagName('desc')
tlist = xmldoc.getElementsByTagName('title')

fw = open(out_file_name, "w")

fw.write('<parameters>\n')
count=0

for query in qlist:

    if count == 50:
        break

    fw.write('\t<query>\n')
    fw.write('\t\t<type>indri</type>\n')
    fw.write('\t\t<number>qtest2014.' + str(count+1)+ '</number>\n')
    fw.write('\t\t<text>')
    query_str = ""

    for term in tlist[count].childNodes[0].nodeValue.split(" "):
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords:
            term = term.lower()
            query_str = query_str+ " "+term

    for term in qlist[count].childNodes[0].nodeValue.split(" "):
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords:
            term = term.lower()
            query_str = query_str+ " "+term


    state = "normal"
    ds_file_name = dslist[count].childNodes[0].nodeValue
    ds_file_name = ds_root + ds_file_name
    ds_file = open(ds_file_name, "r")
    for line in ds_file:
        line = line.strip()

        if state == "past":
    	   line = ''.join([i for i in line if str.isalpha(i) or str.isspace(i)])
    	   ds_terms = line.split(" ")
    	   for ds_term in ds_terms:
    		  if ds_term not in stopwords:
    		      #print line
    		      ds_term = ds_term.strip()
    		      query_str = query_str + " "+ds_term

    	if line == "Past Medical History:":
    		state = "past"
    	if line == "" and state=="past":
    		state = "normal"
    print "----"
    print query_str
    print count
    fw.write("#combine(")
    fw.write(query_str)
    fw.write(")")
    fw.write('</text>\n')
    fw.write('\t</query>\n')
    count = count+1
fw.write("</parameters>")