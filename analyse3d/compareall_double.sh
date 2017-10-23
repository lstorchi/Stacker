for i in {0..39}
do 
  export name1=$(ls ./step8/cluster_"$i"_*_opt.xyz)  
  export name2=$(ls ./step8/cluster_"$i"_*.xyz)
  
  for n in $name2
  do
    python checkrmsd.py $name1 $n
  done

done
