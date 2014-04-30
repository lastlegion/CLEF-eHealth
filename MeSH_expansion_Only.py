import os
from xml.dom import minidom
import enchant
import subprocess
import re

#d=enchant.DictWithPWL("en_us","medical_terms.txt")
d = enchant.Dict("en_us")
#fr = open("q.xml",'r');
fw = open('q5_indri2.xml', 'w')
fr = open("stopwords.txt",'r')
#fread = open("medical_words.txt", 'r')

'''
for line in fread:
    d.add(line.strip())
    print line
'''
stopwords = []
for line in fr:
    if(line.strip() != ""):
        line=line.replace(',','')
        stopwords.append(line.strip())
#print stopwords

xmldoc = minidom.parse('queries.clef2014ehealth.1-50.test.en.xml')
qlist = xmldoc.getElementsByTagName('desc')
tlist = xmldoc.getElementsByTagName('title')
count=0
fw.write('<parameters>\n')
IND_Qs = [[]]

for query in qlist:
    fw.write('\t<query>\n')
    fw.write('\t\t<type>indri</type>\n')
    fw.write('\t\t<number>qtest' + str(count+1)+ '</number>\n')
    fw.write('\t\t<text>')
    ind_q = []
    main_q = []

    #Title tag
    for term in tlist[count].childNodes[0].nodeValue.split(" "):
        #Clean term(remove extra chars)
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords:
	        ind_q.insert(0, term.lower())
                main_q.append(term.lower())
            #fw.write(term + " ") 
   #Desc tag
    for term in query.childNodes[0].nodeValue.split(" "):
        #Clean term(remove extra chars)
        term = ''.join(e for e in term if e.isalnum())
        if term not in stopwords and len(term)>=2:
	        ind_q.insert(0, term.lower())
                main_q.append(term.lower())
            #fw.write(term + " ")

    #Expand using spellchecker
    '''
    for term in ind_q:
        if not d.check(term):
            correctedList = d.suggest(term)
            ind_q.append(correctedList[0])
            main_q.append(term.lower())
    #fw.write(main_q)    
    '''
    ind_q_str = ' '.join(ind_q) 
    
    mesh_q = []
    #Expand using metamap
    #p = subprocess.Popen('echo "copd" | metamap13 -v -a  -O -T --bracketed_output -K -Y' )
    p = subprocess.Popen('echo "'+ ind_q_str +'"| metamap13 -v -a -O -T --bracketed_output -K -Y', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    state = "none"
    for line in p.stdout.readlines():
        line = line.strip()
        if(line == ">>>>> Variants"):
            state = "variants"
            #print "yo"
        if(state == "variants"):
            if(re.match(r'[0-9].*', line.strip(),re.M|re.I)):
                s = re.search(r'[0-9]*:(.*){.*}',line, re.M|re.I)
                #print s.group(1).strip()
                if(s):
                    expansion_term = s.group(1).strip()
                
                #Add expansion term
                if(expansion_term not in ind_q):
                    #ind_q.append(expansion_term)
                    mesh_q.append(expansion_term)
                    #print "here"
        if(line == "<<<<< Variants"):
            state="none"
   
    ind_q_str = ' '.join(ind_q)    
    main_q_str = ' '.join(main_q)
    mesh_q_str_1= ' '.join(mesh_q[0:3])
    mesh_q_str_2 = ' '.join(mesh_q[3:len(mesh_q)])
    #print mesh_q 
    #print mesh_q_str_1
    #print mesh_q_str_2
    
    if not mesh_q:
        fw.write("#combine( ")
        fw.write(main_q_str)
        fw.write(" )")
    else:
        fw.write("#weight( 0.6 #combine( ")
        fw.write(main_q_str)
        fw.write(" )")
        
    if(mesh_q_str_2):
        fw.write(" 0.3 #combine(")
        fw.write(mesh_q_str_1)
        fw.write(")")
        fw.write(" 0.1 #combine(")
        fw.write(mesh_q_str_2)
        fw.write(" )")
    else:
        fw.write(" 0.4 #combine( ")
        fw.write(mesh_q_str_1)
        fw.write(" )")
    
    fw.write(" )")
    fw.write('</text>\n')
    fw.write('\t</query>\n')
    count = count+1
    print ind_q

    IND_Qs.insert(len(IND_Qs), ind_q)   
 
fw.write('</parameters>')

