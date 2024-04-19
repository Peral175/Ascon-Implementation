import argparse
import multiprocessing
import pathlib
import numpy as np
from sage.all import *
import datetime
import os.path

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
parser.add_argument(
    '-W',
    '--window_size',
    type=int,
    default=5,
    help='sliding window size'
)
parser.add_argument(
    '-S',
    '--step',
    type=int,
    default=1,
    help='sliding window size step (2 = half)'
)

args = parser.parse_args()
T = args.n_traces
numOfBytes = os.path.getsize(args.trace_dir / "0000.bin")
numOfNodes = numOfBytes * 8
mode = args.mode
print("numOfBytes = ", numOfBytes)
print("numOfNodes = ", numOfNodes)
print("traces = ", T)
print("window size = ", args.window_size)
print("window step = ", args.step)
if mode == 0:
    ASCONSBOX = [
        0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
        0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17]

    def selection_function(ptb, kbg):
        return ASCONSBOX[ptb ^ kbg] & 1

    PLAINTEXTS = []
    for traceNr in range(T):
        pt = args.trace_dir / ("%04d.pt" % traceNr)
        with open(pt, "rb") as f:
            PLAINTEXTS += [f.read(40)]
    # print("Plaintext length:", len(PLAINTEXTS))
    dictionary = {}
    for plaintextBits in range(64):    # plaintext is 320 bits inputs of 5-bits = 64
        for keyBitsGuess in range(32):   # key is 320 bits - we consider input of size 32-bits
            guessedVector = 0
            for traceNr in range(T):    # 256 traces
                tmp = bin(int.from_bytes(PLAINTEXTS[traceNr], byteorder='big'))[2:].zfill(320)
                x0 = tmp[plaintextBits + 0]
                x1 = tmp[plaintextBits + 64]
                x2 = tmp[plaintextBits + 128]
                x3 = tmp[plaintextBits + 192]
                x4 = tmp[plaintextBits + 256]
                x = x0 + x1 + x2 + x3 + x4
                guessedVector ^= selection_function(int(x, 2), keyBitsGuess) << traceNr
            dictionary[plaintextBits * 32 + keyBitsGuess] = guessedVector   # had to inverse because of duplicates
    print("Dictionary length: ", len(dictionary))   # should be 2048 ? --> see above
TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]
# print("Traces length: ", len(TRACES))
M = []
for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
    M.append(nodeVector)
# print("M length: ", len(M))
matr = np.zeros((T, numOfNodes), dtype=int, order='C')
for i in range(numOfNodes):
    c = bin(M[i])[2:].zfill(T)
    for j in range(T):
        matr[j, i] = c[j]
print("Matrix shape: \t", matr.shape)
# print(matr.view())
S = np.ndarray((64, T, 32), dtype=int, order='C')
l_dict = list(dictionary.values())
# print(l_dict)
for k in range(0, 64 * 32, 32):
    c = l_dict[k:k+32]
    for m in range(32):
        d = bin(c[m])[2:].zfill(T)
        for n in range(T):
            S[k//32, n, m] = d[n]
print("Key Matrix shape: ", S.shape)
# print(S.view())


def work(s, M_matrix, ID, numNodes, Solutions):
    # mostProbableKey = [-1] * 16
    w_size = args.window_size
    step = args.step
    for w in range(0, numNodes-w_size+1, w_size//step):
        tmp = np.ascontiguousarray(M_matrix[:, w:w+w_size])
        window = matrix(GF(2), tmp)
        for kg in range(0, 32, 1):
            K = vector(GF(2), s[:, kg])
            # print(window, K)
            try:
                _ = window.solve_right(K)
                print("ID: ", ID, w, kg)
                Solutions[ID] = (w, kg)
                # return
            except ValueError as e:
                # print(e)
                continue


SOLS = multiprocessing.Manager().dict()
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
recovered_key = ''
for i in range(64):
    # print(i, '\t', bin(SOLS.get(i)[1])[2:].zfill(5), '\t', SOLS.get(i)[0])
    recovered_key += bin(SOLS.get(i)[1])[2:].zfill(5)
print("Recovered key: ", recovered_key, len(recovered_key), int(recovered_key, 2))
#01100 00101 10000 10110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001011000010110000101100001
