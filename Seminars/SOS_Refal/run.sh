refgo GrammarGen+Auxiliaries $1 $2 -l1024 -V4 -nt -C4 -c528
if [[ -f Generated_Grammar.ref ]]
  then
  echo '==== GENERATED GRAMMAR ===='
  cat Generated_Grammar.ref
  read -s -n 1
  refc Generated_Grammar.ref
  echo 'Checker result:'
  refgo Generated_Grammar+PrintTree -l1024 -V4 -nt -C4 -c528
  if [[ -f ParseTree.dot ]]
  then
  dot -Tpng ParseTree.dot > ParseTree.png
  cat ParseTree.dot
  rm ParseTree.dot 
  fi
  rm Generated_Grammar.ref
  rm Generated_Grammar.rsl
fi
read -s -n 1