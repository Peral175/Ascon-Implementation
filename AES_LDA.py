#!/usr/bin/env sage -python
import argparse
import datetime
import numpy as np
import os.path
import pathlib
from bitarray import frozenbitarray
from collections import defaultdict
from sage.all import matrix, vector, GF

from line_profiler import profile


@profile
def aes_lda(traces, traces_dir, window_size, window_step, KEY_BYTES=(0, 1, 2, 3, 4, 5, 6, 7, 8,
                                                                     9, 10, 11, 12, 13, 14, 15)):
    num_of_bytes = os.path.getsize(traces_dir / "0000.bin")
    num_of_nodes = num_of_bytes * 8

    # 2^8 AES SBox
    aes_sbox = [
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
        # xor the plaintext byte and key byte guess
        # input to AES SBox
        # we consider only the last bit of output
        return aes_sbox[ptb ^ kbg] & 1

    plaintexts = []
    for t in range(traces):
        pt = traces_dir / ("%04d.pt" % t)
        with open(pt, "rb") as f:
            plaintexts += [f.read(16)]  # for each plaintext trace, read the first 16 bytes and append to list

    binaries = []
    for t in range(traces):
        ftrace = traces_dir / ("%04d.bin" % t)
        with open(ftrace, "rb") as f:
            binaries += [f.read(num_of_bytes)]  # for each binary trace, read full

    Vectors_dict = {}
    for key_byte in range(16):  # 16 bytes of secret key are attacked individually
        for key_byte_guess in range(256):  # 2^8 possibilities for each key byte
            guessed_vector = 0
            for t in range(traces):
                guessed_vector ^= selection_function(plaintexts[t][key_byte], key_byte_guess) << t
            Vectors_dict[guessed_vector] = key_byte * 256 + key_byte_guess

    Vectors = list(Vectors_dict)

    Guess_Matrix = np.zeros((16, 256,), dtype=frozenbitarray, order='C')
    for kB in range(0, 16):
        vecs = Vectors[kB * 256: (kB + 1) * 256]
        for c in range(256):
            Guess_Matrix[kB, c] = frozenbitarray(bin(vecs[c])[2:].zfill(traces))

    node_vectors = []
    for i in range(num_of_nodes):
        node_vector = 0
        for t in range(traces):
            node_vector ^= ((binaries[t][i // 8] >> i % 8) & 0b1) << t
        node_vectors.append(node_vector)

    Gates_Matrix = np.zeros((num_of_nodes,), dtype=frozenbitarray, order='C')
    for i in range(num_of_nodes):
        Gates_Matrix[i] = frozenbitarray(bin(node_vectors[i])[2:].zfill(traces))

    Solutions = defaultdict(list)
    # ctr = 0
    for w in range(0, num_of_nodes, window_step):
        cols = set(Gates_Matrix[w:w + window_size])
        # nr_of_windows = num_of_nodes // window_step
        # if ctr % (nr_of_windows // 3) == 0:
        #     print("Current window: [{:4} / {:4}] Columns: {:4} - {:4} out of {} (unique columns: {:4})"
        #           .format(ctr, nr_of_windows, w, w+window_size, num_of_nodes, len(cols)))
        # ctr += 1
        window = matrix(GF(2), cols)
        kernel_matrix = window.right_kernel().matrix()
        kernel_matrix = [frozenbitarray(row) for row in kernel_matrix]

        for KEY_BYTE in KEY_BYTES:
            assert isinstance(KEY_BYTE, int) and 15 >= KEY_BYTE >= 0
            # O(n^3 + nk)
            for kg, target in enumerate(Guess_Matrix[KEY_BYTE]):
                match = True
                nm = 0
                for row in kernel_matrix:
                    if (row & target).count(1) & 1:
                        match = False
                        break
                    nm += 1
                if not match:
                    continue
                # _ = window.solve_left(vector(GF(2), target))  # verification
                Solutions[(KEY_BYTE, kg)] += [w]

    # Print Key
    key_bytes_string = "__" * 16
    for i in Solutions.keys():
        key_bytes_string = key_bytes_string[:i[0] * 2] + hex(i[1])[2:] + key_bytes_string[i[0] * 2 + 2:]
    print("Recovered key bytes as hex chars: ", key_bytes_string)
    return key_bytes_string


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
        default=178,
        help='nr. traces'
    )
    parser.add_argument(
        '-W',
        '--window_size',
        type=int,
        default=128,
        help='sliding window size'
    )
    parser.add_argument(
        '-S',
        '--step',
        type=int,
        default=64,
        help='sliding window size step'
    )
    args = parser.parse_args()

    start = datetime.datetime.now()
    aes_lda(
        args.n_traces,
        args.trace_dir,
        args.window_size,
        args.step,
        KEY_BYTES=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
        # KEY_BYTES=(0, 1, 2)
        # KEY_BYTES=(0,)
    )
    end = datetime.datetime.now()
    print("Time: ", end - start)
"""
    Run in Command Line:
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
    
    """
