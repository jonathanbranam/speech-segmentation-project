#!/usr/bin/env bash

# Usage
# sph-to-wave.sh DIRECTORY PATH-TO-SPH2PIPE [remove-orig]
# DIRECTORY: directory to process
# PATH-TO-SPH2PIPE: path to sph2pipe (if not in your path)
# remove-orig: if specified will remove the original file during processing
# sph-to-wave.sh wsj0-merged ../sph2pipe_v2.5/sph2pipe remove-orig

root_dir="$1"
shift

if [ -z "$1" ]
then
  sphpipe=sph2pipe
else
  sphpipe=$1
  shift
fi

#TODO: make removing original file a proper option

command="echo $sphpipe -f rif \"\$1\" \"\${1%.*}\".wav; $sphpipe -f rif \"\$1\" \"\${1%.*}\".wav"

if [ ! -z "$1" ]
then
  if [ "$1" == "remove-orig" ]
  then
    command="$command && rm \"\$1\""
  fi
fi

find "$root_dir" \( -iname \*.wv1 -o -iname \*.wv2 \) -exec sh -c "$command" _ {} \;
