#!/usr/bin/env python
import sys

### GENERIC
#python script.py ATHALIANA.INPUT.sorted.sam ALBUGO.INPUT.sorted.sam ATHALIANA.OUTPUT.UNIQUE.sorted.sam ATHALIANA.OUTPUT.UNIQUE.sorted.sam

#### SPECIFY NUMBER OF HEADER LINES IN SAM FILES
athaliana=10 #number of SAM header lines to pass
albugo=3830 #number of SAM header lines to pass

#### DICTIONARIES AND SETS
all_reads_d1={}
all_reads_d2={}

export_reads_s1=set()
export_reads_s2=set()


### ATHALIANA READ SET EXTRACTED FROM SAM FILE
print("Building Read Set 1")
ct=0
for seqid in open(sys.argv[1], "r"): #SORTED SAM INPUT
    if int(ct) < int(athaliana): #IGNORE HEADER
        ct += 1
    else:
        seqid=seqid.replace("\n","").split("\t") #SPLIT SAM ENTRIES
        if ("\b"+str(seqid[0])+"\b") not in all_reads_d1: #ADD ONLY SAM FILE READ IDS TO THIS SET
            all_reads_d1["\b"+str(seqid[0])+"\b"] = float(seqid[4])
        else:
            if float(all_reads_d1["\b"+str(seqid[0])+"\b"]) < float(seqid[4]):
                all_reads_d1["\b"+str(seqid[0])+"\b"] = float(seqid[4])
        
### ALBUGO READ SET EXTRACTED FROM SAM FILE
print("Building Read Set 2")
ct=0
for seqid in open(sys.argv[2], "r"): #SORTED SAM INPUT
    if int(ct) < int(albugo): #IGNORE HEADER
        ct += 1
    else:
        seqid=seqid.replace("\n","").split("\t") #SPLIT SAM ENTRIES
        if ("\b"+str(seqid[0])+"\b") not in all_reads_d2: #ADD ONLY SAM FILE READ IDS TO THIS SET
            all_reads_d2["\b"+str(seqid[0])+"\b"] = float(seqid[4])
        else:
            if float(all_reads_d2["\b"+str(seqid[0])+"\b"]) < float(seqid[4]):
                all_reads_d2["\b"+str(seqid[0])+"\b"] = float(seqid[4])

### MATCH READS OF BOTH DICTIONARIES AND EXTRACT UNIQUES INTO THE export_reads_s1 AND export_reads_s2 sets
print("Filtering unique reads between samples")
export_reads_s1 = {str(k1) for k1, v1 in all_reads_d1.iteritems() if k1 not in all_reads_d2}
export_reads_s2 = {str(k1) for k1, v1 in all_reads_d2.iteritems() if k1 not in all_reads_d1}

### MATCH READS OF BOTH DICTIONARIES AND SORT HIGHER ALIGNMENT SCORES INTO THE CORRESPONDING export_reads_s1 AND export_reads_s2 sets
print("Matching MAPQ scores between samples")
for k1, v1 in all_reads_d1.iteritems():
    if k1 in all_reads_d2:
        if float(all_reads_d1[k1]) > float(all_reads_d2[k1]):
            export_reads_s1.add(str(k1))
        elif float(all_reads_d1[k1]) == float(all_reads_d2[k1]):
            pass
        else:
            export_reads_s2.add(str(k1))


print("Filtered Reads: Athaliana")
print(len(export_reads_s1))
print("Filtered Reads: Albugo")
print(len(export_reads_s2))

### ARABIDOPSIS PRINTING
print("Printing Read Set 1")
ct=0
with open(sys.argv[3], "w+") as f1:
    for seqid in open(sys.argv[1], "r"): #SORTED SAM INPUT
        if int(ct) < int(athaliana): #WRITE HEADER
            ct += 1
            f1.write(seqid)
        else:
            seqid=seqid.split("\t") #SPLIT SAM ENTRIES
            if ("\b"+str(seqid[0])+"\b") in export_reads_s1:
                f1.write(str(("\t").join(seqid)))
f1.close()

### ALBUGO PRINTING
print("Printing Read Set 2")
ct=0
with open(sys.argv[4], "w+") as f2:
    for seqid in open(sys.argv[2], "r"): #SORTED SAM INPUT
        if int(ct) < int(albugo): #WRITE HEADER
            ct += 1
            f2.write(seqid)
        else:
            seqid=seqid.split("\t") #SPLIT SAM ENTRIES
            if ("\b"+str(seqid[0])+"\b") in export_reads_s2:
                f2.write(str(("\t").join(seqid)))
f2.close()