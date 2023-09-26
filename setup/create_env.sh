#! /bin/bash

while getopts f:n: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
        n) envname=${OPTARG};;
    esac
done
echo "file: $file";
echo "env name: $envname";

conda env create -f $file 
eval "$(conda shell.bash hook)"
conda activate $envname
python -m ipykernel install --user --name=$envname
conda init bash
echo "Activate the environment by opening a new terminal and running: conda activate ${envname}"
echo


