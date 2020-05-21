if [ "$#" -ne 2 ]; then
  echo "usage: " $0 " numofelectrons stepstocheck"
  exit
fi

XVAL=$(grep "Traps X max: "  *.out | awk '{print $4}')
YVAL=$(grep "Traps Y max: "  *.out | awk '{print $4}')
ZVAL=$(grep "Traps Z max: "  *.out | awk '{print $4}')

#echo $XVAL, $YVAL, $ZVAL

for i in $(seq 1 $1)
do
  python3 convert_boundary_cond.py -f electrons_"$i"_of_"$1"_at_step_"$2".txt -d "$XVAL:$YVAL:$ZVAL" > electrons_"$i"_atstep_"$2".txt
done

LISTA=$(ls electrons_*_atstep_"$2".txt | xargs | sed "s/\ /:/g")

python3 computedj.py -f "$LISTA" -t 100.0 
