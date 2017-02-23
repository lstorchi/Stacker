#! /usr/bin/env python
# original Written by Jules Jacobsen (jacobsen@ebi.ac.uk). Feel free to do whatever you like with this code.
# extensively modified by Robert L. Campbell (rlc1@queensu.ca)

from pymol import cmd
import glob, re

def align_mine(target=None,files=None):
  """
  Aligns all models in a list of files to one target

  usage:
    align_mine [target][files=<filenames>]
        where target specifies the model id you want to align all others against,

    Example:
      align_mine target=name1, files=cluster*.xyz

  """

  file_list = glob.glob(files)
  file_list.sort()
  extension = re.compile( '(^.*[\/]|\.(pdb|ent|brk|xyz))' )
  object_list = []

  rmsd = {}
  rmsd_list = []
  for i in range(len(file_list)):
    obj_name1 = extension.sub('',file_list[i])
    object_list.append(extension.sub('',file_list[i]))
    cmd.load(file_list[i],obj_name1)
    objectname = 'align_%s_on_%s' % (object_list[i],target)
    rms = cmd.align('%s '%(object_list[i]),'%s '%(target),object=objectname)

    rmsd[object_list[i]] = (rms[0],rms[1])
    rmsd_list.append((object_list[i],rms[0],rms[1]))
    cmd.delete(obj_name1)

  print ("Aligning against: %s"%(target))
  for object_name in object_list:
    print ("%s: %6.3f using %d atoms" % (object_name,rmsd[object_name][0],rmsd[object_name][1]))

  for r in rmsd_list:
    print ("%s: %6.3f using %d atoms" % r)

cmd.extend('align_mine',align_mine)
