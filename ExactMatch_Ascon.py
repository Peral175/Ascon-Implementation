import argparse
import os.path
import pathlib

import numpy as np

parser = argparse.ArgumentParser(
    description='my implementation of exact matching attack for ASCON',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    'trace_dir',
    type=pathlib.Path,
    help='path to trace directory'
)
parser.add_argument(
    '-T',
    '--n-traces',
    type=int,
    default=256,
    help='nr. traces'
)
parser.add_argument(
    '-M',
    '--mode',
    type=int,
    default=0,
    help='mode'
)
args = parser.parse_args()
T = args.n_traces
numOfBytes = os.path.getsize(args.trace_dir / "0000.bin")
numOfNodes = numOfBytes * 8
mode = args.mode

ASCONSBOX = [0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
             0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17]


def selection_function(ptb, kbg):
    return ASCONSBOX[ptb ^ kbg]


PLAINTEXTS = []
for traceNr in range(T):
    pt = args.trace_dir / ("%04d.pt" % traceNr)
    with open(pt, "rb") as f:
        PLAINTEXTS += [f.read(40)]

dict1, dict2, dict3, dict4, dict5 = {}, {}, {}, {}, {}

for plaintextBits in range(64):
    for keyBitsGuess in range(32):
        guessedVector1, guessedVector2, guessedVector3, guessedVector4, guessedVector5 = 0, 0, 0, 0, 0
        for traceNr in range(T):
            tmp = bin(int.from_bytes(PLAINTEXTS[traceNr], byteorder='big'))[2:].zfill(320)
            x0 = tmp[plaintextBits + 0]
            x1 = tmp[plaintextBits + 64]
            x2 = tmp[plaintextBits + 128]
            x3 = tmp[plaintextBits + 192]
            x4 = tmp[plaintextBits + 256]
            x = int(x0 + x1 + x2 + x3 + x4, 2)
            out = selection_function(x, keyBitsGuess)
            guessedVector1 ^= (out >> 0 & 0b1) << traceNr
            guessedVector2 ^= (out >> 1 & 0b1) << traceNr
            guessedVector3 ^= (out >> 2 & 0b1) << traceNr
            guessedVector4 ^= (out >> 3 & 0b1) << traceNr
            guessedVector5 ^= (out >> 4 & 0b1) << traceNr
        dict1[plaintextBits * 32 + keyBitsGuess] = guessedVector1
        dict2[plaintextBits * 32 + keyBitsGuess] = guessedVector2
        dict3[plaintextBits * 32 + keyBitsGuess] = guessedVector3
        dict4[plaintextBits * 32 + keyBitsGuess] = guessedVector4
        dict5[plaintextBits * 32 + keyBitsGuess] = guessedVector5

TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]

v1 = list(dict1.values())
v2 = list(dict2.values())
v3 = list(dict3.values())
v4 = list(dict4.values())
v5 = list(dict5.values())
r1, r2, r3, r4, r5 = [], [], [], [], []

for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber


    def vectInList(vect, lst, array):  # we are looking for all occurrences!
        while vect in lst:
            index = lst.index(vect)
            array.append(index)
            lst[index] = -1


    vectInList(nodeVector, v1, r1)
    vectInList(nodeVector, v2, r2)
    vectInList(nodeVector, v3, r3)
    vectInList(nodeVector, v4, r4)
    vectInList(nodeVector, v5, r5)

r1 = sorted(r1)
r2 = sorted(r2)
r3 = sorted(r3)
r4 = sorted(r4)
r5 = sorted(r5)

# we want to find the intersection between all 5 lists
intersection = set(set(set(set(r1).intersection(r2)).intersection(r3)).intersection(r4)).intersection(r5)
sorted_intersection = sorted(intersection)
print(sorted_intersection)

try:

    bits_matr = np.zeros((64, 5), dtype=np.uint8)
    for i in range(64):
        bits = bin((sorted_intersection[i] % 32))[2:].zfill(5)
        for j in range(5):
            bits_matr[i, j] = bits[j]
    bits_matr = bits_matr.T

    mostProbableKey = [-1] * 40
    for _ in range(5):
        for j in range(0, 64, 8):
            byte = bits_matr[_][j:j+8]
            s = ''
            for k in byte:
                s += str(k)
            i = int(s, 2)
            mostProbableKey[_*8+j//8] = i

    recovered_key = ''
    for keyByte in mostProbableKey:
        recovered_key += chr(keyByte)
    print("Recovered key: ", recovered_key)
except IndexError:
    print("List is empty!")
