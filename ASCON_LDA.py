import argparse
import multiprocessing
import pathlib
import numpy as np
import datetime
import os.path
from sage.all import *


def attack(T, trace_dir, w_size, step):
    numOfBytes = os.path.getsize(trace_dir / "0000.bin")
    numOfNodes = numOfBytes * 8

    # print("numOfBytes = ", numOfBytes)
    # print("numOfNodes = ", numOfNodes)
    # print("traces = ", T)
    # print("window size = ", window_size)
    # print("window step = ", step)

    ASCONSBOX = [0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
                 0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17]

    def selection_function(ptb, kbg):
        return ASCONSBOX[ptb ^ kbg]

    PLAINTEXTS = []
    for traceNr in range(T):
        pt = trace_dir / ("%04d.pt" % traceNr)
        with open(pt, "rb") as f:
            PLAINTEXTS += [f.read(40)]

    dict1, dict2, dict3, dict4, dict5 = {}, {}, {}, {}, {}
    for plaintextBits in range(64):  # plaintext is 320 bits inputs of 5-bits = 64
        for keyBitsGuess in range(32):  # key is 320 bits - we consider input of size 32-bits
            guessedVector1, guessedVector2, guessedVector3, guessedVector4, guessedVector5 = 0, 0, 0, 0, 0
            for traceNr in range(T):  # 256 traces
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
        ftrace = trace_dir / ("%04d.bin" % traceNumber)
        with open(ftrace, "rb") as f:
            TRACES += [f.read(numOfBytes)]

    v1 = list(dict1.values())
    v2 = list(dict2.values())
    v3 = list(dict3.values())
    v4 = list(dict4.values())
    v5 = list(dict5.values())

    M = []
    for node in range(numOfNodes):
        nodeVector = 0
        for traceNumber in range(T):
            nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
        M.append(nodeVector)
    matr = np.zeros((T, numOfNodes), dtype=int, order='C')
    for x in range(numOfNodes):
        c = bin(M[x])[2:].zfill(T)
        for j in range(T):
            matr[j, x] = c[j]
    M = matr

    S1 = np.ndarray((64, T, 32), dtype=int, order='C')
    S2 = np.ndarray((64, T, 32), dtype=int, order='C')
    S3 = np.ndarray((64, T, 32), dtype=int, order='C')
    S4 = np.ndarray((64, T, 32), dtype=int, order='C')
    S5 = np.ndarray((64, T, 32), dtype=int, order='C')
    for k in range(0, 2048, 32):
        c1 = v1[k:k + 32]
        c2 = v2[k:k + 32]
        c3 = v3[k:k + 32]
        c4 = v4[k:k + 32]
        c5 = v5[k:k + 32]
        for m in range(32):
            d1 = bin(c1[m])[2:].zfill(T)
            d2 = bin(c2[m])[2:].zfill(T)
            d3 = bin(c3[m])[2:].zfill(T)
            d4 = bin(c4[m])[2:].zfill(T)
            d5 = bin(c5[m])[2:].zfill(T)
            for t in range(T):
                S1[k // 32, t, m] = d1[t]
                S2[k // 32, t, m] = d2[t]
                S3[k // 32, t, m] = d3[t]
                S4[k // 32, t, m] = d4[t]
                S5[k // 32, t, m] = d5[t]

    S = [S1, S2, S3, S4, S5]

    def doWork(k_matr, M_matrix, ID, numNodes, Solutions):
        s1, s2, s3, s4, s5 = k_matr[0], k_matr[1], k_matr[2], k_matr[3], k_matr[4]
        l1, l2, l3, l4, l5 = [], [], [], [], []
        for w in range(0, numNodes - w_size + 1, step):
            window = matrix(GF(2), np.ascontiguousarray(M_matrix[:, w:w + w_size]))
            # TEST1 = window.right_kernel().matrix()
            # TEST2 = window.left_kernel().matrix()
            # print("Test1: ", TEST1)
            # print("Test2: ", TEST2)
            for kg in range(0, 32, 1):
                K1 = vector(GF(2), s1[ID, :, kg])
                K2 = vector(GF(2), s2[ID, :, kg])
                K3 = vector(GF(2), s3[ID, :, kg])
                K4 = vector(GF(2), s4[ID, :, kg])
                K5 = vector(GF(2), s5[ID, :, kg])
                try:
                    _ = window.solve_right(K1); l1.append(kg)
                except ValueError:
                    pass
                try:
                    _ = window.solve_right(K2); l2.append(kg)
                except ValueError:
                    pass
                try:
                    _ = window.solve_right(K3); l3.append(kg)
                except ValueError:
                    pass
                try:
                    _ = window.solve_right(K4); l4.append(kg)
                except ValueError:
                    pass
                try:
                    _ = window.solve_right(K5); l5.append(kg)
                except ValueError:
                    pass

                pot1 =             set(l1)
                pot2 =             set(l1).intersection(l2)
                pot3 =         set(set(l1).intersection(l2)).intersection(l3)
                pot4 =     set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)
                pot5 = set(set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)).intersection(l5)
                print(pot1, pot2, pot3, pot4, pot5)
            Solutions[ID] = set(set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)).intersection(l5)
            # todo: rank candidates + all combinations of intersections; start with l3 ?
            # 3 mostly good enough
            # 4 almost always good enough
            # intersection impact on performance?
            # if pot3 == pot5 and pot4 == pot5:
            #     input("FOUND!")
            # if len(pot1) > 0:
            #     print(pot1, pot2, pot3, pot4, pot5)
            # Solutions[ID] = pot5
            # print(ID, w, set(set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)).intersection(l5))
            # todo: do not stop with first ?
            # if len(Solutions[ID]) > 0:
            #     break

    SOLS = multiprocessing.Manager().dict()
    procs = []
    start = datetime.datetime.now()
    for id in range(64):
        proc = multiprocessing.Process(target=doWork, args=(S, M, id, numOfNodes, SOLS,))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()
    end = datetime.datetime.now()
    # print(SOLS)
    print("Time: ", end - start)
    bits_matr = [-1] * 320

    if len(SOLS) == 64:
        for x in range(64):
            t = list(SOLS.get(x))
            try:
                bits = bin(t[0])[2:].zfill(5)
                bits_matr[x] = int(bits[0])
                bits_matr[x+64] = int(bits[1])
                bits_matr[x+128] = int(bits[2])
                bits_matr[x+192] = int(bits[3])
                bits_matr[x+256] = int(bits[4])
            except IndexError:
                continue
        mostProbableKey = [-1] * 40
        for j in range(0, 320, 8):
            byte = bits_matr[j:j+8]
            s = ''
            for k in byte:
                s += str(k)
            x = int(s, 2)
            mostProbableKey[j//8] = x
        recovered_key = ''
        for keyByte in mostProbableKey:
            try:
                recovered_key += chr(keyByte)
            except ValueError:
                recovered_key += '_'
        print("Recovered key: ", recovered_key)
        return True, recovered_key
    else:
        print("Key was not fully recovered!", len(SOLS))
        return False, SOLS


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='LDA for ASCON',
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
        help='sliding window size step'
    )
    args = parser.parse_args()
    attack(args.n_traces, args.trace_dir, args.window_size, args.step)
