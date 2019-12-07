import argparse
import traceback
import os

class Perturbation:
    BASES = list("ACGTACGT")
    input_filename = ""  # input FASTA filename
    input_num = 0     # sequence number within FASTA, starting with zero
    input_seq = ""
    input_id = ""
    output_filename = ""
    mutant_seqs_from_one_input_seq=[]
    mode="SUB"
    maxlen=-1

    def __init__ (self,fn,off,mode,maxlen):
        self.input_filename=fn
        self.input_num=off
        num=str(off)
        self.output_filename="mutantsOfSeq."+num+".fasta"
        self.mode=mode
        self.maxlen=maxlen

    def mutate_base (self,base,offset):
        '''Offset must be in 0123, base must be in ACGT. A+1=C, etc.'''
        # At offset=1, A->C, C->G, G->T, T->A 
        pos = self.BASES.index(base)
        mut = self.BASES[pos+offset]
        return mut

    def substitute_all_positions(self):
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

    def delete_all_positions(self):
        # Assume string contains only ACGT.
        # Use one tight loop to minimize string/chararray conversions.
        # Load list of mutated strings.
        self.mutant_seqs_from_one_input_seq=[]
        string=self.input_seq
        chars = list(string)
        i = 0
        L = len(chars)
        while i < L:
            if i==0:
                temp=chars[i+1:]
            elif i+1 < L:
                temp=chars[:i]+chars[i+1:]
            else:
                temp=chars[:i]
            next_mutant = "".join(temp)
            self.mutant_seqs_from_one_input_seq.append(next_mutant)
            i = i+1

    def shorten(self,id):  
        # Given sequence IDs like this:
        # ENST00000641515.2|ENSG00000186092.6|OTTHUMG00000001094.4|
        # Shorten to this:
        # ENST00000641515.2
        short=id.split('|',1)[0]
        return short

    def load_one(self,seq_id,sequence,seqnum):
        if self.maxlen < 0 or length(self.input_seq) <= self.maxlen:
            print ("Loading num={} id={}\n".format(seqnum,seq_id))
            self.input_id = self.shorten(seq_id)
            self.input_seq = sequence
            return True
        return False

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
                        if self.load_one(seq_name,seq_full,seqnum):
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

    def write_all_mutants(self):
        print("Writing mutants of num={} id={}\n".format(self.input_num,self.input_id))
        if self.mode=="SUB":
            self.substitute_all_positions()
        else:
            self.delete_all_positions()
        self.write_mutants()

    def arg_parser():
        parser = argparse.ArgumentParser(description="Description.")
        parser.add_argument('fasta', help='FASTA filename', type=str)
        parser.add_argument('seqnum', help='seq position within FASTA file, 0-based', type=int)
        parser.add_argument('--maxlen', help='Ignore sequences longer than this', type=int)
        parser.add_argument('--delete', help='Delete rather than mutate', action='store_true')
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
        mode="SUB"
        if args.delete: mode="DEL"
        maxlen=-1
        if args.maxlen: maxlen=args.maxlen
        pt = Perturbation(args.fasta,args.seqnum,mode,maxlen)
        pt.load_all()
        pt.start_output()
        pt.write_all_mutants()
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
