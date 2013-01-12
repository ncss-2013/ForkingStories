#!/bin/bash

PYTHON="python3.3"
TESTS=$(grep -l __main__ `find ./ -iname \*\.py` | grep -v tornado)

for TEST in $TESTS; do
  # Get relative paths only (i.e., strip .// from prefix)
  TEST=$(echo $TEST | grep -o -E "\w+.*")

  # If we're a subpackage, run with -w.
  echo $TEST | grep "\/" >/dev/null
  if [ "$?" == "0" ]; then
    PKG=$(echo $TEST | grep -o -E "[^\.]*")
    PKG=$(echo $PKG | sed "s/\//./g")
    $PYTHON -m $PKG
  else
    $PYTHON $TEST
  fi

  if [ "$?" != "0" ]; then
    echo -e "failure: \033[00;31m${TEST}\033[00m"
  else
    echo -e "success: \033[00;32m${TEST}\033[00m"
  fi

done

