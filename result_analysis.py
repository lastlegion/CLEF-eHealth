queries=[]
score=[]
with open('results.txt', 'r') as fr:
    for line in fr:
        words = line.split()
        if(words[0] == "P_10"):
            print str(words[1]) + " " + str(words[2])
            queries = queries.insert(0,words[1])      
            scores = scores.insert(0, scores[1])
