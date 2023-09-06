#!/bin/bash

refgo Preprocess_Inline Exec
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
read -s -n 1
