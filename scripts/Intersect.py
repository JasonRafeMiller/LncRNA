import argparse
import traceback
import os
import csv

class Intersection:
    fastafile=""

    def __init__ (self,fasta):
        self.fastafile=fasta

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
        
    except Exception as e:
        print("\nERROR!\n")
        if args.debug:
            print(traceback.format_exc())
        else:
            print ('Run with --debug for traceback.')
    
