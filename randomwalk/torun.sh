time python rwfromtraps.py -f fullsimulatedfilm.out --num-of-electrons 10 -n 10000 -e "2937:-3.526656:10.0;2938:-3.432025:10.0;2939:-3.363308:10.00;2940:-3.322555:10.0" -l 2937 --min-dist 100.0 -v 1> 10ele_10000step.out 2> 10ele_10000step.err &

for i in $(seq 1 10)
do
  python convert_boundary_cond.py -f ./10ele_10000steps/electrons_"$i"_of_10.txt -d "527.82203:527.37773:501.25099" > electrons_"$i".txt
done

python computedj.py -f "electrons_1.txt:electrons_2.txt:electrons_3.txt:electrons_4.txt:electrons_5.txt:electrons_6.txt:electrons_7.txt:electrons_8.txt:electrons_9.txt:electrons_10.txt" -t 2.11300337178e-9
