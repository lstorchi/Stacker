for i in {0..39}
do 
  export name=$(ls ./step8/cluster_"$i"_*_*.xyz | grep -v opt)  

  python nanoparticle_splitsurface_count_xyz.py ./step8/"$i".txt $name

done
