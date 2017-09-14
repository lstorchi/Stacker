for i in {0..39}
do 
  export name1=$(ls cluster_"$i"_*_*.xyz)  
  export name2=$(ls cluster_"$i".xyz) 
  
  python checkrmsd.py $name1 $name2 

done
