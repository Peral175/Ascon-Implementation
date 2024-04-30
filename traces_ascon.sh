#!/bin/bash

nr_traces=512

# 1. run ascon128-circkit.py
python3 ascon128-circkit.py

# 2. mv bin to circuits folder
mv ./bin/ascon128_r* ./circuits/

# 3. traces

#wboxkit.trace -T $nr_traces circuits/ascon128_r1-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_r2-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql4.bin traces/

wboxkit.trace -T $nr_traces circuits/ascon128_r3-clear.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-isw_2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-isw_3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-isw_4.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-minq.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-ql2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-ql3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r3-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_r4-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r4-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_r5-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r5-ql4.bin traces/

#wboxkit.trace -T $nr_traces circuits/ascon128_r8-clear.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_4.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-minq.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql2.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql3.bin traces/
#wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql4.bin traces/

# 4. run exact attack
sage ExactMatch_Ascon.py traces/ascon128_r3-clear/ -T 64