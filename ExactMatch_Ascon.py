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
                x = x0 + x1 + x2 + x3 + x4
                guessedVector ^= selection_function(int(x, 2), keyBitsGuess) << traceNr
            # print(guessedVector)
            if guessedVector in dictionary:
                dictionary[guessedVector] = plaintextBits * 32 + keyBitsGuess
                # continue
            else:
                dictionary[guessedVector] = plaintextBits * 32 + keyBitsGuess
            # dictionary[plaintextBits * 32 + keyBitsGuess] = (plaintextBits * 32 + keyBitsGuess, guessedVector)
    print("Dictionary length: ", len(dictionary))       # todo: why 512 instead 2048 ?
TRACES = []
for traceNumber in range(T):
    ftrace = args.trace_dir / ("%04d.bin" % traceNumber)
    with open(ftrace, "rb") as f:
        TRACES += [f.read(numOfBytes)]

mostProbableKey = [-1] * 64
# rrrr = dictionary.values()
# values = []
# ke = []
# for i,j in rrrr:
#     values.append(j)
#     ke.append(i)
# for i in range(len(rrrr)):
#     print("ZYY" , list(rrrr)[i], values[i], ke[i])
# sol = ''
for node in range(numOfNodes):
    nodeVector = 0
    for traceNumber in range(T):
        # print(TRACES[traceNumber], len(TRACES[traceNumber]), numOfBytes, numOfNodes, traceNumber)
        # print(TRACES[traceNumber][node // 8])
        # print(TRACES[traceNumber][node // 5])
        # print(TRACES[traceNumber][node // 8] >> node % 8, node)
        # print(((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber)
        # input()
        tmp = bin(int.from_bytes(TRACES[traceNumber], byteorder='big'))[2:].zfill(4176)
        # print(tmp, len(tmp))
        t = tmp[(node//5)*5:(node//5)*5+5]
        # print(t, int(t, 2), int(t, 2) >> node % 5)
        # print(node//5)
        # input()
        nodeVector ^= ((int(t, 2) >> node % 5) & 0b1) << traceNumber
        # print(nodeVector, node, traceNumber, len(TRACES[traceNumber]), node // 5, node //8)
    # print(nodeVector, node, node // 5, node //8)
        # input()
        # nodeVector ^= ((TRACES[traceNumber][node // 8] >> node % 8) & 0b1) << traceNumber   # todo: this correct?
    # print(nodeVector, nodeVector.bit_length())
    match = dictionary.get(nodeVector)
    # print(match)
    if match != None:
        # print("XXX")
        print(match, match // 32, match % 32)   # todo: why always same?
        mostProbableKey[match // 32] = match % 32
print(mostProbableKey)
#     if nodeVector in values:
#         bla = values[values.index(nodeVector)]
#         blaa = ke[values.index(nodeVector)]
#         print("ASDF" , bla, blaa, blaa // 32)
#         match = nodeVector
#     else:
#         match = None
#     if match != None:
#         print(match, match % 32, match // 32)
#         mostProbableKey[blaa // 32] = match % 32
#         sol += bin(match % 32)[2:].zfill(5)
# print(sol, len(sol))
# missingBytes = 0
# s = ''
# for i in range(64):
#     print(bin(mostProbableKey[i])[2:].zfill(5))
#     s += bin(mostProbableKey[i])[2:].zfill(5)
# print(s, len(s))
# for i in range(0,320,8):
#     print(i//8, int(s[i:i+8],2))
