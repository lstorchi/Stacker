for n in {0..39} 
do 
  for name in ./"$n"/* 
  do 
    python extractmindtpair.py $name >> "$n".out 
  done  
done 

for n in {0..39}
do 
  mkdir "$n"_near 
done

for n in {0..39}
do
  for name in $(cat "$n".out)
  do 
    cp -f $name ./"$n"_near/ 
  done
done 


for n in {0..39}
do
 tar -c ./"$n"_near | gzip -c -9 > "$n"_near.tgz 
done

