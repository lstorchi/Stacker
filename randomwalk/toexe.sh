
ln -s ../computedj.py .
ln -s ../convert_boundary_cond.py .

for i in $(seq 1 10)
do
  python convert_boundary_cond.py -f electrons_"$i"_of_10.txt -d "527.82203:527.37773:501.25099" > electrons_"$i".txt
done

export TIME=$(grep "Total run time:" *.out | awk '{print $4}')

python computedj.py -f "electrons_1.txt:electrons_2.txt:electrons_3.txt:electrons_4.txt:electrons_5.txt:electrons_6.txt:electrons_7.txt:electrons_8.txt:electrons_9.txt:electrons_10.txt" -t $TIME

echo $TIME
