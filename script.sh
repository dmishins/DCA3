#!/bin/bash
for i in {1..20}
do
echo "Welcome $i times"
python takeBinaryData.py -f COLD/gp10/$i
done


