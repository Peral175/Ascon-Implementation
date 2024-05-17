#!/bin/bash

nr_traces=256
window_size=256

#echo 'Exact attack on ascon r1 clear.\n'
## modify exact to test this
#sage AES_ExactMatch.py traces/ascon128_r1-clear/ -T $nr_traces -M 0
#
#echo '\nExact attack on ascon r1 isw masking with 2 linear shares.\n'
#sage AES_ExactMatch.py traces/ascon128_r1-isw2/ -T $nr_traces -M 0
#
#echo '\nExact attack on ascon r1 minq.\n'
#sage AES_ExactMatch.py traces/ascon128_r1-minq/ -T $nr_traces -M 0
#
#echo '\nExact attack on ascon r1 quadlin with 2 linear shares.\n'
#sage AES_ExactMatch.py traces/ascon128_r1-ql2/ -T $nr_traces -M 0

#sage LDA_ASCON.py traces/ascon128_r1-clear/ -T $nr_traces -M 0 -W $window_size -S 2
