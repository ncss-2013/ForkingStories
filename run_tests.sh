#!/bin/bash

cd "$(dirname "$0")"

PYTHON="python3.3"
FILES=$(find ./ -iname \*\*.py | grep -v " ")
TESTS=$(grep -l __main__ $FILES | grep -v tornado)

STATUS=0

for TEST in $TESTS; do
  # Get relative paths only (i.e., strip .// from prefix)
  TEST=$(echo $TEST | grep -o -E "\w+.*")

  # If we're a subpackage, run with -w.
  echo $TEST | grep "\/" >/dev/null
  if [ "$?" == "0" ]; then
    PKG=$(echo $TEST | grep -o -E "[^\.]*")
    PKG=$(echo $PKG | sed "s/\//./g")
    $PYTHON -m $PKG >/dev/null
  else
    $PYTHON $TEST >/dev/null
  fi

  if [ "$?" != "0" ]; then
    echo "" >&2
    echo -e "failure: \033[00;31m${TEST}\033[00m"
    STATUS=1
  else
    echo -e "success: \033[00;32m${TEST}\033[00m"
  fi

done

exit $STATUS

