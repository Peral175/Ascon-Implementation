import argparse
import multiprocessing
import os.path
import pathlib
import numpy as np
from sage.all import *
import multiprocessing as mp
import datetime

from sage.matrix.matrix_mod2_dense import Matrix_mod2_dense

# import timeit

parser = argparse.ArgumentParser(
    description='my implementation of LDA',
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
print("numOfBytes = ", numOfBytes)
print("numOfNodes = ", numOfNodes)

if mode == 0:
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
        return AESSBox[pB ^ kBG] & 1

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
    # print(len(dict), 256*16)
TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]
M = []
for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
    M.append(nodeVector)

len_m = numOfNodes
matr = np.zeros((256, len_m), dtype=int, order='C')
for i in range(len_m):
    c = bin(M[i])[2:].zfill(256)
    for j in range(256):
        matr[j, i] = c[j]
# print(matr.shape)
S = np.ndarray((16, 256, T), dtype=int, order='C')
l_dict = list(dict)
for k in range(0, 4096, 256):
    c = l_dict[k:k+256]
    for m in range(T):
        d = bin(c[m])[2:].zfill(256)
        for n in range(256):
            S[k//256, n, m] = d[n]
# print(S.view())
# print(S.shape)


def work(s, M_matrix, id, numNodes, SOLS):
    # mostProbableKey = [-1] * 16
    w_size = 512
    for i in range(0, numNodes-w_size+1, w_size//4):
        tmp = np.ascontiguousarray(M_matrix[:, i:i+w_size])
        window = matrix(GF(2), tmp)
        for j in range(0, 256, 1):
            K = vector(GF(2), s[:, j])
            try:
                X = window.solve_right(K)
                print("ID: ", id, i, j)
                SOLS[id] = (i, j)
                return
            except ValueError as e:
                continue


SOLS = multiprocessing.Manager().dict()
procs = []
start = datetime.datetime.now()
for id in range(2):
    proc = multiprocessing.Process(target=work, args=(S[id, :], matr, id, numOfNodes, SOLS,))
    procs.append(proc)
    proc.start()
for proc in procs:
    proc.join()
end = datetime.datetime.now()
print("Time: ", end - start)
print(SOLS)
# print(SOLS.values())
# print(SOLS.keys())
for i in range(2):
    print(i, '\t', chr(SOLS.get(i)[1]), '\t', SOLS.get(i)[0])
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


#  sage AsconPy/myLDA.py ./wboxkit-main/tutorials/traces/aes2_clear/ -T 256 -M 0
# clear 5825 nodes
# 128 inputs and outputs
# key = abcdefghABCDEFGH

# isw 18022 nodes
