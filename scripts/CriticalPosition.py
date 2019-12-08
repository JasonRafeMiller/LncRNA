import argparse
import traceback
import os
import csv

class CriticalPosition:
    scorefile=""
    database=[]

    def __init__ (self,fn):
        self.scorefile=fn
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

    def start_output(self):
        filename=self.output_filename
        seq=str(self.input_num)
        seqname=self.input_id
        newline="\n"
        # Open and truncate the output file
        with open(filename,"w") as outfile:
            defline=">original.ofSeq."+seq+" "+seqname
            outfile.write(defline)
            outfile.write(newline)
            outfile.write(self.input_seq) 
            outfile.write(newline)

    def write_mutants(self):
        filename=self.output_filename
        seq=str(self.input_num)
        seqname=self.input_id
        newline="\n"
        # Open and append to the output file
        with open(filename,"a+") as outfile:
            mut = 0
            while mut < len(self.mutant_seqs_from_one_input_seq):
                defline=">mutant."+str(mut)+".ofSeq."+seq+" "+seqname
                outfile.write(defline)
                outfile.write(newline)
                mutant=self.mutant_seqs_from_one_input_seq[mut]
                outfile.write(mutant) 
                outfile.write(newline)
                mut = mut+1

    def compute_all(self):
        print ("Computing...")

    def write_all(self):
        print ("Writing...")

    def arg_parser():
        parser = argparse.ArgumentParser(description="Determine position with maximum effect on classification.")
        parser.add_argument('scorefile', help='three-column text file', type=str)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()

    def demo(self):
        pass

if __name__ == '__main__':
    try:
        CriticalPosition.arg_parser()
        cp = CriticalPosition(args.scorefile)
        cp.load_all()
        cp.compute_all()
        cp.write_all()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
