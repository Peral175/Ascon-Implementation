#!/bin/bash

nr_traces=2098
key=abcdefghABCDEFGH
#key='0123456789:;<=>?'

## 1. run aes with key as cmd argument
python3 aes.py -K $key

# 2. mv bin to circuits folder
mv ./bin/aes2* ./circuits/
mkdir -p ./traces/$key

## 3. traces
wboxkit.trace -T $nr_traces circuits/aes2-clear.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw2.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw3.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw4.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-isw5.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-minq.bin traces/$key
wboxkit.trace -T $nr_traces circuits/aes2-quadlin2.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/aes2-quadlin3.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/aes2-quadlin4.bin traces/$key
#wboxkit.trace -T $nr_traces circuits/aes2-quadlin5.bin traces/$key

## 4. run exact attack
#printf '\nExact attack on aes with 2 rounds.'
#
#printf "\nClear:"
#r="$(sage AES_ExactMatch.py traces/$key/aes2-clear/ -T 256)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
#
#printf '\nISW-2:'
#r="$(sage AES_ExactMatch.py traces/$key/aes2-isw2/ -T 256)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
#
#printf '\nMinq:'
#r="$(sage AES_ExactMatch.py traces/$key/aes2-minq/ -T 256)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
#
#printf '\nLDA on aes with 2 rounds and no constant addition.'
#printf '\nClear:'
#r="$(sage AES_LDA.py traces/$key/aes2-clear/ -T 128 -W 100 -S 100)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
#
#printf '\nISW-2:'
#r="$(sage AES_LDA.py traces/$key/aes2-isw2/ -T 200 -W 192 -S 192)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
#
#printf '\nISW-3:'
#r="$(sage AES_LDA.py traces/$key/aes2-isw3/ -T 512 -W 500 -S 250)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi

#printf '\nMinq:'
#r="$(sage ASCON_LDA.py traces/$key/aes2-minq/ -T 512 -W 500 -S 250)"
#if [[ $r == *$key* ]]; then
#    printf "key match!"
#    echo "$r"
#else
#    printf "key does not match!"
#    echo "$r"
#fi
