for i in {0..39}
do 
  export name1=$(ls cluster_"$i".xyz) 
  
  python checkrmsd.py $name1 ../../step5/"$i"_near/out1.xyz 
  python checkrmsd.py $name1 ../../step5/"$i"_near/out2.xyz

done
