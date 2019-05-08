#!/bin/bash

for i in {1..30}
do
   echo Starting worker $i
   ./run-newman-tests.sh &> /dev/null &
done

echo "Waiting for newman processes to exit."

wait

