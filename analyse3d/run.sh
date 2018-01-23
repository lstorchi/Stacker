for i in {0..39}
do 
  export name=$(ls ./step6/Set1/cluster_"$i"_*_*.xyz | grep -v opt)  

  python nanoparticle_splitsurface_count_xyz.py ./step6/Set1/"$i".txt $name

done

for i in {0..39}
do 
  export name=$(ls ./step6/Set2/cluster_"$i"_*_*.xyz | grep -v opt)  

  python nanoparticle_splitsurface_count_xyz.py ./step6/Set2/"$i".txt $name

done
