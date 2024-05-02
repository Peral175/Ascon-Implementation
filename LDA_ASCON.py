import argparse
import multiprocessing
import pathlib
import numpy as np
from sage.all import *
import datetime
import os.path

parser = argparse.ArgumentParser(
    description='my implementation of LDA for ASCON',
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


def vectInList(vect, lst, array):  # we are looking for all occurrences!
    while vect in lst:
        index = lst.index(vect)
        array.append(index)
        lst[index] = -1


if mode == 0:
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
    for plaintextBits in range(64):    # plaintext is 320 bits inputs of 5-bits = 64
        for keyBitsGuess in range(32):   # key is 320 bits - we consider input of size 32-bits
            guessedVector1, guessedVector2, guessedVector3, guessedVector4, guessedVector5 = 0, 0, 0, 0, 0
            for traceNr in range(T):    # 256 traces
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

    M = []
    for node in range(numOfNodes):
        nodeVector = 0
        for traceNumber in range(T):
            nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
        M.append(nodeVector)

    def work(M_matrix, ID, numNodes, Solutions):
        w_size = args.window_size
        step = args.step
        for w in range(0, numNodes-w_size+1, w_size//step):
            tmp = M_matrix[w:w+w_size]
            for i in range(0, w_size):
                for j in range(i+1, w_size):
                    # for k in range(j+1, w_size):
                    #     curr_vec = tmp[i] ^ tmp[j] ^ tmp[k]
                    #     vectInList(curr_vec, v1, r1)
                    #     vectInList(curr_vec, v2, r2)
                    #     vectInList(curr_vec, v3, r3)
                    #     vectInList(curr_vec, v4, r4)
                    #     vectInList(curr_vec, v5, r5)
                    curr_vec = tmp[i] ^ tmp[j]
                    vectInList(curr_vec, v1, r1)
                    vectInList(curr_vec, v2, r2)
                    vectInList(curr_vec, v3, r3)
                    vectInList(curr_vec, v4, r4)
                    vectInList(curr_vec, v5, r5)
            print(w, len(r1), len(r2), len(r3), len(r4), len(r5))
        r1.sort()
        r2.sort()
        r3.sort()
        r4.sort()
        r5.sort()
        intersection = set(set(set(set(r1).intersection(r2)).intersection(r2)).intersection(r4)).intersection(
            r5)
        si = sorted(intersection)
        print(r1[:10], r2[:10], r3[:10], r4[:10], r5[:10])
        print(si, len(si))
        return si

    sorted_intersection = work(M, "0", numOfNodes, "sols")
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
                byte = bits_matr[_][j:j + 8]
                s = ''
                for k in byte:
                    s += str(k)
                i = int(s, 2)
                mostProbableKey[_ * 8 + j // 8] = i

        recovered_key = ''
        for keyByte in mostProbableKey:
            recovered_key += chr(keyByte)
        print("Recovered key: ", recovered_key)
    except IndexError:
        print("List is empty!")
    # SOLS = multiprocessing.Manager().dict()
    # procs = []
    # start = datetime.datetime.now()
    # for id in range(64):
    #     proc = multiprocessing.Process(target=work, args=(S[id, :], matr, id, numOfNodes, SOLS,))
    #     procs.append(proc)
    #     proc.start()
    # for proc in procs:
    #     proc.join()
    # end = datetime.datetime.now()
    # print("Time: ", end - start)
    # print(SOLS)
    # # print(SOLS.values())
    # # print(SOLS.keys())
    # recovered_key = ''
    # for i in range(64):
    #     # print(i, '\t', bin(SOLS.get(i)[1])[2:].zfill(5), '\t', SOLS.get(i)[0])
    #     recovered_key += bin(SOLS.get(i)[1])[2:].zfill(5)
    # print("Recovered key: ", recovered_key, len(recovered_key), int(recovered_key, 2))
