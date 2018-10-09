#!/usr/bin/env python

import sys
from group import *
from SNP_Matrix import *
from candidates import *
from bioStats import *




if (len (sys.argv)) != 2:
    print sys.argv[0], "inputmatrix"
    sys.exit ()


def stampe(rowsA, rowsB, h1, h2):
    print "alpha = " , h1
    print "beta  = ",  h2
    print " rowsA =",rowsA
    print " rowsB =", rowsB

def comp (a, b):
    return a[2] - b[2]

    


    
    
SNP = SNP_Matrix (sys.argv[1])
SNP.groupsBuild ()
SNP.buildComparMatrix ()
a, b = SNP. reconstruction_Step1_buildPartition ()

#for i in range (len (SNP.groups)):
#    if SNP.groups[i].getSetsSize () == 2:
#        print i,  "TotColl", SNP.groups[i].totCollision, "-",
#        print "ProbErrRows", len (SNP.groups[i].ProbErrRows),
#        print "TotEl", len (SNP.groups[i].sets[0] | SNP.groups[i].sets[1])
#        print "-------------"
        

#print
#print "insiemi delle righe iniziali"
#print a
#print b
h1 = SNP.outputHaplotype (a)
h2 = SNP.outputHaplotype (b)
print a
print b
print h1
print h2
print "Fine primo step"

# End of first step

rowsA = set (a)
rowsB = set (b)
rowsA, rowsB, vCompares = SNP.reconstruction_step2 (rowsA, rowsB)
h1 = SNP.outputHaplotype (rowsA)
h2 = SNP.outputHaplotype (rowsB)
print rowsA
print rowsB
print h1
print h2
print "Fine secondo step"


alpha, beta = SNP.reconstruction_step3 (rowsA, rowsB, vCompares)
if alpha is not None and beta is not None:
    g1 = group (rowsA, rowsB)
    g2 = group (alpha, beta)
    m = g1.getComparMatrix (g2)
    canJoin = g2.detectErrorInGroupWeak  (m, g1)
    if canJoin:
        m = g1.getComparMatrix (g2)
        g1.alpha = 0
        g1.beta = 1
        g1.labeled = True
        g2.labelingGroup ( m , g1, True)
        rowsA = g1.sets[g1.alpha] | g2.sets[g2.alpha]
        rowsB = g1.sets[g1.beta] | g2.sets[g2.beta]

h1 = SNP.outputHaplotype (rowsA, True)
h2 = SNP.outputHaplotype (rowsB, True)
print rowsA
print rowsB
print len (rowsA)
print len (rowsB)
print h1
print h2

print SNP.outputHaplotype2 (rowsA) 
print SNP.outputHaplotype2 (rowsB) 

stats = bioStats (SNP.origM)
#print stats.outputHaplotypeStatistical (rowsA) 
#print stats.outputHaplotypeStatistical (rowsB) 
#
#print
#print stats.outputHaplotypeStatistical2 (rowsA) 
#print stats.outputHaplotypeStatistical2 (rowsB) 

