fw = open('wiki_trecweb_style','w')
count =0
with open('wiki.0842_12.dat','r') as fr:
    state = "doc"
    for line in fr:     
        line = line.strip()
        line = line.strip("\\")
        wline=""
        if(state == "doc"):
            if(line[0:4] == "#UID"):
                wline = "<DOC>\n<DOCNO>\n\t"+ line[5:len(line)]+ "\n</DOCNO>\n<DOCHDR>\n"
                state = "hdr"
        elif(state=="hdr"):
                #print line
                wline= ""
                if(line[0:3] == "#CO"):
                    state="content"
                    wline+="</DOCHDR>"
        elif(state=="content"):
            #print "content state"
            wline=line
            if(line[0:4]=="#EOR"):
                count = count+1
                print "Processed " + str(count) + " docs"
                state="doc"
                wline+="\n</DOC>\n"
        fw.write(wline + "\n")
