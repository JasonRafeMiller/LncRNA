import argparse
import traceback
import os
import csv

class Intersection:
    fastafile=""
    annofile=""
    index_to_seqid=[]
    seqid_to_index={}
    annotation_per_transcript={}

    def __init__ (self,fasta,anno):
        self.fastafile=fasta
        self.annofile=anno
        self.index_to_seqid=[]
        self.seqid_to_index={}
        self.annotation_per_transcript={}

    def parse_sequence_ids(self):
        index = 0
        with open(self.fastafile,"r") as infile:
            for oneline in infile:
                #oneline=oneline.rstrip()
                if (oneline.startswith(">")):
                    seqid = oneline[2:]
                    #print("{}={}".format(index,seqid))
                    self.index_to_seqid.append(seqid)
                    self.seqid_to_index[seqid]=index
                    index=index+1

    def parse_annotations(self):
        HEADER=0
        line=0
        with open(self.annofile,"r") as infile:
            tsvin = csv.reader(infile, delimiter='\t')
            for oneline in tsvin:
                if line>HEADER:
                    seqid=oneline[0]
                    classification=oneline[1]
                    trstart=int(oneline[5])
                    trend=int(oneline[6])
                    one_annot=(classification,trstart,trend)
                    if seqid not in self.annotation_per_transcript:
                        self.annotation_per_transcript[seqid]=[]
                    self.annotation_per_transcript[seqid].append(one_annot)
                line=line+1

    def arg_parser():
        parser = argparse.ArgumentParser(description="List annotations per critical position.")
        parser.add_argument('fastafile', help='fasta input file', type=str)
        parser.add_argument('annofile', help='annotation input file', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()


if __name__ == '__main__':
    try:
        Intersection.arg_parser()
        it = Intersection(args.fastafile,args.annofile)
        it.parse_sequence_ids()
        it.parse_annotations()

    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
