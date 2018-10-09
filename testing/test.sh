#!/usr/bin/env sh

for i in `ls --color=no $1/conf* | cut -f2 -d"/" | cut -f2 -d "f" | sort -n`
  do 
  echo $i
  ./snp.py $1/exp$i.dat > $1/exp$i.snp2.all
  cat $1/exp$i.snp2.all | tail -n 2 > $1/exp$i.snp2
  x=`./hdis.py $1/exp$i.h1 $1/exp$i.h2 $1/exp$i.b`
  echo "BASE", $x
  x=`./hdis.py $1/exp$i.h1 $1/exp$i.h2 $1/exp$i.snp2`
  echo "SpeedHAP", $x
done > $1.txt
somma=0
cat $1.txt | grep "BASE" | cut -f2 -d"-" | while read line; do let somma=$somma+$line; echo $somma;  done | tail -n1
somma=0
cat $1.txt | grep "SpeedHAP" | cut -f2 -d"-" | while read line; do let somma=$somma+$line; echo $somma;  done | tail -n1
