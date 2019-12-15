#!/bin/bash
###PBS -q debug
#PBS -q standby
###PBS -q testqueue
###PBS -q training
####PBS -l nodes=1:ppn=1
####PBS -l procs=1
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:20:00
###PBS -m ae   ## email onabort and exit
#PBS -m n   ## no email
###PBS -M < your email here >
#PBS -N LNC108

echo -n "START AT "; date
module load lang/python/2.7.15_gcc82
cd /users/jrm0122/RunLncADeep
source venv/bin/activate     # virtual environment with paths to python libraries
cd /scratch/jrm0122/RunLncADeep/Run.108

echo My Task $PBS_ARRAYID
if [[ "x${PBS_ARRAYID}x" == "xx" ]] ; then
    echo Please run this as a task array e.g. qsub -t 1-10
    exit 1
fi
MYFILE="mutantsOfSeq.${PBS_ARRAYID}.fasta"
echo My File $MYFILE
MYOUTPUT="classificationsOfSeq.${PBS_ARRAYID}.txt"
echo My Output $MYOUTPUT

ls -l
if [ ! -f "${MYFILE}" ]; then
    echo "Missing $MYFILE FASTA."
    exit 2
fi
if [ ! -f "LncADeep.py" ]; then
    echo "Missing LncADeep program."
    exit 3
fi
echo python LncADeep.py --MODE lncRNA --fasta $MYFILE --species human --model full --out $MYOUTPUT
     python LncADeep.py --MODE lncRNA --fasta $MYFILE --species human --model full --out $MYOUTPUT
echo -n $?; echo " exit status LncADeep"
ls -l
echo CLEANUP
mv -nv ${MYOUTPUT}_LncADeep_lncRNA_results/${MYOUTPUT}_LncADeep.results ${MYOUTPUT}
rm -rf ${MYOUTPUT}_LncADeep_lncRNA_results
ls -l

echo -n "FINISH AT ";  date
