#!/bin/bash

nr_traces=512

# 1. run ascon128-circkit.py
python3 ascon128-circkit.py

# 2. mv bin to circuits folder
mv ./bin/ascon128_* ./circuits/

# 3. traces
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_1_no_lin_diff-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_2_no_lin_diff-ql4.bin traces/

# 4. run exact attack
sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-clear/ -T 128
sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-isw_4/ -T 128
sage ExactMatch_Ascon.py traces/ascon128_1_no_lin_diff-minq/ -T 128

sage ExactMatch_Ascon.py traces/ascon128_2_no_lin_diff-clear/ -T 128
sage ExactMatch_Ascon.py traces/ascon128_2_no_lin_diff-isw_4/ -T 128
sage ExactMatch_Ascon.py traces/ascon128_2_no_lin_diff-minq/ -T 128