import argparse
import traceback
import os
import csv

class Intersection:
    fastafile=""
    index_to_seqid=[]
    seqid_to_index={}

    def __init__ (self,fasta):
        self.fastafile=fasta
        self.index_to_seqid=[]
        self.seqid_to_index={}

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


    def arg_parser():
        parser = argparse.ArgumentParser(description="List annotations per critical position.")
        parser.add_argument('fastafile', help='fasta input file', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()


if __name__ == '__main__':
    try:
        Intersection.arg_parser()
        it = Intersection(args.fastafile)
        it.parse_sequence_ids()

    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
