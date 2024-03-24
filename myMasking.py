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


class CubeLin(MaskingTransformer):
    """Cubic Monomial + Linear shares [Seker,Eisenbarth,Liśkiewicz 2021]"""

    NAME_SUFFIX = "_CubeLin"

    def __init__(self, *args, n_linear=2, **kwargs):
        self.n_linear = int(n_linear)
        super().__init__(*args, n_shares=3 + n_linear, **kwargs)

    def encode(self, s):
        tx0 = self.rand()
        tx1 = self.rand()
        tx2 = self.rand()
        lins = [self.rand() for _ in range(self.n_linear-1)]
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
        W = (
             ((tr2 & (tx0 ^ r0)) & (tr1 ^ (tx1 ^ r0))) ^
             ((tr1 & (tx2 ^ r0)) & (tr0 ^ (tx0 ^ r0))) ^
             ((tr0 & (tx1 ^ r0)) & (tr2 ^ (tx2 ^ r0)))
            )
        # W = (tr0 & (tx1 ^ r0)) ^ ((tr1 & (tx0 ^ r0)))
        R = (
             ((tr0 ^ r0) & (tr1 ^ r0) & (tr2 ^ r0)) ^
             (r0 & ((tr2 & (tx0 ^ r0)) ^ (tr1 & (tx0 ^ r0)) ^ (tr0 & (tx1 ^ r0)))) ^
             (r0 & ((tr2 & (tx1 ^ r0)) ^ (tr1 & (tx2 ^ r0)) ^ (tr0 & (tx2 ^ r0))))
            )
        # R = ((tr0 ^ r0) & (tr1 ^ r0)) ^ r0
        x[-1] ^= W ^ R
        return tx0, tx1, tx2, Array(x)

    def visit_XOR(self, node, x, y):
        tx0, tx1, tx2, x = self.refresh(x)
        ty0, ty1, ty2, y = self.refresh(y)

        tz0 = tx0 ^ ty0
        tz1 = tx1 ^ ty1
        tz2 = tx2 ^ ty2

        z = x ^ y
        # U = (tx0 & ty1) ^ (tx1 & ty0)
        U = ((tx1 & ((tx2 & ty0) ^ (ty2 & (tx0 ^ ty0)))) ^
             (ty1 & ((tx2 & ty0) ^ (tx0 & (tx2 ^ ty2)))))
        z[-1] ^= U
        return tz0, tz1, tz2, z

    def visit_AND(self, node, x, y):
        tx0, tx1, tx2, x = self.refresh(x)
        ty0, ty1, ty2, y = self.refresh(y)
        n = len(x)

        r0  = Array(self.rand() for _ in range(n))
        r1  = Array(self.rand() for _ in range(n))
        r2  = Array(self.rand() for _ in range(n))

        tz0 = (tx0 & ty1) ^ xorlist(r0)
        tz1 = (tx1 & ty2) ^ xorlist(r1)
        tz2 = (tx2 & ty0) ^ xorlist(r2)

        r = {}
        for i in range(n+1):
            ii = i - 1
            for j in range(i+1, n+1):
                jj = j - 1
                if i == 0:
                    # r[j,0] = (
                    #     (tx1 & ((tx0&y[jj]) ^ (r0[jj]&ty0)))
                    #     ^ (ty1 & ((ty0&x[jj]) ^ (r1[jj]&tx0)))
                    #     ^ (r1[jj]  & xorlist(r0))
                    r[j,0] = (
                          (tx0 & ((tx2 & ((tx1 & y[jj]) ^ (r0[jj] & ty0))) ^ (r1[jj] & xorlist(r2) & ty1)))
                        ^ (ty0 & ((ty1 & ((ty2 & x[jj]) ^ (r1[jj] & tx2))) ^ (r0[jj] & xorlist(r1) & tx2)))
                        ^ (tx0 & ty1 & ((r1[jj] & tx2 & ty0) ^ (r2[jj] & tx1 & ty2)))
                        ^ (r0[jj] & tx1 & ty2 & (xorlist(r2) ^ (tx2 & ty0)))
                        ^ (tx2 & ty0 & ((r0[jj] & tx0) ^ (r1[jj] & ty1)))
                        ^ (xorlist(r1) & xorlist(r2) & r0[jj])
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
        return tz0, tz1, tz2, Array(z)

    def visit_NOT(self, node, x):
        lins = Array(x[3])
        lins[-1] = 1 ^ lins[-1]
        return x[0], x[1], x[2], lins


