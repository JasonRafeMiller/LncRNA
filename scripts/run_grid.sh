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
source venv/bin/activate     # virtual environment with paths to python libraries
cd /scratch/jrm0122/RunLncADeep/Run.001
echo My Task $PBS_ARRAYID
if [[ "x${PBS_ARRAYID}x" == "xx" ]] ; then
    echo Please run this as a task array e.g. qsub -t 1-10
    exit 1
fi

MYFILE=min200.lncRNA.fasta   # gencode lncRNA len>=200
MYFILE=subset1.fasta     # subset for testing

MYSIZE=500     # sequences per grid job
MYSIZE=5     # tiny size for testing

MYSTART=$(( ${PBS_ARRAYID}-1 ))   # first sequence given array ID
MYSTART=$(( ${MYSTART} * ${MYSIZE} ))   # first sequence given array ID
MYSUBSET=my.${PBS_ARRAYID}.fasta           # input fasta for one job
MYOUTPUT=my.${PBS_ARRAYID}.out             # output directory for one job
echo MYSTART $MYSTART
echo MYSUBSET $MYSUBSET
echo MYOUTPUT $MYOUTPUT

echo Extract my group of sequences
echo "python fasta_extractor.py $MYFILE $MYSTART $MYSIZE $MYSUBSET"
     python fasta_extractor.py $MYFILE $MYSTART $MYSIZE $MYSUBSET
echo -n $?; echo " exit status"
ls -l

echo Process the subset
echo python LncADeep.py --MODE lncRNA --fasta $MYSUBSET --species human --model full --out $MYOUTPUT
     python LncADeep.py --MODE lncRNA --fasta $MYSUBSET --species human --model full --out $MYOUTPUT
echo -n $?; echo " exit status"
ls -l

echo -n "FINISH AT ";  date
