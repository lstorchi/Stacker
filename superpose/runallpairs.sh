for name in *.xyz 
do  
  for name1 in *.xyz 
  do 
    if [ $name != $name1 ]
    then 
      python supepose.py $name $name1 
    fi 
  done 
done
