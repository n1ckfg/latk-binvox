#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR

INPUT_DIR=$1

DIMS=$2

rm "$INPUT_DIR"/*.seg
rm "$INPUT_DIR"/*.im
rm "$INPUT_DIR"/*.binvox

for INPUT in "$INPUT_DIR"/*.latk
do
  python3 test.py -- $INPUT $DIMS
done

cd "$INPUT_DIR"

mkdir hdf5
mv *.im hdf5
mv *.seg hdf5
zip -r hdf5.zip hdf5

mkdir binvox
mv *.binvox binvox
zip -r binvox.zip binvox
