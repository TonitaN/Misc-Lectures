#!/bin/bash

# REFC and REFGO store paths to the compilator and interpreter respectively
$REFC Gen_Eq.ref && $REFGO Gen_Eq.rsl;
$REFC Check_Eq.ref && $REFGO Check_Eq.rsl;

