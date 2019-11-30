import argparse
import traceback
import os

class Perturbation:
    BASES = list("ACGTACGT")
    seq_filename = ""
    input_seqs=[]
    input_ids=[]
    mutant_seqs_from_one_input_seq=[]

    def __init__ (self,fn):
        self.seq_filename=fn

    def mutate_base (self,base,offset):
        '''Offset must be in 0123, base must be in ACGT. A+1=C, etc.'''
        # At offset=1, A->C, C->G, G->T, T->A 
        pos = self.BASES.index(base)
        mut = self.BASES[pos+offset]
        return mut

    def mutate_all_positions(self,seq_index):
        # Assume string contains only ACGT.
        # Use one tight loop to minimize string/chararray conversions.
        # Load list of mutated strings.
        self.mutant_seqs_from_one_input_seq=[]
        string=self.input_seqs[seq_index]
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

    def load_one(self,seq_id,sequence):
        if (len(seq_id)>0 and len(sequence)>0):
            self.input_ids.append(seq_id)
            self.input_seqs.append(sequence)

    def load_all(self):
        self.input_seqs=[]
        self.input_ids=[]
        seq_name=""
        seq_parts=[]
        seq_full=""
        with open(self.seq_filename,"r") as infile:
            for oneline in infile:
                oneline=oneline.rstrip()
                if (oneline.startswith(">")):
                    seq_full=''.join(seq_parts)
                    self.load_one(seq_name,seq_full)
                    seq_name=oneline[1:]
                    seq_parts=[]
                    seq_full=""
                else:
                    seq_parts.append(oneline)
            seq_full=''.join(seq_parts)
            self.load_one(seq_name,seq_full)

    def write_mutants(self,seq_index):
        filename="mutantsOfSeq."+str(seq_index)+".fasta"
        seqname=self.input_ids[seq_index]
        newline="\n"
        with open(filename,"w") as outfile:
            mut = 0
            while mut < len(self.mutant_seqs_from_one_input_seq):
                defline=">mutant."+str(mut)+".ofSeq."+str(seq_index)+" "+seqname
                outfile.write(defline)
                outfile.write(newline);
                mutant=self.mutant_seqs_from_one_input_seq[mut]
                outfile.write(mutant) 
                outfile.write(newline);
                mut = mut+1

    def write_all_mutants(self):
        seq=0
        while seq < len(self.input_ids):
            print("Writing #{}\n".format(seq))
            self.mutate_all_positions(seq)
            self.write_mutants(seq)
            seq = seq+1

    def arg_parser():
        parser = argparse.ArgumentParser(description="Description.")
        parser.add_argument('fasta', help='FASTA filename', type=str)
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
        pt = Perturbation(args.fasta)
        pt.load_all()
        pt.write_all_mutants()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
