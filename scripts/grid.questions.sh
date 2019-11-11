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
#PBS -N Grid
cd /users/jrm0122/RunLncADeep/Run.001
touch "GridWasHere.txt"
cd /scratch/jrm0122/RunLncADeep/Run.001
touch "GridWasHere.txt"

