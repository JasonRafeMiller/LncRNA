import sys

'''
Input: fasta file with each sequence on one line.
Input: sequence number to start with and number to print.
Output: subset fasta file
Example to extract just the first sequence.
$ python extractor.py bigfile.fasta 1 1 > reduced.fasta
'''

filename = sys.argv[1]
start_at = int(sys.argv[2])
group_size = int(sys.argv[3])
with open (filename,'rt') as fastafile:
    even_odd = 0
    num_in = 0
    num_out = 0
    defline = ""
    sequence = ""
    for oneLine in fastafile:
        if even_odd == 0:
            defline = oneLine
            even_odd = 1
        else:
            even_odd = 0
            num_in = num_in + 1
            sequence = oneLine
            if (num_in >= start_at) and (num_out < group_size):
                num_out = num_out + 1
                print defline,
                print sequence,

