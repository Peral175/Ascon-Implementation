import argparse
import multiprocessing
import os.path
import pathlib
import numpy as np
from sage.all import *
import multiprocessing as mp
import datetime

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
    ASCONSBOX = [
        0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
        0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17]     # 16 * 2

    def selection_function(pB, kBG):
        # print(pB, kBG)
        # input()
        return ASCONSBOX[pB ^ kBG] & 1

    PLAINTEXTS = []
    for traceNr in range(T):
        pt = args.trace_dir / ("%04d.pt" % traceNr)
        with open(pt, "rb") as f:
            PLAINTEXTS += [f.read(40)]
    print("PLAINTEXTS = ", len(PLAINTEXTS))
    # print(PLAINTEXTS)
    dict = {}
    for bP in range(64):    # plaintext is 320 bits inputs of 5-bits = 64
        for kBG in range(32):   # key is 320 bits - we consider input of size 32-bits
            guessedVector = 0
            for traceNr in range(T):    # 256 traces
                tmp = bin(int.from_bytes(PLAINTEXTS[traceNr], byteorder='big'))[2:].zfill(320)[(bP*5):(bP*5)+5]
                guessedVector ^= selection_function(int(tmp, 2), kBG) << traceNr
            dict[bP * 32 + kBG] = guessedVector # had to inverse because of duplicates
            # print(len(dict), guessedVector,bP * 32 + kBG)
    print("X", len(dict))       # should be 2048 ? --> see above
TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]
M = []
for node in range(numOfNodes):      # todo: problem here maybe ?
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
    M.append(nodeVector)
print("M =", len(M))
len_m = numOfNodes
matr = np.zeros((T, len_m), dtype=int, order='C')
for i in range(len_m):
    c = bin(M[i])[2:].zfill(T)
    # print(len(bin(M[i])[2:]))
    for j in range(T):
        matr[j, i] = c[j]
print(matr.shape)
S = np.ndarray((64, T, 32), dtype=int, order='C')
l_dict = list(dict.values())
# print("XXX", l_dict)
for k in range(0, 64 * 32, 32):
    c = l_dict[k:k+32]
    # print(len(c), len(l_dict), c[0])
    for m in range(32):
        # print(c[m], bin(c[m])[2:], len(bin(c[m])[2:]))
        # print(k,m)
        d = bin(c[m])[2:].zfill(T)
        for n in range(32):
            S[k//32, m, n] = d[n]
# print(S.view())
print(S.shape)


def work(s, M_matrix, id, numNodes, SOLS):
    # mostProbableKey = [-1] * 16
    w_size = 256
    for i in range(0, numNodes-w_size+1, w_size//1):
        tmp = np.ascontiguousarray(M_matrix[:, i:i+w_size])
        window = matrix(GF(2), tmp)
        for j in range(0, 32, 1):
            K = vector(GF(2), s[:, j])
            try:
                X = window.solve_right(K)
                print("ID: ", id, i, j)
                SOLS[id] = (i, j)
                return
            except ValueError as e:
                # print(e)
                continue


SOLS = multiprocessing.Manager().dictionary()
procs = []
start = datetime.datetime.now()
for id in range(64):
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
bla = ''
for i in range(64):
    print(i, '\t', bin(SOLS.get(i)[1])[2:].zfill(5), '\t', SOLS.get(i)[0])
    bla += bin(SOLS.get(i)[1])[2:].zfill(5)
print(bla, len(bla))
# REAL
# 01100001011000100110001101100100011001010110011001100111011010000110000101100010011000110110010001100101011001100110011101101000011000010110001001100011011001000110010101100110011001110110100001100001011000100110001101100100011001010110011001100111011010000110000101100010011000110110010001100101011001100110011101101000
# 00010000010011101110010010000100111000000000000100000000001000001000100000000111000010001100000000000000000010010010000100010000100001100100000000010100110000000000000010001100000100010001000001000001000100000000001001100000100010000110010100000000010000100000000010001100001010000001000000000010000000010000110010000000
# my sol

# there are some mistakes left in both myLDA and myLDA_Ascon
