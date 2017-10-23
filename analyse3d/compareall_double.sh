for i in {0..39}
do 
  export name1=$(ls ./step8/cluster_"$i"_*_opt.xyz)  
  export name2=$(ls ./step8/cluster_"$i"_*.xyz)
  export name3=$(ls ./step8/cluster_"$i"_*_*.xyz)
  
  python checkrmsd.py $name1 $name2 
  python checkrmsd.py $name1 $name3

done
