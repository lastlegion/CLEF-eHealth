#!/bin/bash
# feedback optimum point

echo "Hello"

FILENAME="fool"
OUTPUTFILE="output"

P10_MAX=0
newval=0 

#i is for docs
for i in 1 10 15 20
do 
	#j is for terms
	for j in 0 5 10
	do
		#k is for weights
		for k in 0 0.5 1
		do
			#cd 2013data/			
			IndriRunQuery -memory=1G -index="../indexed_data" -count=100 "../Queries/queries.clef2014ehealth.1-50.test.en.INDRI.xml" -trecFormat=true -fbDocs=$i -fbTerms=$j -fbOrigWeight=$k > $FILENAME
			cd ..
			cd trec_eval.9.0/
			./trec_eval ../Queries/qrels.clef2013ehealth.1-50-test.bin.final.txt ../CLEF-eHealth/$FILENAME > evals/$OUTPUTFILE
			cd evals/
			newval=$(python result_analysis.py 2>&1)
			#put result_analysis.py in trec_eval.9.0/evals/

			echo "newval is $newval"
			
			awk 'BEGIN{if ('$newval'>'$P10_MAX') exit 1}'
			if [ $? -eq 1 ];then
				P10_MAX=$newval
				echo "doc is $i, terms $j, weight $k"
			fi
			
			cd ..
			cd ..
			
		done
	done	
done
