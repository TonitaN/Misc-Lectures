#!/bin/bash

refgo Preprocess_Inline Visualize
Str=`cat temp`
refc $Str'.ref'
refgo $Str'+Auxiliaries' $1
rm temp
read -s -n 1
