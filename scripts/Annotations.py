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
            outs=('tr_id','feature','strand',
                  'genomic_start','genomic_end',
                  'transcriptomic_start','transcriptomic_end')
            tsvout.writerow(outs)            
            # keep genomic start/end and transcriptomic start/end
            this_feature={'gs':0,'ge':0,'ts':0,'te':0}
            prev_exon={'gs':0,'ge':0,'ts':0,'te':0}
            for oneline in tsvin:
                if self.is_data_line(oneline):
                    comments=oneline[8]
                    tr_id=self.extract_transcript(comments)
                    if tr_id:    # genes do not have a transcript id, so ignore them
                        feature=oneline[2]
                        gs=int(oneline[3])
                        ge=int(oneline[4])
                        strand="pos"
                        if oneline[6]=="-":
                            strand="neg"
                        length=ge-gs+1
                        if feature=="transcript":
                            ts=1
                            te=ts+length-1
                            this_feature={'gs':gs,'ge':ge,'ts':ts,'te':te}
                            prev_exon={'gs':0,'ge':0,'ts':0,'te':0}
                        elif feature=="exon":
                            ts=prev_exon['te']+1
                            te=ts+length-1
                            this_feature={'gs':gs,'ge':ge,'ts':ts,'te':te}
                            prev_exon={'gs':gs,'ge':ge,'ts':ts,'te':te}
                        else:
                            ts=prev_exon['ts']+(gs-prev_exon['gs'])
                            te=ts+length-1                        
                            this_feature={'gs':gs,'ge':ge,'ts':ts,'te':te}
                            outs=(tr_id,feature,strand,
                                  this_feature['gs'],this_feature['ge'],
                                  this_feature['ts'],this_feature['te'])
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
    
