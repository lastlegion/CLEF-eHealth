import os
from xml.dom import minidom
import enchant


#d=enchant.DictWithPWL("en_us","medical_terms.txt")
d = enchant.Dict("en_us")
#fr = open("q.xml",'r');
fw = open('q5_indri2.xml', 'w')

fr = open("stopwords.txt",'r')

fread = open("medical_words.txt", 'r')

for line in fread:
    d.add(line.strip())
    print line
stopwords = []
for line in fr:
    if(line.strip() != ""):
        line=line.replace(',','')
        stopwords.append(line.strip())
print stopwords

xmldoc = minidom.parse('queries.clef2013ehealth.1-50.test.xml')
qlist = xmldoc.getElementsByTagName('desc')
tlist = xmldoc.getElementsByTagName('title')
count=0
fw.write('<parameters>\n')
for query in qlist:
    fw.write('\t<query>\n')
    fw.write('\t\t<type>indri</type>\n')
    fw.write('\t\t<number>qtest' + str(count+1)+ '</number>\n')
    fw.write('\t\t<text>')
    ind_q = []
    fw.write('#combine(')
    for term in tlist[count].childNodes[0].nodeValue.split(" "):
        if term not in stopwords:
	    ind_q.insert(0, term)
        if not d.check(term):
            correctedList = d.suggest(term)
            print "Inserting "+ correctedList[0] + " for "+term
            fw.write(term + " ")
            fw.write(correctedList[0] + " ")
        else:
	        fw.write(term + " ")
    for term in query.childNodes[0].nodeValue.split(" "):
        if term not in stopwords and len(term)>=2:
	    ind_q.insert(0, term)
            if not d.check(term):
                correctedList = d.suggest(term)
                print "Inserting "+correctedList[0] + " for "+term
                fw.write(term + " ")
                fw.write(correctedList[0] + " ")
            else:
                fw.write(term + " ")
    fw.write(")")
    fw.write('</text>\n')
    fw.write('\t</query>\n')
    count = count+1
fw.write('</parameters>')


