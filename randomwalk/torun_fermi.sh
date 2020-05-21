time python rwfromtraps.py -f fullsimulatedfilm.out --num-of-electrons 100 -n 10000 -e "2937:-3.526656:10.0;2938:-3.432025:10.0;2939:-3.363308:10.00;2940:-3.322555:10.0" -F -5.139013 --min-dist 100.0 -v 1> 10ele_10000step.out 2> 10ele_10000step.err &

for i in $(seq 100 100 1000)
do
  VAL=$(./boundary_cond.sh 100 $i)
  echo $i $VAL
done

