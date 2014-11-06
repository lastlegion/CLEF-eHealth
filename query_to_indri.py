#Usage:
#python query_to_indri.py <input query file> <output query file>

import os
from xml.dom import minidom
import sys


print "Opening "+str(sys.argv[1])
print "Writing to " + str(sys.argv[2]) 
q_file_name = sys.argv[1]
out_file_name = sys.argv[2]
#fr = open("q.xml",'r');
fw = open(out_file_name, 'w')

fr = open("stopwords.txt",'r')
stopwords = []
for line in fr:
    if(line.strip() != ""):
        stopwords.append(line.strip())
print stopwords

xmldoc = minidom.parse(q_file_name)
qlist = xmldoc.getElementsByTagName('desc')
tlist = xmldoc.getElementsByTagName('title')
count=0
fw.write('<parameters>\n')
for query in qlist:
    fw.write('\t<query>\n')
    fw.write('\t\t<type>indri</type>\n')
    fw.write('\t\t<number>qtest2014.' + str(count+1)+ '</number>\n')
    fw.write('\t\t<text>')
    ind_q = []
    fw.write('#combine(')
    for term in tlist[count].childNodes[0].nodeValue.split(" "):
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords:
	    ind_q.insert(0, term)
	    fw.write(term.encode('utf-8').strip() + " ")
    for term in query.childNodes[0].nodeValue.split(" "):
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords:
	    ind_q.insert(0, term)
            fw.write(term.encode('utf-8').strip() + " ")
    
    fw.write(")")
    fw.write('</text>\n')
    fw.write('\t</query>\n')
    count = count+1
fw.write('</parameters>')


