for i in {0..39}
do 
  > out."$i" 

  for name in $(ls ../../step4/"$i"_near/)
  do 
    python checkrmsd.py ../../step4/"$i"_near/"$name"  ./cluster_"$i".xyz  >> out."$i"
  done

  export TOCPY=$(sort -k 3 -g out."$i"  | head -n 1 | awk '{print $1}')
  cp $TOCPY ./
done

