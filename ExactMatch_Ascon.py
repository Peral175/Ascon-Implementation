import argparse
import os.path
import pathlib

import numpy as np

parser = argparse.ArgumentParser(
    description='my implementation of exact matching attack',
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

dict5 = {}
dict4 = {}
dict3 = {}
dict2 = {}
dict1 = {}

for plaintextBits in range(64):
    for keyBitsGuess in range(32):
        guessedVector5 = 0
        guessedVector4 = 0
        guessedVector3 = 0
        guessedVector2 = 0
        guessedVector1 = 0
        for traceNr in range(T):
            tmp = bin(int.from_bytes(PLAINTEXTS[traceNr], byteorder='big'))[2:].zfill(320)
            x0 = tmp[plaintextBits + 0]
            x1 = tmp[plaintextBits + 64]
            x2 = tmp[plaintextBits + 128]
            x3 = tmp[plaintextBits + 192]
            x4 = tmp[plaintextBits + 256]
            x = int(x0 + x1 + x2 + x3 + x4, 2)
            out = selection_function(x, keyBitsGuess)
            guessedVector5 ^= (out >> 4 & 0b1) << traceNr
            guessedVector4 ^= (out >> 3 & 0b1) << traceNr
            guessedVector3 ^= (out >> 2 & 0b1) << traceNr
            guessedVector2 ^= (out >> 1 & 0b1) << traceNr
            guessedVector1 ^= (out >> 0 & 0b1) << traceNr
        dict5[plaintextBits * 32 + keyBitsGuess] = guessedVector5
        dict4[plaintextBits * 32 + keyBitsGuess] = guessedVector4
        dict3[plaintextBits * 32 + keyBitsGuess] = guessedVector3
        dict2[plaintextBits * 32 + keyBitsGuess] = guessedVector2
        dict1[plaintextBits * 32 + keyBitsGuess] = guessedVector1
        # dict5[guessedVector5] = plaintextBits * 32 + keyBitsGuess
        # dict4[guessedVector4] = plaintextBits * 32 + keyBitsGuess
        # dict3[guessedVector3] = plaintextBits * 32 + keyBitsGuess
        # dict2[guessedVector2] = plaintextBits * 32 + keyBitsGuess
        # dict1[guessedVector1] = plaintextBits * 32 + keyBitsGuess
print("Dictionary length: ", len(dict1))

TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]

mostProbableKey = [-1] * 64

v5 = list(dict5.values())
v4 = list(dict4.values())
v3 = list(dict3.values())
v2 = list(dict2.values())
v1 = list(dict1.values())
r5 = []
r4 = []
r3 = []
r2 = []
r1 = []

# for node in range(numOfNodes):
#     nodeVector = 0
#     for traceNumber in range(T):
#         nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber

for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        tmp = bin(int.from_bytes(TRACES[traceNumber], byteorder='big'))[2:].zfill(numOfNodes)
        t = tmp[(node // 5) * 5: (node // 5) * 5 + 5]
        nodeVector ^= (((int(t, 2) >> node % 5) & 0b1) << traceNumber)

    # match1 = dict1.get(nodeVector)
    # if match1 is not None:
    #     r1.append(match1)
    # match2 = dict2.get(nodeVector)
    # if match2 is not None:
    #     r2.append(match2)
    # match3 = dict3.get(nodeVector)
    # if match3 is not None:
    #     r3.append(match3)
    # match4 = dict4.get(nodeVector)
    # if match4 is not None:
    #     r4.append(match4)
    # match5 = dict5.get(nodeVector)
    # if match5 is not None:
    #     r5.append(match5)
    # print(match1, match2, match3, match4, match5)
    while nodeVector in v1:
        idx = v1.index(nodeVector)
        r1.append(idx)
        v1[idx] = -1
    while nodeVector in v2:
        idx = v2.index(nodeVector)
        r2.append(idx)
        v2[idx] = -1
    while nodeVector in v3:
        idx = v3.index(nodeVector)
        r3.append(idx)
        v3[idx] = -1
    while nodeVector in v4:
        idx = v4.index(nodeVector)
        r4.append(idx)
        v4[idx] = -1
    while nodeVector in v5:
        idx = v5.index(nodeVector)
        r5.append(idx)
        v5[idx] = -1

# r1 = sorted(r1, key=lambda z: z[1])
# r2 = sorted(r2, key=lambda z: z[1])
# r3 = sorted(r3, key=lambda z: z[1])
# r4 = sorted(r4, key=lambda z: z[1])
# r5 = sorted(r5, key=lambda z: z[1])
r1 = sorted(r1)
r2 = sorted(r2)
r3 = sorted(r3)
r4 = sorted(r4)
r5 = sorted(r5)
# print(r1[:9], len(r1))
# print(r2[:9], len(r2))
# print(r3[:18:2], len(r3))
# print(r3[1:18:2], len(r3))
# print(r4[:9], len(r4))
# print(r5[:9], len(r5))
print(r1, len(r1))
print(r2, len(r2))
print(r3, len(r3))
print(r4, len(r4))
print(r5, len(r5))

s1 = set(set(set(set(r1).intersection(r2)).intersection(r3)).intersection(r4)).intersection(r5)
print(s1, len(s1))
s3 = sorted(s1)
finall = np.zeros((64, 5), dtype=np.uint8)
ss = ''
for i in range(len(s3)):
    print(s3[i], s3[i] % 32, s3[i] // 32)
    t = bin((s3[i] % 32))[2:].zfill(5)
    ss += t
    for j in range(5):
        finall[i, j] = t[j]
# print(finall)
print(ss)
s = ''
for i in range(0,5,1):
    s += ss[i]
    s += ss[i+5]
    s += ss[i+10]
    s += ss[i+15]
    s += ss[i+20]
    s += ss[i + 25]
    s += ss[i + 30]
    s += ss[i + 35]
    s += ss[i + 40]
    s += ss[i + 45]
    s += ss[i + 50]
    s += ss[i + 55]
    s += ss[i + 60]
    s += ss[i + 65]
    s += ss[i + 70]
    s += ss[i + 75]
    s += ss[i + 80]
    s += ss[i + 85]
    s += ss[i + 90]
    s += ss[i + 95]
    s += ss[i + 100]
    s += ss[i + 105]
    s += ss[i + 110]
    s += ss[i + 115]
    s += ss[i + 120]
    s += ss[i + 125]
    s += ss[i + 130]
    s += ss[i + 135]
    s += ss[i + 140]
    s += ss[i + 145]
    s += ss[i + 150]
    s += ss[i + 155]
    s += ss[i + 160]
    s += ss[i + 165]
    s += ss[i + 170]
    s += ss[i + 175]
    s += ss[i + 180]
    s += ss[i + 185]
    s += ss[i + 190]
    s += ss[i + 195]
    s += ss[i + 200]
    s += ss[i + 205]
    s += ss[i + 210]
    s += ss[i + 215]
    s += ss[i + 220]
    s += ss[i + 225]
    s += ss[i + 230]
    s += ss[i + 235]
    s += ss[i + 240]
    s += ss[i + 245]
    s += ss[i + 250]
    s += ss[i + 255]
    s += ss[i + 260]
    s += ss[i + 265]
    s += ss[i + 270]
    s += ss[i + 275]
    s += ss[i + 280]
    s += ss[i + 285]
    s += ss[i + 290]
    s += ss[i + 295]
    s += ss[i + 300]
    s += ss[i + 305]
    s += ss[i + 310]
    s += ss[i + 315]
print(s, len(s))
xxx = ''
for i in range(0,320,8):
    # print(s[i:i+8], int(s[i:i+8], 2))
    # print(chr(int(s[i:i+8], 2)))
    xxx += chr(int(s[i:i+8], 2))
print(xxx)
# for i in range(64):
#     x = r1[i]%32 ^ r2[i]%32 ^ r3[i*2]%32 ^ r3[i*2+1]%32 ^r4[i]%32 ^ r5[i]%32
#     print(i, x, r1[i]%32, r2[i]%32, r3[i*2]%32,r3[i*2+1]%32, r4[i]%32, r5[i]%32)
#     print(bin(r1[i]%32)[2:].zfill(5),
#           bin(r2[i]%32)[2:].zfill(5),
#           bin(r3[i*2]%32)[2:].zfill(5),
#           bin(r3[i*2+1]%32)[2:].zfill(5),
#           bin(r4[i]%32)[2:].zfill(5),
#           bin(r5[i]%32)[2:].zfill(5))

#     mostProbableKey[i] = x
# print(mostProbableKey)
# for i in mostProbableKey:
#     print(bin(i)[2:].zfill(5))
