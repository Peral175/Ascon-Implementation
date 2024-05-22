from wboxkit.masking import ISW, MINQ, QuadLin
from wboxkit.prng import NFSR, Pool
from wboxkit.serialize import RawSerializer
from wboxkit.ciphers.aes import BitAES
from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from binteger import Bin
import argparse


def circuit(key):
    nfsr = NFSR(
        taps=[[], [11], [50], [3, 107]],
        clocks_initial=100,
        clocks_per_step=1,
    )
    prng = Pool(prng=nfsr, n=256)

    C = BooleanCircuit(name="AES_2")
    # key = b"abcdefghABCDEFGH"
    plaintext = b"0123456789abcdef"
    pt = C.add_inputs(128)
    ct, k2 = BitAES(pt, Bin(key).tuple, rounds=2)
    C.add_output(ct)
    C.in_place_remove_unused_nodes()
    C.print_stats()
    ct = C.evaluate(Bin(plaintext).tuple)
    RawSerializer().serialize_to_file(C, "bin/aes2-clear.bin")

    C_ISW_2 = ISW(prng=prng, order=1).transform(C)
    C_ISW_2.in_place_remove_unused_nodes()
    C_ISW_2.print_stats()
    RawSerializer().serialize_to_file(C_ISW_2, "bin/aes2-isw2.bin")

    C_ISW_3 = ISW(prng=prng, order=2).transform(C)
    C_ISW_3.in_place_remove_unused_nodes()
    C_ISW_3.print_stats()
    RawSerializer().serialize_to_file(C_ISW_3, "bin/aes2-isw3.bin")

    C_ISW_4 = ISW(prng=prng, order=3).transform(C)
    C_ISW_4.in_place_remove_unused_nodes()
    C_ISW_4.print_stats()
    RawSerializer().serialize_to_file(C_ISW_4, "bin/aes2-isw4.bin")

    C_MINQ = MINQ(prng=prng).transform(C)
    C_MINQ.in_place_remove_unused_nodes()
    C_MINQ.print_stats()
    RawSerializer().serialize_to_file(C_MINQ, "bin/aes2-minq.bin")

    C_QL2 = QuadLin(prng=prng, n_linear=2).transform(C)
    C_QL2.in_place_remove_unused_nodes()
    C_QL2.print_stats()
    RawSerializer().serialize_to_file(C_QL2, "bin/aes2-quadlin2.bin")

    C_QL3 = QuadLin(prng=prng, n_linear=3).transform(C)
    C_QL3.in_place_remove_unused_nodes()
    C_QL3.print_stats()
    RawSerializer().serialize_to_file(C_QL3, "bin/aes2-quadlin3.bin")

    C_QL4 = QuadLin(prng=prng, n_linear=4).transform(C)
    C_QL4.in_place_remove_unused_nodes()
    C_QL4.print_stats()
    RawSerializer().serialize_to_file(C_QL4, "bin/aes2-quadlin4.bin")


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
    circuit(bytes(args.key, encoding="ascii"))
