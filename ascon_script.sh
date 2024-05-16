#!/bin/bash

nr_traces=512
key=abcdefghijklmnopqrstuvwxyz1234567890ABCD
#key=abcdefghijklmnopqrstabcdefghijklmnopqrst

# 1. run ascon128-circkit.py with key as cmd argument
python3 ascon128-circkit.py -K $key

# 2. mv bin to circuits folder
mv ./bin/ascon128_* ./circuits/
mkdir -p ./traces/$key

# 3. traces
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql4.bin traces/
#
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-clear.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-isw_2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-isw_3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-isw_4.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-minq.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-ql2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-ql3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/ascon128_2R_full-ql4.bin traces/$key

wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-clear.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-isw_4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-minq.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/ascon128_2R_simplified-ql4.bin traces/$key

# 4. run exact attack
echo '\n Exact attack on ascon with 2 rounds and no constant addition.'

#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-clear/ -T 256
#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-isw_2/ -T 256
#sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-minq/ -T 256

echo '\n Clear:'
r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-clear/ -T 256)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n ISW-2:'
r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-isw_2/ -T 256)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n Minq:'
r="$(sage ExactMatch_Ascon.py traces/$key/ascon128_2R_simplified-minq/ -T 256)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n LDA on ascon with 2 rounds and no constant addition.'
echo '\n Clear:'
r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-clear/ -T 128 -W 100 -S 100)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n ISW-2:'
r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-isw_2/ -T 200 -W 192 -S 192)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n ISW-3:'
r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-isw_3/ -T 200 -W 192 -S 192)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi

echo '\n Minq:'
r="$(sage LDA_ASCON.py traces/$key/ascon128_2R_simplified-minq/ -T 200 -W 192 -S 192)"
if [[ $r == *$key* ]]; then
    echo "key match!" $r
else
    echo "key does not match!" $r
fi
