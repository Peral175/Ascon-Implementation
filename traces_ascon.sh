#!/bin/bash

nr_traces=2048

wboxkit.trace -T $nr_traces circuits/ascon128_r1-clear.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-isw_4.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-minq.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r1-ql4.bin traces/

wboxkit.trace -T $nr_traces circuits/ascon128_r2-clear.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-isw_4.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-minq.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r2-ql4.bin traces/

wboxkit.trace -T $nr_traces circuits/ascon128_r8-clear.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-isw_4.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-minq.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql2.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql3.bin traces/
wboxkit.trace -T $nr_traces circuits/ascon128_r8-ql4.bin traces/

