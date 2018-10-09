#!/usr/bin/env sh

totfrag=100
hamm=-1
totgaps=0.5

for expsize in 100 500 1000
  do
  rm test$expsize.sh
  for coverage in 3 5 8 10
    do
    for err in 0 0.05 0.1 0.15 0.2
      do
      ./genExp.py 100 $totfrag $err $hamm $coverage $expsize Y $totgaps
      x=exp$expsize-tf$totfrag-er$err-h$hamm-c$coverage-Y$totgaps
      echo "echo $x >> test$expsize.res" >> test$expsize.sh
      echo "test.sh $x >> test$expsize.res" >> test$expsize.sh
    done
  done
  chmod +x test$expsize.sh
done