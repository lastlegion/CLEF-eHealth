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
			state = "text"

		elif(state == "text"):	
			#just querying the title field
			strt = line.find("<title>")
			if( strt != -1 ):
				end = line.find("</title>")
				wline = line[strt+7:end] 
				wline += ")</text>\n\t</query>\n"
				state = "next"
				print "Query " + str(count) + " generated"		

		fw.write(wline)
