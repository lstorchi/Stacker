for i in {0..39}
do 
  
  python xyz2vasp-vacuum.py  cluster_"$i".xyz 6 
  diff POSCARcluster_"$i".xyz ./loriano/POSCAR_"$i"
  rm POSCARcluster_"$i".xyz

done
