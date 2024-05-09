#!/bin/bash

nr_traces=512
key=abcdefghijklmnopqrstuvwxyz1234567890ABCD

## 1. run ascon128-circkit.py with key as cmd argument
#python3 ascon128-circkit.py -K $key
#
## 2. mv bin to circuits folder
#mv ./bin/ascon128_* ./circuits/
#mkdir -p ./traces/$key

# 3. traces
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-clear.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_2.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_3.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_4.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-minq.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql2.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql3.bin traces/
##wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-clear.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_4.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-minq.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql4.bin traces/$key

# 4. run exact attack
#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-clear/ -T 128
#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-isw_2/ -T 128
#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-minq/ -T 128

echo '\nExact attack on ascon with 2 rounds and no constant addition.'

r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-clear/ -T 128)"
if [ "$r" = "$key" ]; then
    echo "key match! Key: " $r
else
    echo "key does not match! Key: " $r
fi

r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-isw_2/ -T 128)"
if [ "$r" = "$key" ]; then
    echo "key match! Key: " $r
else
    echo "key does not match! Key: " $r
fi

#r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-minq/ -T 128)"

echo '\nLDA on ascon with 2 rounds and no constant addition.'

r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-clear/ -T 64 -W 32 -S 1 -F 1)"
if [ "$r" = "$key" ]; then
    echo "key match! Key: " $r
else
    echo "key does not match! Key: " $r
fi

r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-isw_2/ -T 64 -W 32 -S 2 -F 2)"
if [ "$r" = "$key" ]; then
    echo "key match! Key: " $r
else
    echo "key does not match! Key: " $r
fi

r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-isw_3/ -T 64 -W 16 -S 2 -F 3)"
if [ "$r" = "$key" ]; then
    echo "key match! Key: " $r
else
    echo "key does not match! Key: " $r
fi