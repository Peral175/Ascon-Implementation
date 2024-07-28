"""
This file is redundant; see Ascon_P.py for the boolean circuit."
"""

# import sys
from circkit.bitwise import BitwiseCircuit
# sys.path.append("../../")


def circ_ascon_perm(state, nr_rounds=12):
    crA = [0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    # crB8 = [0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    # crB6 = [0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    C = BitwiseCircuit(word_size=64)    # word_size in bits
    x0 = C.add_input("x0")
    x1 = C.add_input("x1")
    x2 = C.add_input("x2")
    x3 = C.add_input("x3")
    x4 = C.add_input("x4")
    for r in range(nr_rounds):
        # Round Constant Addition
        x2 ^= crA[r+12-nr_rounds]
        # Substitution Layer
        x0 ^= x4;   x4 ^= x3;   x2 ^= x1
        t0 = x0;    t1 = x1;    t2 = x2;    t3 = x3;    t4 = x4
        t0 = ~t0;   t1 = ~t1;   t2 = ~t2;   t3 = ~t3;   t4 = ~t4
        t0 &= x1;   t1 &= x2;   t2 &= x3;   t3 &= x4;   t4 &= x0
        x0 ^= t1;   x1 ^= t2;   x2 ^= t3;   x3 ^= t4;   x4 ^= t0
        x1 ^= x0;   x0 ^= x4;   x3 ^= x2;   x2 = ~x2
        # Linear Diffusion Layer
        x0 = x0 ^ x0.ror(19) ^ x0.ror(28)
        x1 = x1 ^ x1.ror(61) ^ x1.ror(39)
        x2 = x2 ^ x2.ror( 1) ^ x2.ror( 6)
        x3 = x3 ^ x3.ror(10) ^ x3.ror(17)
        x4 = x4 ^ x4.ror( 7) ^ x4.ror(41)

    C.add_output([x0,x1,x2,x3,x4])
    inp = [state[0],
           state[1],
           state[2],
           state[3],
           state[4]]
    out = C.evaluate(inp)
    # print("Circuit output: ")
    # print(out)
    # Masking etc + compare with another python implementation
    return out
