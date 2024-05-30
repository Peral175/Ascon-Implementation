import random
from functools import reduce
from operator import xor
from queue import PriorityQueue

import logging

from circkit.transformers.core import CircuitTransformer
from circkit.array import Array

from wboxkit.containers import Rect


log = logging.getLogger(__name__)


def xorlist(lst):
    return reduce(xor, lst, 0)


class MaskingTransformer(CircuitTransformer):
    START_FROM_VARS = True  # ensure all INPUTS are processed first

    def __init__(self, prng=None, n_shares=2, encode_input=True, decode_output=True):
        """rand() -> random bit"""
        if prng is None:
            self.prng = None
        else:
            self.prng = prng

        self.n_shares = int(n_shares)
        assert n_shares >= 1  # maybe 1 is useful for debugging purposes

        self.encode_input = encode_input
        self.decode_output = decode_output

    def rand(self):
        if self.prng is None:
            return self.target_circuit.RND()()
        return self.prng.step()

    def encode(self, x):
        raise NotImplementedError()

    def decode(self, x):
        raise NotImplementedError()

    def refresh(self, x):
        raise NotImplementedError()

    def visit_generic(self, node, *args):
        raise NotImplementedError(f"visiting {node}")

    def __repr__(self):
        return (
            "<MaskingScheme:%s n_shares=%d prng=%r>"
            % (type(self).__name__, self.n_shares, self.prng)
        )

    def before_transform(self, circuit, **kwargs):
        super().before_transform(circuit, **kwargs)

        # create input vars beforehand to initialize the prng
        if self.encode_input:
            inputs = []
            for node in circuit.inputs:
                new_node = super().visit_generic(node)
                inputs.append(new_node)

            if self.prng is not None:
                self.prng.set_state(inputs)

            for old_node, new_node in zip(circuit.inputs, inputs):
                self.result[old_node] = self.encode(new_node)
        else:
            inputs = []
            for node in circuit.inputs:
                shares = []
                for i in range(self.n_shares):
                    new_name = f"{node.operation.name}_share{i}"
                    x = self.target_circuit.add_input(new_name)
                    shares.append(x)
                self.result[node] = shares
                inputs.extend(shares)

            if self.prng is not None:
                self.prng.set_state(inputs)

    def visit_INPUT(self, node):
        return self.result[node]

    def make_output(self, node, result):
        if self.decode_output:
            result = self.decode(result)
        super().make_output(node, result)


class ObfuscatedTransformer(MaskingTransformer):
    # todo: add inputs for users
    START_FROM_VARS = True  # ensure all INPUTS are processed first

    def __init__(self, prng=None, n_shares=2, encode_input=True, decode_output=True):
        super().__init__(prng, n_shares, encode_input, decode_output)
        if prng is None:
            self.prng = None
        else:
            self.prng = prng
        self.n_shares = int(n_shares)
        assert n_shares >= 1  # maybe 1 is useful for debugging purposes
        self.encode_input = encode_input
        self.decode_output = decode_output

    def rand(self):
        if self.prng is None:
            return self.target_circuit.RND()()
        return self.prng.step()

    def visit_XOR(self, node, x, y):
        from random import randint
        c = randint(0, 100)
        n = 2

        if c < 90:
            # original
            return x ^ y

        elif c < 95:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[randint(0, n)]
            return ((o ^ x) ^ y) ^ o

        elif c < 100:
            # v2
            nodes = self.target_circuit.nodes[-n:]
            o1 = nodes[randint(0, n)]
            o2 = nodes[randint(0, n)]
            return (((o1 ^ x) ^ (o2 ^ y)) ^ o1) ^ o2

    def visit_AND(self, node, x, y):
        from random import randint
        c = randint(0, 100)
        n = 2

        if c < 90:
            # original
            return x & y

        elif c < 95:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[randint(0, n)]
            return ((x ^ o) & y) ^ (o & y)

        elif c < 100:
            # v2
            nodes = self.target_circuit.nodes[-n:]
            o1 = nodes[randint(0, n)]
            o2 = nodes[randint(0, n)]
            return ((x ^ o1) & (y ^ o2)) ^ ((o1 & (o2 ^ y)) ^ (x & o2))

    def visit_NOT(self, node, x):
        from random import randint
        c = randint(0, 100)
        n = 2

        if c < 90:
            # original
            return 1 ^ x

        elif c < 100:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[randint(0, n)]
            return ((1 ^ o) ^ x) ^ o


class ISW(ObfuscatedTransformer):
    """Private Circuits [ISW03]"""
    NAME_SUFFIX = "_ISW"

    def __init__(self, *args, order=2, **kwargs):
        n_shares = order + 1
        super().__init__(*args, n_shares=n_shares, **kwargs)

    def encode(self, s):
        x = [self.rand() for _ in range(self.n_shares-1)]
        x.append(xorlist(x) ^ s)
        return Array(x)

    def decode(self, x):
        return xorlist(x)

    def visit_XOR(self, node, x, y):
        return x ^ y

    def visit_AND(self, node, x, y):
        r = [[0] * self.n_shares for _ in range(self.n_shares)]
        for i in range(self.n_shares):
            for j in range(i+1, self.n_shares):
                r[i][j] = self.rand()
                r[j][i] = r[i][j] ^ x[i] & y[j] ^ x[j] & y[i]
        z = x & y
        for i in range(self.n_shares):
            for j in range(self.n_shares):
                if i != j:
                    z[i] = z[i] ^ r[i][j]
        return z

    def visit_NOT(self, node, x):
        x = Array(x)
        x[0] = 1 ^ x[0]
        return x


class MINQ(MaskingTransformer):
    """MINimalist Quadratic Masking [BU18]"""
    NAME_SUFFIX = "_MINQ"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, n_shares=3, **kwargs)

    def encode(self, s):
        a = self.rand()
        b = self.rand()
        c = (a & b) ^ s
        return a, b, c

    def decode(self, x):
        return (x[0] & x[1]) ^ x[2]

    def rand3(self):
        return (self.rand(), self.rand(), self.rand())

    def refresh(self, x, rs=None):
        a, b, c = x
        if rs is None:
            rs = self.rand3()
        ra, rb, rc = rs
        ma = ra & (b ^ rc)
        mb = rb & (a ^ rc)
        rmul = (ra ^ rc) & (rb ^ rc)
        rc ^= ma ^ mb ^ rmul
        a ^= ra
        b ^= rb
        c ^= rc
        return a, b, c

    def visit_XOR(self, node, x, y):
        rxs = ra, rb, rc = self.rand3()
        rys = rd, re, rf = self.rand3()
        a, b, c = self.refresh(x, rs=rxs)
        d, e, f = self.refresh(y, rs=rys)
        x = a ^ d
        y = b ^ e
        ae = a & e
        bd = b & d
        z = c ^ f ^ ae ^ bd
        return x, y, z

    def visit_AND(self, node, x, y):
        rxs = ra, rb, rc = self.rand3()
        rys = rd, re, rf = self.rand3()
        a, b, c = self.refresh(x, rs=rxs)
        d, e, f = self.refresh(y, rs=rys)

        ma = (b & f) ^ (rc & e)
        md = (c & e) ^ (rf & b)
        x = rf ^ (a & e)
        y = rc ^ (b & d)
        ama = a & ma
        dmd = d & md
        rcrf = rc & rf
        cf = c & f
        z = ama ^ dmd ^ rcrf ^ cf
        return x, y, z

    def visit_NOT(self, node, x):
        return x[0], x[1], ~x[2]


class QuadLin(MaskingTransformer):
    """Quadratic Monomial + Linear shares [Seker,Eisenbarth,Liśkiewicz 2021]"""

    NAME_SUFFIX = "_QuadLin"

    def __init__(self, *args, n_linear=2, **kwargs):
        self.n_linear = int(n_linear)
        super().__init__(*args, n_shares=2 + n_linear, **kwargs)

    def encode(self, s):
        tx0 = self.rand()
        tx1 = self.rand()
        lins = [self.rand() for _ in range(self.n_linear-1)]
        lins.append(xorlist(lins) ^ (tx0 & tx1) ^ s)
        return tx0, tx1, Array(lins)

    def decode(self, x):
        return (x[0] & x[1]) ^ xorlist(x[2])

    def refresh(self, x):
        tx0, tx1, lins = x

        tr0 = self.rand()  # tilde r0
        tr1 = self.rand()  # tilde r1

        tx0 ^= tr0
        tx1 ^= tr1

        x = list(lins)
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                r = self.rand()
                x[i] ^= r
                x[j] ^= r

        r0 = self.rand()
        W = (tr0 & (tx1 ^ r0)) ^ ((tr1 & (tx0 ^ r0)))
        R = ((tr0 ^ r0) & (tr1 ^ r0)) ^ r0
        x[-1] ^= W ^ R
        return tx0, tx1, Array(x)

    def visit_XOR(self, node, x, y):
        tx0, tx1, x = self.refresh(x)
        ty0, ty1, y = self.refresh(y)

        tz0 = tx0 ^ ty0
        tz1 = tx1 ^ ty1

        z = x ^ y
        U = (tx0 & ty1) ^ (tx1 & ty0)
        z[-1] ^= U
        return tz0, tz1, z

    def visit_AND(self, node, x, y):
        tx0, tx1, x = self.refresh(x)
        ty0, ty1, y = self.refresh(y)
        n = len(x)

        r0  = Array(self.rand() for _ in range(n))
        r1  = Array(self.rand() for _ in range(n))

        tz0 = (tx0 & ty1) ^ xorlist(r0)
        tz1 = (tx1 & ty0) ^ xorlist(r1)

        r = {}
        for i in range(n+1):
            ii = i - 1
            for j in range(i+1, n+1):
                jj = j - 1
                if i == 0:

                    r[j,0] = (
                        (tx1 & ((tx0&y[jj]) ^ (r0[jj]&ty0)))
                        ^ (ty1 & ((ty0&x[jj]) ^ (r1[jj]&tx0)))
                        ^ (r1[jj]  & xorlist(r0))
                    )
                else:
                    r[i,j] = self.rand()
                    r[j,i] = (r[i,j] ^ (x[ii]&y[jj])) ^ (x[jj]&y[ii])

        z = [None] * n
        for i in range(1, n+1):
            ii = i - 1
            z[ii] = x[ii] & y[ii]
            for j in range(n+1):
                if j != i:
                    z[ii] ^= r[i,j]
        return tz0, tz1, Array(z)

    def visit_NOT(self, node, x):
        lins = Array(x[2])
        lins[-1] = 1 ^ lins[-1]
        return x[0], x[1], lins


# debugging below
from wboxkit.prng import NFSR, Pool
from wboxkit.ciphers.aes import BitAES
from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from binteger import Bin
nfsr = NFSR(taps=[[], [11], [50], [3, 107]], clocks_initial=100, clocks_per_step=1,)
prng = Pool(prng=nfsr, n=256)
# C = BooleanCircuit(name="AES_2_test")
# key = b"abcdefghABCDEFGH"
# plaintext = b"0123456789abcdef"
# pt = C.add_inputs(128)
# ct, k2 = BitAES(pt, Bin(key).tuple, rounds=2)
# C.add_output(ct)
# # C.digraph().view()
# C.in_place_remove_unused_nodes()
# C.print_stats()
# ct = C.evaluate(Bin(plaintext).tuple)
# print(ct)
# C_ISW_2 = ISW(prng=prng, order=1).transform(C)
# # C_ISW_2.digraph().view()
# C_ISW_2.in_place_remove_unused_nodes()
# C_ISW_2.print_stats()
# print(C_ISW_2.evaluate(Bin(plaintext).tuple))

# todo: simpler circuit
C = BooleanCircuit(name="debugging")
a1 = C.add_input("a1")
a2 = C.add_input("a2")
b1 = C.add_input("b1")
b2 = C.add_input("b2")

c = a1 ^ a2
d = b1 ^ b2
e = c & d
e = ~e

C.add_output([c, d, e])
# C.digraph()
C.in_place_remove_unused_nodes()
C.print_stats()

C_obfus_1 = ISW(order=1).transform(C)
C_obfus_1.in_place_remove_unused_nodes()
C_obfus_1.print_stats()
# C_obfus_1.digraph().view()
C_obfus_2 = ISW(order=2).transform(C)
C_obfus_2.in_place_remove_unused_nodes()
C_obfus_2.print_stats()
# C_obfus_2.digraph().view()


inp = [1, 0, 1, 1]
out = C.evaluate(inp)
print("OUT", out)
# inp_shares = [1, 0, 1, 1]
out = C_obfus_1.evaluate(inp)
print("OUT", out)
out = C_obfus_2.evaluate(inp)
print("OUT", out)
