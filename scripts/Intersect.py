import argparse
import traceback
import os
import csv
import sys

class Intersection:
    fastafile=""
    annofile=""
    critfile=""
    index_to_seqid=[]
    seqid_to_index={}
    annotation_per_transcript={}

    def __init__ (self,fasta,anno,crit):
        self.fastafile=fasta
        self.annofile=anno
        self.critfile=crit
        self.index_to_seqid=[]
        self.seqid_to_index={}
        self.annotation_per_transcript={}

    def parse_sequence_ids(self):
        index = 0
        with open(self.fastafile,"r") as infile:
            for oneline in infile:
                oneline=oneline.rstrip()
                if (oneline.startswith(">")):
                    seqid = oneline[1:]
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

    def parse_positions(self):
        HEADER=0
        line=0
        with open(self.critfile,"r") as infile:
            tsvin = csv.reader(infile, delimiter='\t')
            for oneline in tsvin:
                if line>HEADER:
                    seqnum=int(oneline[0])
                    position=int(oneline[1])
                    self.deconvolve(seqnum,position)
                line=line+1

    def deconvolve(self,sn,ps):
        sid=self.index_to_seqid[sn]
        print("{} NO_ANNOTATION".format(sid))
        if sid in self.annotation_per_transcript:
            print("{} ANNOTATION".format(sid))            
            ann=self.annotation_per_transcript[sid]
            for one_ann in ann:
                name=one_ann[0]
                trstart=one_ann[1]
                trend=one_ann[2]
                if ps >= trstart and ps <= trend:
                    print("{} {}".format(sid,name))            

    def arg_parser():
        parser = argparse.ArgumentParser(description="List annotations per critical position.")
        parser.add_argument('fastafile', help='fasta input file', type=str)
        parser.add_argument('annofile', help='annotation input file', type=str)
        parser.add_argument('critfile', help='critical position input file', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()


if __name__ == '__main__':
    try:
        Intersection.arg_parser()
        it = Intersection(args.fastafile,args.annofile,args.critfile)
        sys.stderr.write("Parsing fasta...")
        it.parse_sequence_ids()
        sys.stderr.write("Parsing annotation...")
        it.parse_annotations()
        sys.stderr.write("Parsing critical positions...")
        it.parse_positions()

    except Exception as e:
        sys.stderr.write("\nERROR!\n")
        if args.debug:
            sys.stderr.write(traceback.format_exc())
        else:
            sys.stderr.write('Run with --debug for traceback.')
    
