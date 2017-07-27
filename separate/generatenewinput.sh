rm -f out.xyz out.gen out_selected.xyz

cp "./Shortlist/"$1 ./

python convert.py $1 detailed.out

rm $1

echo "Geometry = GenFormat {"
./xyz2gen out.xyz
cat out.gen
echo "}" 
echo ""
echo "Driver = ConjugateGradient {"
python selectatoms.py out.xyz
echo " MaxForceComponent = 1.0e-4"
echo " MaxSteps = 1000"
echo " OutputPrefix = \"NC.out\""
echo "}"
echo ""
echo "Hamiltonian = DFTB {"
echo "  SCC = Yes"
echo "  SCCTolerance = 1.0e-4"
echo "  MaxSCCIterations = 800"
echo "  Mixer = Broyden {"
echo "    MixingParameter = 0.1"
echo "  }"
echo "  SlaterKosterFiles = Type2FileNames {"
echo "    Prefix = \"/marconi_work/IscrC_THELFIL/dftb+/\""
echo "    Separator = \"-\""
echo "    Suffix = \".skf\""
echo "  }"
echo "  MaxAngularMomentum = {"
echo "    O = \"p\""
echo "    Ti = \"d\""
echo "  }"
echo "  Charge = 0.0"
echo "  SpinPolarisation = {}"
echo "  Filling = Fermi {"
echo "    Temperature [Kelvin] = 0.0"
echo "  }"
echo "}"
echo ""
echo "Options = {"
echo "  WriteDetailedXML = Yes"
echo "  WriteEigenvectors = Yes"
echo "  WriteAutotestTag = NO"
echo "}"
echo ""
echo "ParserOptions = {"
echo "  ParserVersion = 3"
echo "}"
