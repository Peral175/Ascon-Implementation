import argparse
import os.path
import pathlib

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

ASCONSBOX = [
    0x04, 0x0b, 0x1f, 0x14, 0x1a, 0x15, 0x09, 0x02, 0x1b, 0x05, 0x08, 0x12, 0x1d, 0x03, 0x06, 0x1c,
    0x1e, 0x13, 0x07, 0x0e, 0x00, 0x0d, 0x11, 0x18, 0x10, 0x0c, 0x01, 0x19, 0x16, 0x0a, 0x0f, 0x17
]


def selection_function(ptb, kbg):       # this should be correct
    return ASCONSBOX[ptb ^ kbg] & 1


PLAINTEXTS = []
for traceNr in range(T):
    pt = args.trace_dir / ("%04d.pt" % traceNr)
    with open(pt, "rb") as f:
        PLAINTEXTS += [f.read(40)]  # 40 bytes = 320 bits

dictionary = {}
for plaintextBits in range(64):
    for keyBitsGuess in range(32):
        guessedVector = 0
        for traceNr in range(T):
            tmp = bin(int.from_bytes(PLAINTEXTS[traceNr], byteorder='big'))[2:].zfill(320)
            x0 = tmp[plaintextBits + 0]
            x1 = tmp[plaintextBits + 64]
            x2 = tmp[plaintextBits + 128]
            x3 = tmp[plaintextBits + 192]
            x4 = tmp[plaintextBits + 256]
            x = int(x0 + x1 + x2 + x3 + x4, 2)
            guessedVector ^= selection_function(x, keyBitsGuess) << traceNr
        # dictionary[plaintextBits * 32 + keyBitsGuess] = guessedVector
        dictionary[guessedVector] = plaintextBits * 32 + keyBitsGuess
print("Dictionary length: ", len(dictionary))  # todo question: duplicates okay or indication of mistake?

TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]
mostProbableKey = [-1] * 64

# original: for each trace take one whole byte
for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber

# for node in range(numOfNodes):
#     nodeVector = 0
#     for traceNumber in range(T):
#         tmp = bin(int.from_bytes(TRACES[traceNumber], byteorder='big'))[2:].zfill(numOfNodes)
#         t = tmp[(node // 5) * 5: (node // 5) * 5 + 5]        # todo question: 5-bit here instead of 8?
#         nodeVector ^= (((int(t, 2) >> node % 5) & 0b1) << traceNumber)

    match = dictionary.get(nodeVector)
    if match != None:
        print(match, match // 32, match % 32, nodeVector)
        mostProbableKey[match // 32] = match % 32
print(mostProbableKey)
st = ''
for i in mostProbableKey:
    st += bin(i)[2:].zfill(5)
print(st, len(st))

# Key is b'aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa aaaaaaaa'
# 01100 00101 10000 10110 00010 11000 01011 00001       # first 5 bytes = 40 bits
#    12,    5,   16,   22,    2,   24,   11,    1
