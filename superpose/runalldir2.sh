#1/bin/bash
export V="*"

> lista

for n in {0..39}
do 
  echo $n
  ls "./"$n"_near/"$V >> lista
done

python checkrmsd.py ./lista 
