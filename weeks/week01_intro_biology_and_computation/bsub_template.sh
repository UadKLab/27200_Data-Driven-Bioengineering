#!/bin/bash

#BSUB -q hpc
#BSUB -J 27200_w1
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -W 50
#BSUB -o 27200_w1.sh.o%J
#BSUB -e 27200_w1.sh.e%J

#Actual code
echo ”My first HPC job!” > success.txt


