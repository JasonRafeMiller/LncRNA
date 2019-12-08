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

    def is_data_line (self,list_of_fields):        
        if len(list_of_fields)>=9:
            if not list_of_fields[0].startswith("#"):
                return True
        return False

    def extract_transcript(self,col9):
        words=col9.split(';')
        for word in words:
            if word.startswith("ID=ENST"):
                return word[3:]
            if word.startswith("Parent=ENST"):
                return word[7:]
        return None

    def parse(self):
        print ("Parsing...")
        with open(self.infile,"r") as infile, open(self.outfile,"w") as outfile:
            tsvin = csv.reader(infile, delimiter='\t')
            tsvout = csv.writer(outfile, delimiter='\t')
            for oneline in tsvin:
                if self.is_data_line(oneline):
                    comments=oneline[8]
                    transcript=self.extract_transcript(comments)
                    feature=oneline[2]
                    genome_start=oneline[3]
                    genome_end=oneline[4]
                    genome_strand=oneline[6]
                    outs=(transcript,feature,genome_start,genome_end,genome_strand)
                    tsvout.writerow(outs)
                    
                    

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
    
