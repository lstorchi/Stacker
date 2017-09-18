
> out

for i in {0..39}
do 
  for name in $(ls ../../step4/"$i"_near/)
  do 
    python checkrmsd.py ../../step4/"$i"_near/"$name"  ./cluster_"$i".xyz  >> out 
  done

  export TOCPY=$(sort -k 3 -n out  | head -n 1 | awk '{print $1}')
  cp $TOCPY ./
done

rm -f out

