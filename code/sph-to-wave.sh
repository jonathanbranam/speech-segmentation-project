#!/usr/bin/env bash

# find "$1" \( -iname \*.wv1 -o -iname \*.wv2 \) -exec sh -c 'echo sph2pipe -f rif "$1" "${1%.*}".wav' _ {} \;

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
