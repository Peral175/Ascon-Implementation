from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from circkit.array import Array
from binteger import Bin

from wboxkit.masking import ISW
from wboxkit.prng import NFSR, Pool
from wboxkit.masking import MINQ
from wboxkit.masking import QuadLin
from CubeLinMasking import CubeLin
from wboxkit.masking import DumShuf
from wboxkit.serialize import RawSerializer

nfsr = NFSR(
    taps=[[], [11], [50], [3, 107]],
    clocks_initial=100,
    clocks_per_step=1,
)
prng = Pool(prng=nfsr, n=256)


# def input_state(state):
#     inp = []
#     for i in state:
#         for j in format(i, '#066b')[2:]:
#             inp.append(j)
#     return inp


# def output_state(out):
#     bin_str = ''
#     for j in range(320):
#         bin_str += str(out[j])
#     out = []
#     for i in range(0, 320, 64):
#         out.append(int(bin_str[i:i + 64], 2))
#     return out


def ISW_transform(C, order):
    ASCON_ISW = ISW(prng=prng, order=order).transform(C)
    ASCON_ISW.in_place_remove_unused_nodes()
    ASCON_ISW.print_stats()
    return ASCON_ISW


def MINQ_transform(C):
    ASCON_MINQ = MINQ(prng=prng).transform(C)
    ASCON_MINQ.in_place_remove_unused_nodes()
    ASCON_MINQ.print_stats()
    return ASCON_MINQ


def QuadLin_transform(C, n_linear):
    ASCON_QL = QuadLin(prng=prng, n_linear=n_linear).transform(C)
    ASCON_QL.in_place_remove_unused_nodes()
    ASCON_QL.print_stats()
    return ASCON_QL


def CubeLin_transform(C, n_linear):
    ASCON_CL = CubeLin(prng=prng, n_linear=n_linear).transform(C)
    ASCON_CL.in_place_remove_unused_nodes()
    ASCON_CL.print_stats()
    return ASCON_CL


def DumShuf_transform(C, n_shares):
    ASCON_DS = DumShuf(prng=prng, n_shares=n_shares).transform(C)
    ASCON_DS.in_place_remove_unused_nodes()
    ASCON_DS.print_stats()
    return ASCON_DS


def ascon_perm(state, key=b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", nr_rounds=1):
    # print(state)
    # print(key)
    k0 = Array(Bin(key[0:8]))
    k1 = Array(Bin(key[8:16]))
    k2 = Array(Bin(key[16:24]))
    k3 = Array(Bin(key[24:32]))
    k4 = Array(Bin(key[32:40]))
    cr = [0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    C = BooleanCircuit(name="ascon_128_perm_boolean")

    pt = Array(C.add_inputs(320, "x%d"))
    # below i xor the key to plaintext
    # todo question: should this be done once or for every round?
    x0 = k0 ^ pt[0:64]
    x1 = k1 ^ pt[64:128]
    x2 = k2 ^ pt[128:192]
    x3 = k3 ^ pt[192:256]
    x4 = k4 ^ pt[256:320]

    for r in range(nr_rounds):
        # Round Constant Addition
        x2 ^= Array(Bin(cr[r + 12 - nr_rounds], 64))

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

    C.add_output([x0, x1, x2, x3, x4])
    C.in_place_remove_unused_nodes()
    C.print_stats()

    # print("state: ", state, len(state))
    inp = state     # input_state(state)  # input helper function

    out = C.evaluate(inp)           # regular circuit

    def serialize_circuit(C, string):
        RawSerializer().serialize_to_file(C, "bin/ascon128_r1{}.bin".format(string))

    """
    Uncomment below to transform and serialize the various circuits.
    Traces can then be generated for the circuits with shell scripts.
    """
    # serialize_circuit(C, "-clear")
    #
    # ASCON_ISW = ISW_transform(C, 1)
    # out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    # assert out == out_isw
    # serialize_circuit(ASCON_ISW, "-isw_2")
    #
    # ASCON_ISW = ISW_transform(C, 2)
    # out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    # assert out == out_isw
    # serialize_circuit(ASCON_ISW, "-isw_3")
    #
    # ASCON_ISW = ISW_transform(C, 3)
    # out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    # assert out == out_isw
    # serialize_circuit(ASCON_ISW, "-isw_4")
    #
    # ASCON_MINQ = MINQ_transform(C)
    # out_minq = ASCON_MINQ.evaluate(inp)  # non-linear masking
    # assert out == out_minq
    # serialize_circuit(ASCON_MINQ, "-minq")
    #
    # ASCON_QL = QuadLin_transform(C, n_linear=2)
    # out_ql = ASCON_QL.evaluate(inp)  # combined masking - 2 non-linear shares
    # assert out == out_ql
    # serialize_circuit(ASCON_QL, "-ql2")
    #
    # ASCON_QL = QuadLin_transform(C, n_linear=3)
    # out_ql = ASCON_QL.evaluate(inp)  # combined masking - 2 non-linear shares
    # assert out == out_ql
    # serialize_circuit(ASCON_QL, "-ql3")
    #
    # ASCON_QL = QuadLin_transform(C, n_linear=4)
    # out_ql = ASCON_QL.evaluate(inp)  # combined masking - 2 non-linear shares
    # assert out == out_ql
    # serialize_circuit(ASCON_QL, "-ql4")

    # ASCON_CL = CubeLin_transform(C, n_linear=3)
    # out_cl = ASCON_CL.evaluate(inp)  # combined masking - 3 non-linear shares
    # assert out == out_cl
    # serialize_circuit(ASCON_CL, "-cl")

    # ASCON_DS = DumShuf_transform(C, n_shares=3)
    # out_ds = ASCON_DS.evaluate(inp)  # dummy shuffling
    # assert out == out_ds
    # serialize_circuit(ASCON_DS, "-ds")

    # print(out)
    # return output_state(out)
    return out
