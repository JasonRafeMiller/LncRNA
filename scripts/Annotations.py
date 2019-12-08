import argparse
import traceback
import os
import csv

class Annotations:
    infile=""
    outfile=""

    def __init__ (self,inf,outf):
        self.infile=inf
        self.outfile=outf

    def parse(self):
        print ("Parsing...")
        seqnum=-1
        with open(self.infile,"r") as infile:
            tsvin = csv.reader(infile, delimiter='\t')
            for oneline in tsvin:
                if not oneline[0].startswith("#") and len(oneline)>=9:
                    print(oneline[8])

    def arg_parser():
        parser = argparse.ArgumentParser(description="Extract intervals from gff3 file.")
        parser.add_argument('infile', help='annotation file (gff3)', type=str)
        parser.add_argument('outfile', help='output file (tsv)', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()

    def demo(self):
        pass

if __name__ == '__main__':
    try:
        Annotations.arg_parser()
        ann = Annotations(args.infile,args.outfile)
        ann.parse()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
