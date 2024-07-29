from binteger import Bin
from circkit.array import Array
from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from CubeLinMasking import CubeLin
from wboxkit.masking import ISW, MINQ, QuadLin
from wboxkit.prng import NFSR, Pool
from wboxkit.serialize import RawSerializer

nfsr = NFSR(
    taps=[[], [11], [50], [3, 107]],
    clocks_initial=100,
    clocks_per_step=1,
)
prng = Pool(prng=nfsr, n=256)


def ISW_transform(C, order, STATS):
    ASCON_ISW = ISW(prng=prng, order=order).transform(C)
    ASCON_ISW.in_place_remove_unused_nodes()
    if STATS:
        ASCON_ISW.print_stats()
    return ASCON_ISW


def MINQ_transform(C, STATS):
    ASCON_MINQ = MINQ(prng=prng).transform(C)
    ASCON_MINQ.in_place_remove_unused_nodes()
    if STATS:
        ASCON_MINQ.print_stats()
    return ASCON_MINQ


def QuadLin_transform(C, n_linear, STATS):
    ASCON_QL = QuadLin(prng=prng, n_linear=n_linear).transform(C)
    ASCON_QL.in_place_remove_unused_nodes()
    if STATS:
        ASCON_QL.print_stats()
    return ASCON_QL


def CubeLin_transform(C, n_linear, STATS):
    ASCON_CL = CubeLin(prng=prng, n_linear=n_linear).transform(C)
    ASCON_CL.in_place_remove_unused_nodes()
    if STATS:
        ASCON_CL.print_stats()
    return ASCON_CL


def perm(state, key=b'\x00'*40, nr_rounds=1, naming="", SERIALIZE=False, STATS=False, NCA=False):
    k0 = Array(Bin(key[0:8]))
    k1 = Array(Bin(key[8:16]))
    k2 = Array(Bin(key[16:24]))
    k3 = Array(Bin(key[24:32]))
    k4 = Array(Bin(key[32:40]))
    cr = [0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    C = BooleanCircuit(name="Ascon-P")

    pt = Array(C.add_inputs(320, "x%d"))
    # below i xor the key to plaintext
    x0 = k0 ^ pt[0:64]
    x1 = k1 ^ pt[64:128]
    x2 = k2 ^ pt[128:192]
    x3 = k3 ^ pt[192:256]
    x4 = k4 ^ pt[256:320]

    for r in range(nr_rounds):
        # Round Constant Addition
        # !!! we omit this since the adversary can circumvent it !!!
        if not NCA:
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
    # C.print_stats()

    inp = Array(Bin(state))
    out = C.evaluate(inp)           # result of regular circuit

    def serialize_circuit(C, string):
        if NCA:
            s = "bin/asconP_{}R_NCA{}{}.bin".format(nr_rounds, naming, string)
        else:
            s = "bin/asconP_{}R_FULL{}{}.bin".format(nr_rounds, naming, string)
        RawSerializer().serialize_to_file(C, s)

    if SERIALIZE:
        serialize_circuit(C, "-clear")

    ASCON_ISW = ISW_transform(C, 1, STATS)
    out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    assert out == out_isw
    if SERIALIZE:
        serialize_circuit(ASCON_ISW, "-isw2")

    ASCON_ISW = ISW_transform(C, 2, STATS)
    out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    assert out == out_isw
    if SERIALIZE:
        serialize_circuit(ASCON_ISW, "-isw3")

    ASCON_ISW = ISW_transform(C, 3, STATS)
    out_isw = ASCON_ISW.evaluate(inp)  # linear masking
    assert out == out_isw
    if SERIALIZE:
        serialize_circuit(ASCON_ISW, "-isw4")

    ASCON_MINQ = MINQ_transform(C, STATS)
    out_minq = ASCON_MINQ.evaluate(inp)  # minimalistic non-linear masking
    assert out == out_minq
    if SERIALIZE:
        serialize_circuit(ASCON_MINQ, "-minq")

    ASCON_QL = QuadLin_transform(C, n_linear=2, STATS=STATS)
    out_ql = ASCON_QL.evaluate(inp)  # combined masking - 2 linear shares 2 non-linear shares
    assert out == out_ql
    if SERIALIZE:
        serialize_circuit(ASCON_QL, "-ql2")

    ASCON_QL = QuadLin_transform(C, n_linear=3, STATS=STATS)
    out_ql = ASCON_QL.evaluate(inp)  # combined masking - 3 linear shares 2 non-linear shares
    assert out == out_ql
    if SERIALIZE:
        serialize_circuit(ASCON_QL, "-ql3")

    ASCON_QL = QuadLin_transform(C, n_linear=4, STATS=STATS)
    out_ql = ASCON_QL.evaluate(inp)  # combined masking - 4 linear shares 2 non-linear shares
    assert out == out_ql
    if SERIALIZE:
        serialize_circuit(ASCON_QL, "-ql4")

    ASCON_CL = CubeLin_transform(C, n_linear=2, STATS=STATS)
    out_cl = ASCON_CL.evaluate(inp)  # combined masking - 2 linear shares 3 non-linear shares
    assert out == out_cl
    if SERIALIZE:
        serialize_circuit(ASCON_CL, "-cl2")

    ASCON_CL = CubeLin_transform(C, n_linear=3, STATS=STATS)
    out_cl = ASCON_CL.evaluate(inp)  # combined masking - 3 linear shares 3 non-linear shares
    assert out == out_cl
    if SERIALIZE:
        serialize_circuit(ASCON_CL, "-cl3")

    ASCON_CL = CubeLin_transform(C, n_linear=4, STATS=STATS)
    out_cl = ASCON_CL.evaluate(inp)  # combined masking - 4 linear shares 3 non-linear shares
    assert out == out_cl
    if SERIALIZE:
        serialize_circuit(ASCON_CL, "-cl4")

    return out


def main():
    print("'ascon_perm()' should be called from 'Ascon128.py' or 'Even_Mansour.py'")


if __name__ == "__main__":
    main()
