#!/bin/bash

declare executable="./"
declare profile_file="profile"

if [ "$1" == "debug" ]; then 
  python -c pdb $executable
else
  if [ "$1" == "profile" ]; then 
    python -m cProfile -s time  $executable
  else
    python $executable $@
  fi
fi

exit 0
