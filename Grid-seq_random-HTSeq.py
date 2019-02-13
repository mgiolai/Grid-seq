#!/usr/bin/env python
from random import randint
import random
import sys

### GENERIC
#python script.py HTseq-counts.txt 1000000 >> HTseq-counts_random1000000reads.txt


#Open input file
countsfile = open(sys.argv[1], 'r')
#number of reads to subsample
maxReads = int(sys.argv[2])
#number of genes in table
increment = 0

#Dont consider these rows when randomising
elementsPass=["__no_feature", "__ambiguous", "__too_low_aQual", "__not_aligned", "__alignment_not_unique"]

#Randomise counts file
countsShuffle = countsfile.readlines()
countsfile.close()
random.shuffle(countsShuffle)

#Filter genes
for line in countsShuffle:
    line=line.replace("\n","").split("\t")
    if str(line[0]) not in elementsPass:
        if maxReads > 0: #Check that the maximal number of reads is not exceeded
            if int(line[1]) > 0: #Check that the element to randomise is not 0
                randomNumber = randint(0,int(line[1])) #Give a random number between 0 and the number of reads in the counts file
                if(int(maxReads - randomNumber) > 0): #Check that the random number does not exceed the max. number when close to the specified threshold
                    print(line[0]+"\t"+str(randomNumber)) #Print gene and random number
                    maxReads = maxReads - randomNumber #Subtract the random number from the max reads
                else:
                    print(line[0]+"\t"+str(maxReads)) #If the random number would exceed the max number of reads, just specify the remaining reads available
                    maxReads = maxReads - maxReads #maxReads falls to 0
            else:
                print(line[0]+"\t"+line[1]) #If 0 reads were mapped, give 0 reads back
        else:
            print(line[0]+"\t"+str(maxReads)) #If the maximal number of reads has been reached only give 0
    else:
        pass

