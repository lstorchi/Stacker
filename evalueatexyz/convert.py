import re

fp = open("lista.txt")

i = 1
for l in fp:
  print ("MODEL  %4d\n"%i)
  lf = re.sub('[^a-zA-Z0-9-_*.]', '', l)
  fpdb = open(lf)
  for a in fpdb:
   if a.find("HETATM") != -1:
     print re.sub('\n', '', a)
  fpdb.close()
  print "ENDMDL"
  i = i + 1

fp.close()
