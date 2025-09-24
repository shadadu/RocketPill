#!/usr/bin/env bash
solver=$1
case=$2
np=${3:-4}
mpirun -np $np $solver -case $case
