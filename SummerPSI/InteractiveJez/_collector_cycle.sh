#!/bin/bash

echo Input total number of series 
read series
./model_generator 1 $series
for ((i=1; i<=$series; i++))
do
 refgo Preprocess_Inline TestExec_$i
 Str0=`cat temp`
 refc $Str0'.ref'
 refgo Preprocess_Inline Main
 Str1=`cat temp`
 refc $Str1'.ref'
 refgo Preprocess_Inline Heuristics
 Str2=`cat temp`
 refc $Str2'.ref'
 refgo $Str0'+'$Str1'+'$Str2'+Auxiliaries'
rm temp
done
echo The data collecting cycle is completed.
read -s -n 1
