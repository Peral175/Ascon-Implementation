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

ASCONSBOX = [
    0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
    0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17
]


def selection_function(ptb, kbg):       # this should be correct
    return ASCONSBOX[ptb ^ kbg]


PLAINTEXTS = []
for traceNr in range(T):
    pt = args.trace_dir / ("%04d.pt" % traceNr)
    with open(pt, "rb") as f:
        PLAINTEXTS += [f.read(40)]  # 40 bytes = 320 bits

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
print("Dictionary length: ", len(dict1))  # todo question: duplicates okay or indication of mistake?

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
# values = v1
# print(v1)
# print(v2)
# print(v3)
# print(v4)
# print(v5)
r5 = []
r4 = []
r3 = []
r2 = []
r1 = []

# original: for each trace take one whole byte
for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber

    # for node in range(numOfNodes):
    #     nodeVector = 0
    #     for traceNumber in range(T):
    #         tmp = bin(int.from_bytes(TRACES[traceNumber], byteorder='big'))[2:].zfill(numOfNodes)
    #         t = tmp[(node // 5) * 5: (node // 5) * 5 + 5]        # todo question: 5-bit here instead of 8?
    #         nodeVector ^= ((int(t, 2) >> node % 5) & 0b1) << traceNumber

    # match = dictionary.get(nodeVector)
    # if match != None:

    if nodeVector in v1:
        idx = v1.index(nodeVector)
        match = v1[idx]
        print("1: ", idx, match, idx // 32, idx % 32, node)
        r1.append((idx, idx//32, idx % 32))
    if nodeVector in v2:
        idx = v2.index(nodeVector)
        match = v2[idx]
        print("2: ", idx, match, idx // 32, idx % 32, node)
        r2.append((idx, idx // 32, idx % 32))
    if nodeVector in v3:
        idx = v3.index(nodeVector)
        match = v3[idx]
        print("3: ", idx, match, idx // 32, idx % 32, node)
        r3.append((idx, idx // 32, idx % 32))
        mostProbableKey[idx // 32] = idx % 32
    if nodeVector in v4:
        idx = v4.index(nodeVector)
        match = v4[idx]
        print("4: ", idx, match, idx // 32, idx % 32, node)
        r4.append((idx, idx // 32, idx % 32))
    if nodeVector in v5:
        idx = v5.index(nodeVector)
        match = v5[idx]
        print("5: ", idx, match, idx // 32, idx % 32, node)
        r5.append((idx, idx // 32, idx % 32))
        # if match == 10337942924465290724:
        # while match in values:
        #     idx = values.index(nodeVector)
        #     print(match, idx // 32, idx % 32, idx)
        #     values.remove(match)
        #     input()
        # print(match, match // 32, match % 32, idx)
        # input()
print(mostProbableKey)
r1 = sorted(r1, key=lambda x: x[1])
r2 = sorted(r2, key=lambda x: x[1])
r3 = sorted(r3, key=lambda x: x[1])
r4 = sorted(r4, key=lambda x: x[1])
r5 = sorted(r5, key=lambda x: x[1])
print(r1[:3])
print(r2[:3])
print(r3[:6])
print(r4[:3])
print(r5[:3])
print(len(r1), len(r2), len(r3), len(r4), len(r5))
res = np.zeros((64, 5), dtype=int)
for i in range(64):
    x = r1[i][2] ^ r2[i][2] ^ r3[i*2][2] ^ r3[(i*2)+1][2] ^ r4[i][2] ^ r5[i][2]
    print(i, bin(x)[2:].zfill(5), bin(r2[i][2])[2:].zfill(5), bin(r3[i*2][2])[2:].zfill(5), bin(r3[(i*2)+1][2])[2:].zfill(5))
    for j in range(5):
        res[i, j] = bin(x)[2:].zfill(5)[j]
res = res.T
# print(res, len(res))
st = ''
for j in range(5):
    for i in range(64):
        st += str(res[j, i])
print(st, len(st), int(st, 2), bytes.fromhex(hex(int(st, 2))[2:]))
# 2nd and 3rd 8-bytes are still wrong
assert int(st, 2) == 812512715624816776440459237248810020064558190857236543862207984151981621179302483734224793854305
# Key is b'aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa'
# 01100 00101 10000 10110 00010 11000 01011 00001       # first 5 bytes = 40 bits
#    12,    5,   16,   22,    2,   24,   11,    1
