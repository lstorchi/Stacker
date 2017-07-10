#1/bin/bash
export V="*"

for n in {0..39}
do 
  echo $n
  ls "./"$n"_near/"$V > lista
  python checkrmsd.py ./lista 
  mv out1.xyz out2.xyz ./$n"_near"

  echo ""
  echo ""
done
