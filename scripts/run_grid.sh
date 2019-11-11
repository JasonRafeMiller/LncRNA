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
###PBS -M < your email here >
#PBS -N LNC1
echo -n "START AT "; date
module load lang/python/2.7.15_gcc82
cd /users/jrm0122/RunLncADeep
source venv/bin/activate
cd /scratch/jrm0122/RunLncADeep/Run.001
echo My Task $PBS_ARRAYID
MYFILE=min200.lncRNA.fasta
MYFILE=subset1.fasta     # for testing
MYSIZE=5
MYSTART=( (${PBS_ARRAYID}-1) * $MYSIZE )
MYSUBSET=my.${PBS_ARRAYID}.fasta
MYOUTPUT=my.${PBS_ARRAYID}.out
echo MYSTART $MYSTART
echo MYSUBSET $MYSUBSET
echo MYOUTPUT $MYOUTPUT

echo Extract my group of sequences
echo "python fasta_extractor.py $MYFILE $MYSTART $MYSIZE $MYSUBSET"
     python fasta_extractor.py $MYFILE $MYSTART $MYSIZE $MYSUBSET

echo Process the subset
echo python LncADeep.py --MODE lncRNA --fasta $MYSUBSET --species human --model full --out $MYOUTPUT
     python LncADeep.py --MODE lncRNA --fasta $MYSUBSET --species human --model full --out $MYOUTPUT

echo -n "FINISH AT ";  date
