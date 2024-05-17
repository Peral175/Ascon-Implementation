#!/bin/bash

nr_traces=1024

#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_clear.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_isw2.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_isw3.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_isw4.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_minq.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_quadlin2.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_quadlin3.bin traces/
#wboxkit.trace -T $nr_traces ../wboxkit-main/tutorials/circuits/aes2_quadlin4.bin traces/

wboxkit.trace -T $nr_traces circuits/aes2_clear.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_isw2.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_isw3.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_isw4.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_minq.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_quadlin2.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_quadlin3.bin traces/
wboxkit.trace -T $nr_traces circuits/aes2_quadlin4.bin traces/

