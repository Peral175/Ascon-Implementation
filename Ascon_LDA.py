#!/usr/bin/env sage -python
import argparse
import datetime
import numpy as np
import os.path
import pathlib
from bitarray import frozenbitarray
from sage.all import matrix, vector, GF
import line_profiler

INTERSECTION_MODE = True


@line_profiler.profile
def ascon_lda(traces, traces_dir, window_size, window_step, KEY_BYTES=(0,)):
    num_of_bytes = os.path.getsize(traces_dir / "0000.bin")
    num_of_nodes = num_of_bytes * 8
    NUM_BITS = 5

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

    Solutions = {}
    hits = [[] for _ in range(len(KEY_BYTES))]
    for li in range(len(KEY_BYTES)):
        for _ in range(NUM_BITS):
            hits[li].append(set())
    for w in range(0, num_of_nodes, window_step):
        cols = set(Gates_Matrix[w:w + window_size])
        # print("window:", w, "-", w + window_size, "(", len(cols), ")", "/", num_of_nodes)
        window = matrix(GF(2), cols)
        kernel_matrix = window.right_kernel().matrix()
        kernel_matrix = [frozenbitarray(row) for row in kernel_matrix]
        for curr in range(NUM_BITS):
            for KEY_BYTE in KEY_BYTES:
                assert isinstance(KEY_BYTE, int) and 63 >= KEY_BYTE >= 0
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
                    # _ = window.solve_left(vector(GF(2), target))  # verification takes a long time (around 40%)
                    hits[KEY_BYTE][curr].add(kg)

    if INTERSECTION_MODE:
        for KEY_BYTE in KEY_BYTES:
            inters = [set()]  # 0 empty
            for x in range(5):  # 1 2 3 4 5
                inters.append(set(hits[KEY_BYTE][x]))
            for x in range(1, 6):  # 12 13 14 15 23! 24 25 34 35! 45
                for y in range(x + 1, 6):
                    inters.append((inters[x]).intersection(inters[y]))
            for x in range(1, 6):  # 123 124 125 134 135 145 234 235 245 345
                for y in range(x + 1, 6):
                    for z in range(y + 1, 6):
                        inters.append((inters[x]).intersection(inters[y]).intersection(inters[z]))
            for x in range(1, 6):  # 1234 1235 1245 1345 2345
                for y in range(x + 1, 6):
                    for z in range(y + 1, 6):
                        for v in range(z + 1, 6):
                            inters.append(
                                (inters[x]).intersection(inters[y]).intersection(inters[z]).intersection(
                                    inters[v]))
            for i in range(1):
                inters.append(set(hits[KEY_BYTE][0])
                              .intersection(hits[KEY_BYTE][1])
                              .intersection(hits[KEY_BYTE][2])
                              .intersection(hits[KEY_BYTE][3])
                              .intersection(hits[KEY_BYTE][4]))
            print("inters ", inters, len(inters))
            # print(inters[1], inters[2], inters[3], inters[4], inters[5])
            # print(inters[6], inters[7], inters[8], inters[9], inters[10], inters[11], inters[12], inters[13],
            #       inters[14], inters[15])
            # print(inters[16], inters[17], inters[18], inters[19], inters[20], inters[21], inters[22], inters[23],
            #       inters[24], inters[25])
            # print(inters[26], inters[27], inters[28], inters[29], inters[30])

            # Ranking:
            # if len(inters[-1]) == 1:
            #     Solutions[KEY_BYTE] = inters[-1]
            #     continue
            # elif min(map(len, inters[-6:-1])) == 1:
            #     input((KEY_BYTE, min(map(len, inters[-6:-1])), min(inters[-6:-1], key=len)))
            #     Solutions[KEY_BYTE] = min(inters[-6:-1], key=len)
            #     continue
            # elif min(map(len, inters[-16:-6])) == 1:
            #     input(("A", KEY_BYTE, min(map(len, inters[-16:-6])), min(inters[-16:-6], key=len), inters[-16:-6]))
            #     Solutions[KEY_BYTE] = min(inters[-16:-6], key=len)
            #     continue
            # elif min(map(len, inters[-26:-16])) == 1:
            #     input(("B", KEY_BYTE, min(map(len, inters[-26:-16])), min(inters[-26:-16], key=len), inters[-26:-16]))
            #     Solutions[KEY_BYTE] = min(inters[-26:-16], key=len)
            #     continue
            # elif min(map(len, inters[-31:-26])) == 1:
            #     input(("C", KEY_BYTE, min(map(len, inters[-31:-26])), min(inters[-31:-26], key=len), inters[-31:-26]))
            #     Solutions[KEY_BYTE] = min(inters[-31:-26], key=len)
            #     continue
            # else:
            #     Solutions[KEY_BYTE] = min(inters[-31:-1], key=len)  # fix empty set here

            t1 = sorted(inters, key=len)                    # sort list by set length
            t2 = list(filter(lambda x: x != set(), t1))     # get rid of all empty sets
            try:
                t3 = list(filter(lambda x: len(x) == 1, t2))    # find all sets of length 1
                t4 = [list(_)[0] for _ in t3]                   # transform to list
                t5 = max(set(t4), key=t4.count)                 # retrieve most common element
                # Solutions[KEY_BYTE] = {bla4}
                Solutions[KEY_BYTE] = t5
            except ValueError as e:
                input(("Error", e))
                t3 = list(filter(lambda x: 8 >= len(x) >= 2, t2))    # find all sets of length 1
                # input((t3,len(t3)))
                t4 = [list(_) for _ in t3]                   # transform to list
                # print(KEY_BYTE, t4)
                t5 = max(t4, key=t4.count)                 # retrieve most common element
                # Solutions[KEY_BYTE] = {bla4}
                Solutions[KEY_BYTE] = t5
                # input((t4, t5, len(t4)))
            print(Solutions)
    # for KEY_BYTE in KEY_BYTES:
    #     for j in range(1, NUM_BITS):
    #         hits[KEY_BYTE][0] = hits[KEY_BYTE][0].intersection(hits[KEY_BYTE][j])
    #     Solutions[KEY_BYTE] = hits[KEY_BYTE][0]

    recovered_key_bits = Solutions
    recovered_key = ["_"] * 320
    for i in recovered_key_bits:
        try:
            bits = bin(recovered_key_bits[i])[2:].zfill(5)
            # bits = bin(list(recovered_key_bits[i])[0])[2:].zfill(5)
            recovered_key[i + 0] = bits[0]
            recovered_key[i + 64] = bits[1]
            recovered_key[i + 128] = bits[2]
            recovered_key[i + 192] = bits[3]
            recovered_key[i + 256] = bits[4]
        except IndexError:
            continue
    recovered_key_str = ''.join(recovered_key)
    recovered_key_bytes = ""
    if "_" in recovered_key_str:
        print("Incomplete key recovery: ", recovered_key_str)
        return recovered_key_str
    else:
        for i in range(40):
            byte = recovered_key_str[i * 8:(i + 1) * 8]
            recovered_key_bytes += str(hex(int(byte, 2))[2:].zfill(2))
        print("Key recovery: ", recovered_key_bytes)
        key_plaintext = ""
        for i in range(40):
            key_plaintext += chr(int((recovered_key_bytes[i * 2:i * 2 + 2]), 16))
        print(key_plaintext)
        return recovered_key_bytes


def mini_ascon_lda(traces, traces_dir, window_size, window_step, KEY_BYTES=(0,)):
    num_of_bytes = os.path.getsize(traces_dir / "0000.bin")
    num_of_nodes = num_of_bytes * 8
    NUM_BITS = 2

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
                guessed_vector4 ^= (out >> 3 & 0b1) << t
                guessed_vector5 ^= (out >> 4 & 0b1) << t
            vec_bit4[key_bits * 32 + key_bits_guess] = guessed_vector4
            vec_bit5[key_bits * 32 + key_bits_guess] = guessed_vector5

    v4 = list(vec_bit4.values())
    v5 = list(vec_bit5.values())

    Guess_Matr_4 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    Guess_Matr_5 = np.zeros((64, 32,), dtype=frozenbitarray, order='C')
    for kb in range(0, 64):
        vec4 = v4[kb * 32: (kb + 1) * 32]
        vec5 = v5[kb * 32: (kb + 1) * 32]
        for c in range(32):
            Guess_Matr_4[kb, c] = frozenbitarray(bin(vec4[c])[2:].zfill(traces))
            Guess_Matr_5[kb, c] = frozenbitarray(bin(vec5[c])[2:].zfill(traces))
    Guess_Matrix = [Guess_Matr_4, Guess_Matr_5]

    node_vectors = []
    for i in range(num_of_nodes):
        node_vector = 0
        for t in range(traces):
            node_vector ^= ((binaries[t][i // 8] >> i % 8) & 0b1) << t
        node_vectors.append(node_vector)

    Gates_Matrix = np.zeros((num_of_nodes,), dtype=frozenbitarray, order='C')
    for i in range(num_of_nodes):
        Gates_Matrix[i] = frozenbitarray(bin(node_vectors[i])[2:].zfill(traces))

    Solutions = {}
    hits = [[] for _ in range(len(KEY_BYTES))]
    for li in range(len(KEY_BYTES)):
        for _ in range(NUM_BITS):
            hits[li].append(set())
    for w in range(0, num_of_nodes, window_step):
        cols = set(Gates_Matrix[w:w + window_size])
        # print("window:", w, "-", w + window_size, "(", len(cols), ")", "/", num_of_nodes)
        window = matrix(GF(2), cols)
        kernel_matrix = window.right_kernel().matrix()
        kernel_matrix = [frozenbitarray(row) for row in kernel_matrix]
        for curr in range(NUM_BITS):
            for KEY_BYTE in KEY_BYTES:
                assert isinstance(KEY_BYTE, int) and 63 >= KEY_BYTE >= 0
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
                    # _ = window.solve_left(vector(GF(2), target))  # verification takes a long time (around 40%)
                    hits[KEY_BYTE][curr].add(kg)

    for KEY_BYTE in KEY_BYTES:
        for j in range(1, NUM_BITS):
            hits[KEY_BYTE][0] = hits[KEY_BYTE][0].intersection(hits[KEY_BYTE][j])
        Solutions[KEY_BYTE] = hits[KEY_BYTE][0]

    print(Solutions)

    recovered_key_bits = Solutions
    recovered_key = ["_"] * 320
    for i in recovered_key_bits:
        try:
            bits = bin(list(recovered_key_bits[i])[0])[2:].zfill(5)
            recovered_key[i + 0] = bits[0]
            recovered_key[i + 64] = bits[1]
            recovered_key[i + 128] = bits[2]
            recovered_key[i + 192] = bits[3]
            recovered_key[i + 256] = bits[4]
        except IndexError:
            continue
    recovered_key_str = ''.join(recovered_key)
    recovered_key_bytes = ""
    if "_" in recovered_key_str:
        print("Incomplete key recovery: ", recovered_key_str)
        return recovered_key_str
    else:
        for i in range(40):
            byte = recovered_key_str[i * 8:(i + 1) * 8]
            recovered_key_bytes += str(hex(int(byte, 2))[2:].zfill(2))
        print("Key recovery: ", recovered_key_bytes)
        key_plaintext = ""
        for i in range(40):
            key_plaintext += chr(int((recovered_key_bytes[i * 2:i * 2 + 2]), 16))
        print(key_plaintext)
        return recovered_key_bytes


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
    # mini_ascon_lda(
    ascon_lda(
        args.n_traces,
        args.trace_dir,
        args.window_size,
        args.step,
        KEY_BYTES=full_tuple
        # KEY_BYTES=(0, 1, 2, 3, 4, 5, 6, 7)
        # KEY_BYTES=(0,)
    )
    end = datetime.datetime.now()
    print("Time: ", end - start)

    """
    Results for:    ascon Non Constant Addition clear
    python3 Ascon_LDA.py -T 306 -W 256 -S 128 traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-clear/
    Recovered key:  abcdefghijklmnopqrstuvwxyz1234567890ABCD
    Time:  0:00:05.414043   - 5 bits
    Time:  0:00:04.907609   - 2 bits
    2 bits should be always enough
    
    Results for:    ascon Non Constant Addition isw2
    python3 Ascon_LDA.py -T 306 -W 256 -S 128 traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw2/
    Recovered key:  abcdefghijklmnopqrstuvwxyz1234567890ABCD
    Time:  0:00:13.398230   - 5 bits
    Time:  0:00:12.989944   - 2 bits
    
    Detailed timing analysis:
    kernprof -l Ascon_LDA.py -T 306 -W 256 -S 128 traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-clear/
    python3 -m line_profiler -rmt "Ascon_ExactMatch.py.lprof"
    """
