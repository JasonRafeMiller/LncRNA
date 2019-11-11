#!/bin/bash
###PBS -q debug
#PBS -q standby
###PBS -q testqueue
###PBS -q training
####PBS -l nodes=1:ppn=1
####PBS -l procs=1
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:03:00
###PBS -m ae   ## email onabort and exit
#PBS -m n   ## no email
#PBS -M < your email here >
#PBS -N LNC1
module load lang/python/2.7.15_gcc82
cd /users/jrm0122/RunLncADeep
source venv/bin/activate
cd Run.001

echo -n "START AT "; date
echo Extract the first 10 sequences
python fasta_extractor.py lncRNA_transcripts.fasta 1 10 > subset1.fasta
echo Process the subset
python LncADeep.py --MODE lncRNA --fasta subset1.fasta --species human --model full --out subset1
echo -n "FINISH AT ";  date
