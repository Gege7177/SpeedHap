#!/usr/bin/env python

import sys

def getHDistAndCov (string1, string2):
    """ date due stringhe calcola
    - la distanza di Hamming
    - la copertura, cioe quanto si sovrappongono"""

    if (len (string1) != len (string2)):
        print "Initialization error"
        sys.exit ()

    hDist = 0
    cov = 0
    for i in range (len (string1)) :
        if string1 [i] != "-" and string2 [i] != "-":
            cov += 1
            if string1 [i] != string2 [i]:
                hDist += 1
    return hDist, cov


if __name__ == "__main__":
    if len (sys.argv) != 4:
        print "Usage:", sys.argv[1], "haplotype_1 haplotype_2 snp_results"
        sys.exit ()

    f = open (sys.argv[1])
    H1 = f.readline ()
    f.close ()
    f = open (sys.argv[2])
    H2 = f.readline ()
    f.close ()
    if H1[-1] == "\n":
        H1 = H1[:-1]
    if H2[-1] == "\n":
        H2 = H2[:-1]

    f = open (sys.argv[3])
    s1 = f.readline ()
    s2 = f.readline ()
    f.close ()    
    if s1[-1] == "\n":
        s1 = s1[:-1]
    if s2[-1] == "\n":
        s2 = s2[:-1]


    ham1, cov1 = getHDistAndCov (H1, s1)
    ham2, cov2 = getHDistAndCov (H2, s2)

    Ham1, Cov1 = getHDistAndCov (H2, s1)
    Ham2, Cov2 = getHDistAndCov (H1, s2)


    if ham1 + ham2 > Ham1 + Ham2:
        ham1 = Ham1
        cov1 = Cov1
        ham2 = Ham2
        cov2 = Cov2
    
    print ham1, cov1, ham2, cov2, "-", ham1 + ham2, "-"
