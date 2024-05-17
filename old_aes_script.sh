#!/bin/bash

nr_traces=300
window_size=256

#echo 'Exact attack on aes2 clear.\n'
#sage ExactMatch_AES.py traces/aes2_clear/ -T $nr_traces -M 0
#
#echo '\nExact attack on aes2 isw masking with 2 linear shares.\n'
#sage ExactMatch_AES.py traces/aes2_isw2/ -T $nr_traces -M 0
#
#echo '\nExact attack on aes2 minq.\n'
#sage ExactMatch_AES.py traces/aes2_minq/ -T $nr_traces -M 0
#
#echo '\nExact attack on aes2 quadlin with 2 linear shares.\n'
#sage ExactMatch_AES.py traces/aes2_quadlin2/ -T $nr_traces -M 0
#
#
#
#echo '\nLDA attack on aes2 clear.\n'
#sage LDA_AES.py traces/aes2_clear/ -T $nr_traces -M 0 -W $window_size -S 1
#
#echo '\nLDA attack on aes2 isw (2 shares).\n'
#sage LDA_AES.py traces/aes2_isw2/ -T $nr_traces -M 0 -W $window_size -S 2
#
#echo '\nLDA attack on aes2 isw (3 shares).\n'
#sage LDA_AES.py traces/aes2_isw3/ -T $nr_traces -M 0 -W $window_size -S 2
#
#echo '\nLDA attack on aes2 isw (4 shares).\n'
#sage LDA_AES.py traces/aes2_isw4/ -T $nr_traces -M 0 -W $window_size -S 2
#
#echo '\nLDA attack on aes2 minq.\n'
#sage LDA_AES.py traces/aes2_minq/ -T $nr_traces -M 0 -W $window_size -S 2
#
#echo '\nLDA attack on aes2 quadlin (2 shares).\n'
#sage LDA_AES.py traces/aes2_quadlin2/ -T $nr_traces -M 0 -W $window_size -S 2

#echo '\nLDA attack on aes2 quadlin (3 shares).\n'
#sage AES_LDA.py traces/aes2_quadlin3/ -T $nr_traces -M 0 -W $window_size -S 1