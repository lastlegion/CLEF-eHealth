import os
from xml.dom import minidom

#fr = open("q.xml",'r');
fw = open('q5_indri.xml', 'w')

xmldoc = minidom.parse('queries.clef2013ehealth.1-50.test.xml')
qlist = xmldoc.getElementsByTagName('desc')

count=0
fw.write('<parameters>\n')
for query in qlist:
    fw.write('\t<query>\n')
    fw.write('\t\t<type>indri</type>\n')
    fw.write('\t\t<number>qtest' + str(count+1)+ '</number>\n')
    fw.write('\t\t<text>')
    ind_q = []
    fw.write('#combine(')
    for term in query.childNodes[0].nodeValue.split(" "):
        ind_q.insert(0, term)
        fw.write(term + " ")
    fw.write(")")
    fw.write('</text>\n')
    fw.write('\t</query>\n')
    count = count+1
fw.write('</parameters>')
