#!/bin/bash

refgo Preprocess_Inline $1
Str=`cat temp`
refc $Str'.ref'
refgo $Str'+Auxiliaries'
rm temp
read -s -n 1
