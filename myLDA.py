import argparse
import os.path
import pathlib
import numpy as np
from sage.all import *
# from sage.matrix.matrix0 import Matrix
# from sage.modules.free_module_element import vector, ZZ

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

if mode == 0:
    """
    There are N linear shares that together are the key byte.
    We need to solve this with SAGEMATH, vector with 0 meaning that this column is not
    part of the solution.
    How do I know what the correct keybyte is?
    A combination of columns will be equal to the key byte guessed!
    Will there be many solutions?
    """
    AESSBox = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]


    def selection_function(pB, kBG):
        return (AESSBox[pB ^ kBG] & 1)


    PLAINTEXTS = []
    for traceNr in range(T):
        pt = args.trace_dir / ("%04d.pt" % traceNr)
        with open(pt, "rb") as f:
            PLAINTEXTS += [f.read(16)]
    dict = {}
    for bP in range(16):
        for kBG in range(256):
            guessedVector = 0
            for traceNr in range(T):
                guessedVector ^= selection_function(PLAINTEXTS[traceNr][bP], kBG) << traceNr
            dict[guessedVector] = bP * 256 + kBG
    print(len(dict))
TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]

mostProbableKey = [-1] * 16

M = []
S = []

for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
    M.append(nodeVector)

m = np.zeros((T, numOfNodes))
for i in range(numOfNodes):
    for j in range(T):
        curr = M[i]
        bla = bin(curr)[2:].zfill(T)
        m[j,i] = bla[j]
print(m.shape)

# print(m)
dic = list(dict)
# print(dic)
# input()
s = np.zeros((256, T))
for i in range(T):
    for j in range(T):
        curr = dic[i]
        # print(curr.bit_length())
        bla = bin(curr)[2:].zfill(T)
        s[i,j] = bla[j] # size is the problem here
print(s.shape)
# print(s)
# sliding window
w_l = 5
n_l = 256
ctr = 0
# for i in range(n_l - w_l + 1):
#     for j in range(w_l):
#         pass
XXX = []
for i in range(numOfNodes):
    print(i)
    if len(XXX) < w_l:
        XXX.append(m[:, i])
        # print(m)
        # print(m[:, i])
        # input()
    if len(XXX) == w_l:
        # print("XXX", len(XXX))
        mat = Matrix(ZZ, XXX)
        mat = mat.transpose()
        # print(mat.dimensions())
        # input()
        for j in range(256):
            k = vector(ZZ, s[:,j])
            try:
                # print(mat.dimensions(), len(k))
                X = mat.solve_right(k)
                print("X: ", X)
                input()
            except ValueError as e:
                # print(e)
                # input()
                ctr += 1
        XXX.pop(0)
print("Failures: ", ctr)
# if len(VECTORS) < 5:
    #     r = []
    #     for i in bin(nodeVector)[2:].zfill(256):
    #         r += [i]
    #     VECTORS += [r]
    #     # print(VECTORS)
    # if len(VECTORS) == 5:
    #     # matrix stuff here
    #     M = Matrix(ZZ, VECTORS)
    #     print(M.dimensions())
    #     M = M.T
    #     for k in dict:
    #         # print(len(bin(k)[2:]))
    #         K = bin(k)[2:].zfill(256)
    #         # K = bin(i)[2:].zfill(8)
    #         # print(K)
    #         k = vector(ZZ, K)
    #         # print(i, k)
    #         try:
    #             X = M.solve_right(k)
    #             print("X: ", X)
    #             break
    #         except ValueError as e:
    #             continue
    #             # print(e)
    #         # input()
    #
    #     # remove first to slide window further
    #     VECTORS.pop(0)
    #     # print(len(VECTORS))
    #     # print(numOfNodes)   # this is correctly the number of nodes!

    # match = dict.get(nodeVector)
    # if match != None:
    #     print("At node number " + str(node) + ", we have the key byte " + chr((match % 256)))
    #     mostProbableKey[match // 256] = match % 256

# missingBytes = 0
# for i in range(16):
#     if mostProbableKey[i] == -1:
#         missingBytes += 1
# if missingBytes == 0:
#     if mode == 0:
#         print("Most probable key (char): ", end="")
#     for i in range(16):
#         print(chr(mostProbableKey[i]), end="")
#     if mode == 0:
#         print("\n                   (hex): ", end="")
#     for i in range(16):
#         print(hex(mostProbableKey[i])[2:], end="")
#     print()
# else:
#     print("Impossible to find the key: %d bytes are missing" % missingBytes)
#     print("The implementation may be resistant to this attack, but you can still try with more traces")
