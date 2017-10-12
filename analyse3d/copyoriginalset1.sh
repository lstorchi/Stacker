for i in {0..39}
do 
  > out."$i" 

  for name in $(ls /home/redo/Paper_Stacker/Understand/step4/"$i"_near/)
  do 
    echo $name
    python checkrmsd.py /home/redo/Paper_Stacker/Understand/step4/"$i"_near/"$name" /home/redo/Paper_Stacker/Understand/step6/Set1/cluster_"$i"_out1.xyz  >> out."$i"
  done

  export TOCPY=$(sort -k 3 -g out."$i"  | head -n 1 | awk '{print $1}')
  cp $TOCPY /home/redo/Paper_Stacker/Understand/step6/Set1/
done

