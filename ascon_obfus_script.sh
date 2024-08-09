#!/bin/bash

# set line seperator: \n  (LF)

#nr_traces=2098  # 2048 + 50
nr_traces=4146  # 4096 + 50

key='abcdefghijklmnopqrstuvwxyz1234567890ABCD'

# 1. run Ascon128.py with key as cmd argument
python3 Even_Mansour.py -K $key

# 2. mv bin to circuits folder
mv ./bin/asconP_* ./circuits/

# 3. generate traces
mkdir -p ./traces/$key

wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-clear_obfus.bin traces/$key
wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-isw2_obfus.bin traces/$key
wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-isw3_obfus.bin traces/$key
wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-isw4_obfus.bin traces/$key
wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-minq_obfus.bin traces/$key
wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-ql2_obfus.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-ql3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-ql4.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-cl2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-cl3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/asconP_2R_NCA-cl4.bin traces/$key
