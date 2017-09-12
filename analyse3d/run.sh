for i in {0..39}
do 
  export name=$(ls cluster_"$i"_*_*.xyz)  
  
  python nanoparticle_splitatom_count_xyz.py "$i".txt $name

done
