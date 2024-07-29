#!/bin/bash

# set line seperator: \n  (LF)

#nr_traces=2098  # 2048 + 50
nr_traces=4146  # 4096 + 50

key='abcdefghABCDEFGH'

## 1. run aes with key as cmd argument
python3 aes.py -K $key

# 2. mv bin to circuits folder
mv ./bin/aes2* ./circuits/

## 3. generate traces
mkdir -p ./traces/$key

wboxkit.trace -T $nr_traces circuits/aes2-clear.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-minq.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl4.bin traces/$key


# ---------------------------------------------------------------------------


key='0123456789:;<=>?'

## 1. run aes with key as cmd argument
python3 aes.py -K $key

# 2. mv bin to circuits folder
mv ./bin/aes2* ./circuits/

## 3. traces
mkdir -p ./traces/$key

wboxkit.trace -T $nr_traces circuits/aes2-clear.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-minq.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-ql4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-cl4.bin traces/$key
