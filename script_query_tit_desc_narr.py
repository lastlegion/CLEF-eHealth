#Usage: python script_query.py <title> <desc> <narr>
#0 -> Dont want to include
#1 -> Wanna include
import sys

if(len(sys.argv) != 4):
    print "Usage: python script_query.py <title> <desc> <narr>"
    print "Title/desc/narr takes values"
    print "0 -> Dont want to include"
    print "1 -> wanna include"
    sys.exit(1)

fw = open('query_test_1-50_formatted','w')

count = 0;

with open('queries.clef2013ehealth.1-50.test.xml','r') as fr:

	state = "begin"
	for line in fr:
		line = line.strip()
		line = line.strip("\\")
		wline = ""

		if(state == "begin"):
			wline = "<parameters>\n"
			state = "next"

		elif(line[0:10] == "</queries>"):
			wline = "</parameters>\n"
			state = "done"

		elif(state == "next"):
			if(line.find("<id>") != (-1)):
				state = "query"

		elif(state == "query"):
			wline = "\t<query>\n\t\t<type> indri </type>\n\t\t<number> "
			count += 1
			wline += str(count) 
			wline += " </number>\n\t\t"
			wline += "<text> #combine("
			state = "title"

		elif(state == "title"):	
			if(sys.argv[1]=="1"):
				#just querying the title field
				strt = line.find("<title>")
				if( strt != -1 ):
					end = line.find("</title>")
					wline += line[strt+7:end]
					wline += " "
			state = "desc"
			
		elif(state == "desc"):	
			if(sys.argv[2]=="1"):
				#just querying the desc field
				strt = line.find("<desc>")
				if( strt != -1 ):
					end = line.find("</desc>")
					wline += line[strt+6:end] 
					wline += " "
			state = "narr"
		
		elif(state == "narr"):	
			if(sys.argv[3]=="1"):
				#just querying the desc field
				strt = line.find("<narr>")
				if( strt != -1 ):
					end = line.find("</narr>")
					wline += line[strt+6:end] 
					wline += " "
			state = "done_text"
					
		elif(state == "done_text"):			
			wline += ")</text>\n\t</query>\n"
			state = "next"
			print "Query " + str(count) + " generated"		

		fw.write(wline)