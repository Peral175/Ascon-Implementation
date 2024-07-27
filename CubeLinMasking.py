from functools import reduce
from operator import xor
import logging
from wboxkit.masking import MaskingTransformer
from circkit.transformers.core import CircuitTransformer
from circkit.array import Array

log = logging.getLogger(__name__)


def xorlist(lst):
    return reduce(xor, lst, 0)


class CubeLin(MaskingTransformer):
    """Cubic Monomial + Linear shares [Seker,Eisenbarth,Liśkiewicz 2021]"""
    NAME_SUFFIX = "_CubeLin"

    def __init__(self, *args, n_linear=2, **kwargs):
        self.n_linear = int(n_linear)
        super().__init__(*args, n_shares=3 + n_linear, **kwargs)    # n_shares = 3

    def encode(self, s):
        tx0 = self.rand()
        tx1 = self.rand()
        tx2 = self.rand()
        lins = [self.rand() for _ in range(self.n_linear - 1)]
        lins.append(xorlist(lins) ^ (tx0 & tx1 & tx2) ^ s)
        return tx0, tx1, tx2, Array(lins)

    def decode(self, x):
        return (x[0] & x[1] & x[2]) ^ xorlist(x[3])

    def refresh(self, x):
        tx0, tx1, tx2, lins = x

        tr0 = self.rand()  # tilde r0
        tr1 = self.rand()  # tilde r1
        tr2 = self.rand()  # tilde r2

        tx0 ^= tr0
        tx1 ^= tr1
        tx2 ^= tr2

        x = list(lins)
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                r = self.rand()
                x[i] ^= r
                x[j] ^= r

        r0 = self.rand()
        W = tr1 & tr2 & (tx0 ^ r0) ^ tr0 & tr1 & (tx2 ^ r0) ^ tr0 & tr2 & (tx1 ^ r0) ^ tr2 & (tx0 ^ r0) & (
                    tx1 ^ r0) ^ tr1 & (tx0 ^ r0) & (tx2 ^ r0) ^ tr0 & (tx1 ^ r0) & (tx2 ^ r0)
        R = (tr0 ^ r0) & (tr1 ^ r0) & (tr2 ^ r0) ^ tr2 & r0 & (tx0 ^ tx1) ^ tr1 & r0 & (tx0 ^ tx2) ^ tr0 & r0 & (
                    tx1 ^ tx2) ^ r0
        x[-1] ^= W ^ R
        return tx0, tx1, tx2, Array(x)

    def visit_XOR(self, node, x, y):
        tx0, tx1, tx2, x = self.refresh(x)
        ty0, ty1, ty2, y = self.refresh(y)

        tz0 = tx0 ^ ty0
        tz1 = tx1 ^ ty1
        tz2 = tx2 ^ ty2

        z = x ^ y
        U = ((tx1 & ((tx2 & ty0) ^ (ty2 & (tx0 ^ ty0)))) ^
             (ty1 & ((tx2 & ty0) ^ (tx0 & (tx2 ^ ty2)))))
        z[-1] ^= U
        return tz0, tz1, tz2, z

    def visit_AND(self, node, x, y):
        tx0, tx1, tx2, x = self.refresh(x)
        ty0, ty1, ty2, y = self.refresh(y)
        n = len(x)

        r0 = Array(self.rand() for _ in range(n))
        r1 = Array(self.rand() for _ in range(n))
        r2 = Array(self.rand() for _ in range(n))

        tz0 = (tx0 & ty1) ^ xorlist(r0)
        tz1 = (tx1 & ty2) ^ xorlist(r1)
        tz2 = (tx2 & ty0) ^ xorlist(r2)

        r = {}
        for i in range(n + 1):
            ii = i - 1
            for j in range(i + 1, n + 1):
                jj = j - 1
                if i == 0:
                    r[j, 0] = (
                            (tx0 & ((tx2 & ((tx1 & y[jj]) ^ (r0[jj] & ty0))) ^ (r1[jj] & xorlist(r2) & ty1)))
                            ^ (ty0 & ((ty1 & ((ty2 & x[jj]) ^ (r1[jj] & tx2))) ^ (r0[jj] & xorlist(r1) & tx2)))
                            ^ (tx0 & ty1 & ((r1[jj] & tx2 & ty0) ^ (r2[jj] & tx1 & ty2)))
                            ^ (r0[jj] & tx1 & ty2 & (xorlist(r2) ^ (tx2 & ty0)))
                            ^ (tx2 & ty0 & ((r0[jj] & tx0) ^ (r1[jj] & ty1)))
                            ^ (xorlist(r1) & xorlist(r2) & r0[jj])
                    )
                else:
                    r[i, j] = self.rand()
                    r[j, i] = (r[i, j] ^ (x[ii] & y[jj])) ^ (x[jj] & y[ii])

        z = [None] * n
        for i in range(1, n + 1):
            ii = i - 1
            z[ii] = x[ii] & y[ii]
            for j in range(n + 1):
                if j != i:
                    z[ii] ^= r[i, j]
        return tz0, tz1, tz2, Array(z)

    def visit_NOT(self, node, x):
        lins = Array(x[3])
        lins[-1] = 1 ^ lins[-1]
        return x[0], x[1], x[2], lins

#########################################################################################
# DEBUGGING BELOW
#
# from wboxkit.prng import NFSR, Pool
# from circkit.boolean import OptBooleanCircuit as BooleanCircuit
# nfsr = NFSR(taps=[[], [11], [50], [3, 107]], clocks_initial=100, clocks_per_step=1,)
# prng = Pool(prng=nfsr, n=256)
# C = BooleanCircuit(name="debug")
# pt = Array(C.add_inputs(2, "x%d"))
# x0 = pt[0]
# x1 = pt[1]
# x2 = x1 ^ x0
# x3 = x1 & x0
# x4 = ~x0
# x5 = x1 ^ x1
# x6 = x1 & x1
# x7 = x0 ^ x0
# x8 = x0 & x0
# # C1:  [0, 1, 1, 0, 1, 0, 0, 1, 0]
# C.add_output([x0, x1, x2, x3, x4, x5, x7, x6, x8])
# C.in_place_remove_unused_nodes()
# inp = [1, 0]
# out = C.evaluate(inp)           # regular circuit
# print("C1: ", out)
# ASCON_CL = CubeLin( n_linear=1).transform(C)
# ASCON_CL.in_place_remove_unused_nodes()
# # ASCON_CL.print_stats()
# out2 = ASCON_CL.evaluate(inp)
# print("C2: ", out2)
# assert out2 == out
#
# # Assertion fails only sometimes ==> refresh must be the problem --> yes, fixed
