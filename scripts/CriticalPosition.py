import argparse
import traceback
import os
import csv

class CriticalPosition:
    scorefile=""
    positionfile=""
    database=[]

    def __init__ (self,inf,outf):
        self.scorefile=inf
        self.positionfile=outf
        self.database=[]

    def grow_db (self,seqnum):
        while seqnum>=len(self.database):
            self.database.append({})            

    def load_original (self,seqnum,score,classification):
        self.grow_db(seqnum)
        datum=self.database[seqnum]
        datum['original_score']=score
        datum['original_class']=classification

    def load_mutant (self,seqnum,position,score,classification):
        datum=self.database[seqnum]
        if not datum:
            print ("ERROR! MUTANT BEFORE ORIGINAL. SEQNUM={}".format(seqnum))
            exit(1)
        save=False
        if 'mutant_class' not in datum:
            save=True
            # This is the first mutant seen
        else:
            original_score=datum['original_score']=score
            mutant_score=datum['mutant_score']
            this_difference=abs(original_score-score)
            prev_difference=abs(original_score-mutant_score)
            if this_difference > prev_difference:
                save=True
        if save:
            datum['mutant_score']=score
            datum['mutant_class']=classification
            datum['mutant_position']=position

    def load_all(self):
        print ("Loading...")
        seqnum=-1
        with open(self.scorefile,"r") as infile:
            tsvin = csv.reader(infile, delimiter='\t')
            for oneline in tsvin:
                seqid=oneline[0]
                score=float(oneline[1])
                classification=oneline[2]
                idwords=seqid.split('.')
                is_original=(idwords[0]=="original")
                if is_original:
                    seqnum=int(idwords[2])  # string like original.ofSeq.0
                    self.load_original(seqnum,score,classification)
                else:
                    seqnum=int(idwords[3])  # string like mutant.0.ofSeq.0
                    position=int(idwords[1])  # string like mutant.0.ofSeq.0
                    self.load_mutant(seqnum,position,score,classification)

    def write_all(self):
        print ("Writing...")
        fn=['sequence','original_score','original_class','mutant_position','mutant_score','mutant_class']
        with open(self.positionfile,"w") as outfile:
            tsvout = csv.writer(outfile, delimiter='\t')
            i=0
            while i < len(self.database):
                datum=self.database[i]
                if datum:
                    tsvout.writerow((i,datum['original_score'],datum['original_class'],
                                     datum['mutant_position'],datum['mutant_score'],
                                     datum['mutant_class']))
                i=i+1

    def arg_parser():
        parser = argparse.ArgumentParser(description="Determine position with maximum effect on classification.")
        parser.add_argument('scorefile', help='tsv input file', type=str)
        parser.add_argument('positionfile', help='tsv output file', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()

    def demo(self):
        pass

if __name__ == '__main__':
    try:
        CriticalPosition.arg_parser()
        cp = CriticalPosition(args.scorefile,args.positionfile)
        cp.load_all()
        cp.write_all()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
