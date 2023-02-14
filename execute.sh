#!/bin/bash

set -a
source .env
set +a

for i in $*; do
  if [ $i = "--client1" ]
  then
    python3 -m client.client1 &
  fi
done

python3 -m server $* 
