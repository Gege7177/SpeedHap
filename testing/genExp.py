#!/usr/bin/env python

import sys, os

if len (sys.argv) != 9:
    print "Usage:", sys.argv[0], "tot_exp tot_frag err_prob hamming coverage tot_len gapped(Y/N) tot_gaps"
    sys.exit ()

tot_exp = int (sys.argv[1])
tot_frag = sys.argv[2]
err_prob = sys.argv[3]
hamming = sys.argv[4]
coverage = sys.argv[5]
tot_len = sys.argv[6]
gapped = sys.argv[7]
tot_gaps = sys.argv[8]

base_dir = "exp" + tot_len + "-tf" + tot_frag + "-er" + err_prob + "-h" + hamming + \
           "-c" + coverage + "-" + gapped + tot_gaps

os.mkdir (base_dir)
for i in range (tot_exp):
    f = open (base_dir + "/conf" + str (i), "w")
    f.write ("tot_frag = 100\n")
    f.write ("min_len = 3\n")
    f.write ("max_len = 7\n")
    f.write ("err_prob = " + err_prob + "\n")
    f.write ("base_file_name = ./" + base_dir + "/exp" + str (i) + "\n")
    f.write ("hamming = " + hamming + "\n")
    f.write ("coverage = " + coverage + "\n")
    f.write ("tot_len = " + tot_len + "\n")
    f.write ("gapped = " + gapped + "\n")
    f.write ("tot_gaps = " + tot_gaps + "\n")

    f.close ()
