#!/usr/bin/env sage -python
import argparse
import pathlib
import numpy as np
import multiprocessing
import datetime
import os.path

from bitarray import frozenbitarray
from sage.all import matrix, vector, GF
from line_profiler import profile


@profile
def attack(T, trace_dir, w_size, step):
    numOfBytes = os.path.getsize(trace_dir / "0000.bin")
    numOfNodes = numOfBytes * 8

    # print("numOfBytes = ", numOfBytes)
    # print("numOfNodes = ", numOfNodes)
    # print("traces = ", T)
    # print("window size = ", window_size)
    # print("window step = ", step)

    AES_SBox = [
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

    def selection_function(ptb, kbg):
        return AES_SBox[ptb ^ kbg] & 1

    PLAINTEXTS = []
    for traceNr in range(T):
        pt = trace_dir / ("%04d.pt" % traceNr)
        with open(pt, "rb") as f:
            PLAINTEXTS += [f.read(16)]

    TRACES = []
    for traceNumber in range(T):
        ftrace = trace_dir / ("%04d.bin" % traceNumber)
        with open(ftrace, "rb") as f:
            TRACES += [f.read(numOfBytes)]

    dictionary = {}     # cannot be set (?)
    for plaintextByte in range(16):         # 16 bytes of key are attacked individually
        for keyByteGuess in range(256):     # 2^8 possibilities for key byte
            guessedVector = 0
            for traceNr in range(T):
                guessedVector ^= selection_function(PLAINTEXTS[traceNr][plaintextByte], keyByteGuess) << traceNr
            dictionary[guessedVector] = plaintextByte * 256 + keyByteGuess

    l_dict = list(dictionary)
    # Guess_Matrix = np.zeros((16, 256, T), dtype=str, order='C')
    Guess_Matrix = np.zeros((16, 256,), dtype=frozenbitarray, order='C')
    for k in range(0, 4096, 256):
        c = l_dict[k:k+256]
        for m in range(256):
            d = bin(c[m])[2:].zfill(T)
            # Guess_Matrix[k // 256, m] = [*d]
            # Guess_Matrix[k // 256, m] = [*frozenbitarray(d)]
            # input((frozenbitarray(d),d))
            Guess_Matrix[k // 256, m] = frozenbitarray(d)
    # input(Guess_Matrix)

    Nodes_Matrix = []
    for node in range(numOfNodes):
        nodeVector = 0
        for traceNumber in range(T):
            nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber
        Nodes_Matrix.append(nodeVector)

    # Gates_Matrix = np.zeros((numOfNodes, T), dtype=str, order='C')
    # for i in range(numOfNodes):
    #     c = bin(Nodes_Matrix[i])[2:].zfill(T)
    #     Gates_Matrix[i] = [*c]
    #
    # Gates_Matrix = [] * numOfNodes
    Gates_Matrix = np.zeros((numOfNodes,), dtype=frozenbitarray, order='C')
    for i in range(numOfNodes):
        c = bin(Nodes_Matrix[i])[2:].zfill(T)
        # Gates_Matrix[i] = [*c]
        # print(frozenbitarray(c), len(Gates_Matrix))
        Gates_Matrix[i] = frozenbitarray(c)
    # print(Gates_Matrix)
    # input()
    # @profile
    # def work(s, M_matrix, ID, numNodes, Solutions):
    if True:
        M_matrix = Gates_Matrix
        ID = 0
        s = Guess_Matrix[ID]
        numNodes = numOfNodes
        from collections import defaultdict
        Solutions = defaultdict(list)

        for w in range(0, numNodes-w_size+1, step):
            print("window:", w, "/", numNodes)
            tmp = M_matrix[w:w+w_size]
            t = set(tmp)
            # print(type(t), type(tmp), len(t), len(tmp))
            # print(tmp, t)
            # input()
            window = matrix(GF(2), t)  # this is way slower

            TEST2 = window.right_kernel().matrix()
            # TEST2 = window.left_kernel().matrix()
            TEST2 = [frozenbitarray(row) for row in TEST2]

            # todo important
            # visualize on white board
            # precompute target + understand their code + measure performance with theirs + plot

            # optimized implementation : check bit-by-bit, O(n^3 + nk)
            for kg, target in enumerate(s):
                # print(kg, len(target),target)
                original = target
                # tmp = ''
                # for e in target:
                #     tmp += str(e)
                # target = frozenbitarray(tmp)
                match = True
                nm = 0
                for row in TEST2:
                    # if row * target:
                    # print("Row: ", row, target, len(row), len(target), s.shape)
                    if (row & target).count(1) & 1:
                        match = False
                        break
                    nm += 1
                if not match:
                    continue
                # sol = window.solve_right(vector(GF(2), original))
                sol = window.solve_left(vector(GF(2), original))
                # assert sol * mat == target
                # print("Solution found:", sol)
                # Solutions[ID] = (w, kg)  # fastest way?
                Solutions[ID].append((w, [kg]))  # fastest way?
                # input(kg)
            # for kg in range(0, 256, 1):     # 2^8
            #     # K = vector(GF(2), s[:, kg])
            #     K = vector(GF(2), s[kg])
            #     vec = TEST2 * K
            #     # # print("2!", vec, w, kg, type(vec[0]))
            #     vec = set(vec)
            #     if 1 not in vec:
            #         Solutions[ID] = (w, kg)  # fastest way?
            #         # return

            # try:
            #     _ = window.solve_right(K)
            #     Solutions[ID] = (w, kg)
            #     # print("1!", _, w, kg)
            #     # return
            # except ValueError:
            #     continue
    print(Solutions)
    # SOLS = multiprocessing.Manager().dict()
    # print(Guess_Matrix[0,:].shape)
    # print(Gates_Matrix.shape)
    # work(Guess_Matrix[0, :], Gates_Matrix, 0, numOfNodes, SOLS)

    # procs = []
    # for id in range(16):
    #     proc = multiprocessing.Process(target=work, args=(S[id, :], matr, id, numOfNodes, SOLS,))
    #     procs.append(proc)
    #     proc.start()
    # for proc in procs:
    #     proc.join()

    # if len(SOLS) == 16:
    #     recovered_key = ''
    #     for i in range(16):
    #         recovered_key += chr(SOLS.get(i)[1])
    #     print("Recovered key: ", recovered_key)
    #     return True, recovered_key
    # else:
    #     print(SOLS)
    #     print(chr(SOLS.get(0)[1]))
    #     return False, len(SOLS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='LDA for AES',
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

    start = datetime.datetime.now()
    attack(args.n_traces, args.trace_dir, args.window_size, args.step)
    end = datetime.datetime.now()
    print("Time: ", end - start)

    """
    Results for:    aes lda with 2 rounds clear
    python3 AES_LDA.py traces/abcdefghABCDEFGH/aes2-clear/ -T 512 -W 500 -S 500
    Time: 0:00:04.319435        VS      Time:  0:00:06.950022   [Better: Time:  0:00:05.640891]
    We have around 20 % slower performance for clear
    python3 AES_LDA.py traces/abcdefghABCDEFGH/aes2-isw2/ -T 512 -W 500 -S 250
    Time: 0:00:22.076182        VS      Time:  0:00:35.938154
    We have around 40 % slower performance for isw2
    python3 AES_LDA.py traces/abcdefghABCDEFGH/aes2-isw2/ -T 300 -W 256 -S 128
    Time: 0:00:16.654401        VS      Time:  0:00:22.093473   [Better: Time:  0:00:22.872240]
    We have around 27% % slower performance for isw2

    Detailed timing analysis:
    kernprof -l AES_LDA.py traces/abcdefghABCDEFGH/aes2-clear/ -T 512 -W 500 -S 500
    python3 -m line_profiler -rmt "AES_LDA.py.lprof"
    
    
    LDA on clear: 
    Theirs: 5.6 6.7 6.5 5.5 6.5
    Mine:   5.4 5.3 5.4 5.4 6.2
    LDA on isw2: 
    Theirs: 16.1 15.7
    Mine:   17.0 15.8
    
    implement stop at first candidate
    implement keep multiple candidates
    """
