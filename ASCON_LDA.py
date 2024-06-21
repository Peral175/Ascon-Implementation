#!/usr/bin/env sage -python
import argparse
import datetime
import numpy as np
import os.path
import pathlib
from bitarray import frozenbitarray
from collections import defaultdict
from line_profiler import profile
from multiprocessing import Process, Manager
from sage.all import matrix, vector, GF

STOP_AT_FIRST_CANDIDATE = False


@profile
def ascon_lda(traces, traces_dir, window_size, window_step, MULTI_THREADED=False,
              KEY_BYTES=(0, 1, 2, 3, 4, 5, 6, 7,
                         8, 9, 10, 11, 12, 13, 14, 15,
                         16, 17, 18, 19, 20, 21, 22, 23,
                         24, 25, 26, 27, 28, 29, 30, 31,
                         32, 33, 34, 35, 36, 37, 38, 39,
                         40, 41, 42, 43, 44, 45, 46, 47,
                         48, 49, 50, 51, 52, 53, 54, 55,
                         56, 57, 58, 59, 60, 61, 62, 63)):
    num_of_bytes = os.path.getsize(traces_dir / "0000.bin")
    num_of_nodes = num_of_bytes * 8

    # 2^5 Ascon SBox
    ASCONSBOX = [0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
                 0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17]

    def selection_function(ptb, kbg):
        # xor the plaintext byte and key byte guess
        # input to Ascon SBox
        # we consider all bits of output
        return ASCONSBOX[ptb ^ kbg]

    plaintexts = []
    for t in range(traces):
        pt = traces_dir / ("%04d.pt" % t)
        with open(pt, "rb") as f:
            plaintexts += [f.read(40)]

    binaries = []
    for t in range(traces):
        ftrace = traces_dir / ("%04d.bin" % t)
        with open(ftrace, "rb") as f:
            binaries += [f.read(num_of_bytes)]

    vec_bit1, vec_bit2, vec_bit3, vec_bit4, vec_bit5 = {}, {}, {}, {}, {}
    for key_bits in range(64):  # plaintext is 320 bits inputs of 5-bits = 64
        for key_bits_guess in range(32):  # key is 320 bits - we consider input of size 32-bits
            guessed_vector1, guessed_vector2, guessed_vector3, guessed_vector4, guessed_vector5 = 0, 0, 0, 0, 0
            for t in range(traces):
                tmp = bin(int.from_bytes(plaintexts[t], byteorder='big'))[2:].zfill(320)
                x0 = tmp[key_bits + 0]
                x1 = tmp[key_bits + 64]
                x2 = tmp[key_bits + 128]
                x3 = tmp[key_bits + 192]
                x4 = tmp[key_bits + 256]
                x = int(x0 + x1 + x2 + x3 + x4, 2)
                out = selection_function(x, key_bits_guess)
                guessed_vector1 ^= (out >> 0 & 0b1) << t
                guessed_vector2 ^= (out >> 1 & 0b1) << t
                guessed_vector3 ^= (out >> 2 & 0b1) << t
                guessed_vector4 ^= (out >> 3 & 0b1) << t
                guessed_vector5 ^= (out >> 4 & 0b1) << t
            vec_bit1[key_bits * 32 + key_bits_guess] = guessed_vector1
            vec_bit2[key_bits * 32 + key_bits_guess] = guessed_vector2
            vec_bit3[key_bits * 32 + key_bits_guess] = guessed_vector3
            vec_bit4[key_bits * 32 + key_bits_guess] = guessed_vector4
            vec_bit5[key_bits * 32 + key_bits_guess] = guessed_vector5

    v1 = list(vec_bit1.values())
    v2 = list(vec_bit2.values())
    v3 = list(vec_bit3.values())
    v4 = list(vec_bit4.values())
    v5 = list(vec_bit5.values())

    Guess_Matr_1 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    Guess_Matr_2 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    Guess_Matr_3 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    Guess_Matr_4 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    Guess_Matr_5 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    for kb in range(0, 64):
        vec1 = v1[kb * 32: (kb + 1) * 32]
        vec2 = v2[kb * 32: (kb + 1) * 32]
        vec3 = v3[kb * 32: (kb + 1) * 32]
        vec4 = v4[kb * 32: (kb + 1) * 32]
        vec5 = v5[kb * 32: (kb + 1) * 32]
        for c in range(32):
            Guess_Matr_1[kb, c] = frozenbitarray(bin(vec1[c])[2:].zfill(traces))
            Guess_Matr_2[kb, c] = frozenbitarray(bin(vec2[c])[2:].zfill(traces))
            Guess_Matr_3[kb, c] = frozenbitarray(bin(vec3[c])[2:].zfill(traces))
            Guess_Matr_4[kb, c] = frozenbitarray(bin(vec4[c])[2:].zfill(traces))
            Guess_Matr_5[kb, c] = frozenbitarray(bin(vec5[c])[2:].zfill(traces))
    Guess_Matrix = [Guess_Matr_1, Guess_Matr_2, Guess_Matr_3, Guess_Matr_4, Guess_Matr_5]

    node_vectors = []
    for i in range(num_of_nodes):
        node_vector = 0
        for t in range(traces):
            node_vector ^= ((binaries[t][i // 8] >> i % 8) & 0b1) << t
        node_vectors.append(node_vector)

    Gates_Matrix = np.zeros((num_of_nodes,), dtype=frozenbitarray, order='C')
    for i in range(num_of_nodes):
        Gates_Matrix[i] = frozenbitarray(bin(node_vectors[i])[2:].zfill(traces))

    if not MULTI_THREADED:
        Solutions = {}
        for KEY_BYTE in KEY_BYTES:
            # print("Attack key bits: {} {} {} {} {}".format(KEY_BYTE,
            #                                                KEY_BYTE + 64,
            #                                                KEY_BYTE + 128,
            #                                                KEY_BYTE + 192,
            #                                                KEY_BYTE + 256))
            assert isinstance(KEY_BYTE, int) and 63 >= KEY_BYTE >= 0
            DONE = False    # todo
            hits = [[], [], [], [], []]
            for w in range(0, num_of_nodes, window_step):
                cols = set(Gates_Matrix[w:w + window_size])
                # print("window:", w, "-", w + window_size, "(", len(cols), ")", "/", num_of_nodes)
                window = matrix(GF(2), cols)
                kernel_matrix = window.right_kernel().matrix()
                kernel_matrix = [frozenbitarray(row) for row in kernel_matrix]

                for curr in range(5):
                    # O(n^3 + nk)
                    for kg, target in enumerate(Guess_Matrix[curr][KEY_BYTE]):
                        match = True
                        nm = 0
                        for row in kernel_matrix:
                            if (row & target).count(1) & 1:
                                match = False
                                break
                            nm += 1
                        if not match:
                            continue
                        _ = window.solve_left(vector(GF(2), target))  # verification
                        hits[curr].append(kg)

            for j in range(1, 5):
                hits[0] = set(hits[0]).intersection(set(hits[j]))
            Solutions[KEY_BYTE] = hits[0]
        return Solutions

    elif MULTI_THREADED:
        def concurrent(Guess_matrix, Gates_matrix, ID, sols):
            DONE = False    # todo
            hits = [[], [], [], [], []]
            for w in range(0, num_of_nodes, window_step):
                cols = set(Gates_matrix[w:w + window_size])
                # print("Thread ", ID, " window:", w, "-", w + window_size, "(", len(cols), ")", "/", num_of_nodes)
                window = matrix(GF(2), cols)
                kernel_matrix = window.right_kernel().matrix()
                kernel_matrix = [frozenbitarray(row) for row in kernel_matrix]

                for curr in range(5):
                    # O(n^3 + nk)
                    for kg, target in enumerate(Guess_matrix[curr][ID]):
                        match = True
                        nm = 0
                        for row in kernel_matrix:
                            if (row & target).count(1) & 1:
                                match = False
                                break
                            nm += 1
                        if not match:
                            continue
                        _ = window.solve_left(vector(GF(2), target))  # verification
                        hits[curr].append(kg)

            for j in range(1, 5):
                hits[0] = set(hits[0]).intersection(set(hits[j]))
            sols[KEY_BYTE] = hits[0]

        Solutions = Manager().dict()
        processes = []
        for KEY_BYTE in KEY_BYTES:
            # print("Attack key bits: {} {} {} {} {}".format(KEY_BYTE,
            #                                                KEY_BYTE + 64,
            #                                                KEY_BYTE + 128,
            #                                                KEY_BYTE + 192,
            #                                                KEY_BYTE + 256))
            assert isinstance(KEY_BYTE, int) and 63 >= KEY_BYTE >= 0
            process = Process(target=concurrent,
                              args=(Guess_Matrix, Gates_Matrix, KEY_BYTE, Solutions,))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
        return Solutions
        """# 1,2,3,4,5
        pot1 = set(set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)).intersection(l5)
        # 1,2,3,4
        pot2 = set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l4)
        # 1,2,3,5
        pot3 = set(set(set(l1).intersection(l2)).intersection(l3)).intersection(l5)
        # 1,2,4,5
        pot4 = set(set(set(l1).intersection(l2)).intersection(l4)).intersection(l5)
        # 1,3,4,5
        pot5 = set(set(set(l1).intersection(l3)).intersection(l4)).intersection(l5)
        # 2,3,4,5
        pot6 = set(set(set(l2).intersection(l3)).intersection(l4)).intersection(l5)
        # 1,2,3
        pot7 = set(set(l1).intersection(l2)).intersection(l3)
        # 1,2,4
        pot8 = set(set(l1).intersection(l2)).intersection(l4)
        # 1,2,5
        pot9 = set(set(l1).intersection(l2)).intersection(l5)
        # 1,3,4
        pot10 = set(set(l1).intersection(l3)).intersection(l4)
        # 1,3,5
        pot11 = set(set(l1).intersection(l3)).intersection(l5)
        # 1,4,5
        pot12 = set(set(l1).intersection(l4)).intersection(l5)
        # 2,3,4
        pot13 = set(set(l2).intersection(l3)).intersection(l4)
        # 2,3,5
        pot14 = set(set(l2).intersection(l3)).intersection(l5)
        # 2,4,5
        pot15 = set(set(l2).intersection(l4)).intersection(l5)
        # 3,4,5
        pot16 = set(set(l3).intersection(l4)).intersection(l5)
        # 1,2
        pot17 = set(l1).intersection(l2)
        # 1,3
        pot18 = set(l1).intersection(l3)
        # 1,4
        pot19 = set(l1).intersection(l4)
        # 1,5
        pot20 = set(l1).intersection(l5)
        # 2,3
        pot21 = set(l2).intersection(l3)
        # 2,4
        pot22 = set(l2).intersection(l4)
        # 2,5
        pot23 = set(l2).intersection(l5)
        # 3,4
        pot24 = set(l3).intersection(l4)
        # 3,5
        pot25 = set(l3).intersection(l5)
        # 4,5
        pot26 = set(l4).intersection(l5)
        # 1
        pot27 = set(l1)
        # 2
        pot28 = set(l2)
        # 3
        pot29 = set(l3)
        # 4
        pot30 = set(l4)
        # 5
        pot31 = set(l5)
        # {}
        print(numOfNodes,
              pot1,
              pot2, pot3, pot4, pot5, pot6,
              pot7, pot8, pot9, pot10, pot11, pot12, pot13, pot14, pot15, pot16,
              pot17, pot18, pot19, pot20, pot21, pot22, pot23, pot24, pot25, pot26,
              pot27, pot28, pot29, pot30, pot31,
              "\n"
        )
        # if not stopping when finding first solution --> errors can be introduced later"""
        # todo: rank candidates + all combinations of intersections; start with l3 ?
        # optimze with fewest amount of bits/intersection


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

    start = datetime.datetime.now()
    full_tuple = tuple(i for i in range(64))
    recovered_key_bits = ascon_lda(
        args.n_traces,
        args.trace_dir,
        args.window_size,
        args.step,
        MULTI_THREADED=True,
        KEY_BYTES=full_tuple
        # KEY_BYTES=(0, 1)
    )
    end = datetime.datetime.now()
    print("Time: ", end - start)

    # print("Recovered key bits: ", recovered_key_bits)
    recovered_key = ["_"] * 320
    for i in recovered_key_bits:
        bits = bin(list(recovered_key_bits[i])[0])[2:].zfill(5)
        recovered_key[i + 0] = bits[0]
        recovered_key[i + 64] = bits[1]
        recovered_key[i + 128] = bits[2]
        recovered_key[i + 192] = bits[3]
        recovered_key[i + 256] = bits[4]
    # print(recovered_key)
    recovered_key_str = ''.join(recovered_key)
    # print(recovered_key_str)
    recovered_key_bytes = ""
    if len(recovered_key_bits) == 64:
        for i in range(40):
            byte = recovered_key_str[i * 8:(i + 1) * 8]
            recovered_key_bytes += str(hex(int(byte, 2))[2:].zfill(2))
        print(recovered_key_bytes)
        key_plaintext = ""
        for i in range(40):
            key_plaintext += chr(int((recovered_key_bytes[i*2:i*2+2]), 16))
        print(key_plaintext)
    """
    Results for:    aes with 2 rounds clear
    python3 AES_ExactMatch.py -T 256 traces/abcdefghABCDEFGH/aes2-clear/
    Most probable key (char): abcdefghABCDEFGH
                   (hex): 61626364656667684142434445464748
    Time: 0:00:00.241605


    This attack does not find solutions for masked aes (except higher order exact matching attack ?)

    Detailed timing analysis:
    kernprof -l AES_ExactMatch.py -T 256 traces/abcdefghABCDEFGH/aes2-clear/
    python3 -m line_profiler -rmt "AES_ExactMatch.py.lprof"
    """
