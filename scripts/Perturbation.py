import argparse
import traceback
import os

class Perturbation:
    BASES = list("ACGTACGT")
    input_filename = ""  # input FASTA filename
    input_num = 0     # sequence number within FASTA, starting with zero
    input_seq = ""
    input_id = ""
    mutant_seqs_from_one_input_seq=[]

    def __init__ (self,fn,off):
        self.input_filename=fn
        self.input_num=off

    def mutate_base (self,base,offset):
        '''Offset must be in 0123, base must be in ACGT. A+1=C, etc.'''
        # At offset=1, A->C, C->G, G->T, T->A 
        pos = self.BASES.index(base)
        mut = self.BASES[pos+offset]
        return mut

    def mutate_all_positions(self):
        # Assume string contains only ACGT.
        # Use one tight loop to minimize string/chararray conversions.
        # Load list of mutated strings.
        self.mutant_seqs_from_one_input_seq=[]
        string=self.input_seq
        offset=1   
        chars = list(string)
        i = 0
        while i < len(chars):
            original = chars[i]
            mutated = self.mutate_base(original,offset)
            chars[i]=mutated
            next_mutant = "".join(chars)
            self.mutant_seqs_from_one_input_seq.append(next_mutant)
            chars[i]=original
            i = i+1

    def shorten(self,id):  
        # Given sequence IDs like this:
        # ENST00000641515.2|ENSG00000186092.6|OTTHUMG00000001094.4|
        # Shorten to this:
        # ENST00000641515.2
        short=id.split('|',1)[0]
        return short

    def load_one(self,seq_id,sequence,seqnum):
        print ("Loading num={} id={}\n".format(seqnum,seq_id))
        self.input_id = self.shorten(seq_id)
        self.input_seq = sequence

    def load_all(self):
        seqnum = -1
        seq_name=""
        seq_parts=[]
        seq_full=""
        loaded=False
        with open(self.input_filename,"r") as infile:
            for oneline in infile:
                oneline=oneline.rstrip()
                if (oneline.startswith(">")):
                    # Before loading this sequence, output the previous one.
                    # Stop reading once we find our target.
                    seq_full=''.join(seq_parts)
                    if seqnum==self.input_num:  
                        self.load_one(seq_name,seq_full,seqnum)
                        loaded=True
                        break
                    # Now start loading this sequence, 
                    # which spans at least 2 lines of input FASTA.
                    seqnum = seqnum+1
                    seq_name=oneline[1:]
                    seq_parts=[]
                    seq_full=""
                else:
                    seq_parts.append(oneline)
            # Last input sequence is a special case.
            if not loaded:
                if seqnum==self.input_num:
                    seq_full=''.join(seq_parts)
                    self.load_one(seq_name,seq_full,seqnum)
                    loaded=True
                else:
                    print ("ERROR: Never found sequence ().\n".format(seqnum))

    def write_mutants(self):
        seq=str(self.input_num)
        filename="mutantsOfSeq."+seq+".fasta"
        seqname=self.input_id
        newline="\n"
        with open(filename,"w") as outfile:
            mut = 0
            while mut < len(self.mutant_seqs_from_one_input_seq):
                defline=">mutant."+str(mut)+".ofSeq."+seq+" "+seqname
                outfile.write(defline)
                outfile.write(newline);
                mutant=self.mutant_seqs_from_one_input_seq[mut]
                outfile.write(mutant) 
                outfile.write(newline);
                mut = mut+1

    def write_all_mutants(self):
        print("Writing mutants of num={} id={}\n".format(self.input_num,self.input_id))
        self.mutate_all_positions()
        self.write_mutants()

    def arg_parser():
        parser = argparse.ArgumentParser(description="Description.")
        parser.add_argument('fasta', help='FASTA filename', type=str)
        parser.add_argument('seqnum', help='seq position within FASTA file, 0-based', type=int)
        parser.add_argument('--debug', help='See tracebacks', action='store_true')
        global args
        args = parser.parse_args()

    def demo(self):
        print("Mutant of A... should be C")
        print(mutate_base ('A',1))
        print("Mutants of ACGTTGCA are...")
        print(mutate_every_position('ACGTTGCA'))

if __name__ == '__main__':
    try:
        Perturbation.arg_parser()
        pt = Perturbation(args.fasta,args.seqnum)
        pt.load_all()
        pt.write_all_mutants()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
