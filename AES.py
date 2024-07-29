import argparse
from binteger import Bin
from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from wboxkit.ciphers.aes import BitAES
from wboxkit.masking import ISW, MINQ, QuadLin
from CubeLinMasking import CubeLin
from wboxkit.prng import NFSR, Pool
from wboxkit.serialize import RawSerializer


def circuit(key=b'\x00'*16, nr_rounds=2, SERIALIZE=False, STATS=False):
    nfsr = NFSR(
        taps=[[], [11], [50], [3, 107]],
        clocks_initial=100,
        clocks_per_step=1,
    )
    prng = Pool(prng=nfsr, n=256)

    C = BooleanCircuit(name="AES")
    plaintext = b"0123456789abcdef"
    pt = C.add_inputs(128)
    ct, k2 = BitAES(pt, Bin(key).tuple, rounds=nr_rounds)
    C.add_output(ct)
    C.in_place_remove_unused_nodes()
    if STATS:
        C.print_stats()
    out = C.evaluate(Bin(plaintext).tuple)
    if SERIALIZE:
        RawSerializer().serialize_to_file(C, "bin/aes{}-clear.bin".format(nr_rounds))

    C_ISW_2 = ISW(prng=prng, order=1).transform(C)
    C_ISW_2.in_place_remove_unused_nodes()
    if STATS:
        C_ISW_2.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_ISW_2, "bin/aes{}-isw2.bin".format(nr_rounds))
    res = C_ISW_2.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_ISW_3 = ISW(prng=prng, order=2).transform(C)
    C_ISW_3.in_place_remove_unused_nodes()
    if STATS:
        C_ISW_3.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_ISW_3, "bin/aes{}-isw3.bin".format(nr_rounds))
    res = C_ISW_3.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_ISW_4 = ISW(prng=prng, order=3).transform(C)
    C_ISW_4.in_place_remove_unused_nodes()
    if STATS:
        C_ISW_4.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_ISW_4, "bin/aes{}-isw4.bin".format(nr_rounds))
    res = C_ISW_4.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_MINQ = MINQ(prng=prng).transform(C)
    C_MINQ.in_place_remove_unused_nodes()
    if STATS:
        C_MINQ.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_MINQ, "bin/aes{}-minq.bin".format(nr_rounds))
    res = C_MINQ.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_QL2 = QuadLin(prng=prng, n_linear=2).transform(C)
    C_QL2.in_place_remove_unused_nodes()
    if STATS:
        C_QL2.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_QL2, "bin/aes{}-ql2.bin".format(nr_rounds))
    res = C_QL2.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_QL3 = QuadLin(prng=prng, n_linear=3).transform(C)
    C_QL3.in_place_remove_unused_nodes()
    if STATS:
        C_QL3.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_QL3, "bin/aes{}-ql3.bin".format(nr_rounds))
    res = C_QL3.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_QL4 = QuadLin(prng=prng, n_linear=4).transform(C)
    C_QL4.in_place_remove_unused_nodes()
    if STATS:
        C_QL4.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_QL4, "bin/aes{}-ql4.bin".format(nr_rounds))
    res = C_QL4.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_CL2 = CubeLin(prng=prng, n_linear=2).transform(C)
    C_CL2.in_place_remove_unused_nodes()
    if STATS:
        C_CL2.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_CL2, "bin/aes{}-cl2.bin".format(nr_rounds))
    res = C_CL2.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_CL3 = CubeLin(prng=prng, n_linear=3).transform(C)
    C_CL3.in_place_remove_unused_nodes()
    if STATS:
        C_CL3.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_CL3, "bin/aes{}-cl3.bin".format(nr_rounds))
    res = C_CL3.evaluate(Bin(plaintext).tuple)
    assert out == res

    C_CL4 = CubeLin(prng=prng, n_linear=4).transform(C)
    C_CL4.in_place_remove_unused_nodes()
    if STATS:
        C_CL4.print_stats()
    if SERIALIZE:
        RawSerializer().serialize_to_file(C_CL4, "bin/aes{}-cl4.bin".format(nr_rounds))
    res = C_CL4.evaluate(Bin(plaintext).tuple)
    assert out == res


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='aes implementation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-K',
        '--key',
        type=str,
        help='key to use in encryption'
    )
    args = parser.parse_args()
    print(args.key, bytes(args.key, encoding="utf-8"))
    circuit(bytes(args.key, encoding="utf-8"), nr_rounds=2, SERIALIZE=True, STATS=True)
