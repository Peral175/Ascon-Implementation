from functools import reduce
from operator import xor
from queue import PriorityQueue
import logging
from circkit.transformers.core import CircuitTransformer
from circkit.array import Array
from wboxkit.containers import Rect

import random   # we use the random library instead of deriving pseudorandom from input
from wboxkit.masking import ISW, MINQ, QuadLin
from wboxkit.prng import NFSR, Pool
from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from wboxkit.ciphers.aes import BitAES
from binteger import Bin

log = logging.getLogger(__name__)


def xorlist(lst):
    return reduce(xor, lst, 0)


class ObfuscatedTransformer(CircuitTransformer):
    NAME_SUFFIX = "_Obfuscated"
    def __init__(self, prng=None, n=2):
        self.prng = prng
        self.n = int(n)

    def rand(self):
        if self.prng is None:
            return self.target_circuit.RND()()
        return self.prng.step()

    def visit_XOR(self, node, x, y):
        c = random.randint(0, 99)
        n = self.n
        if c < 90:
            # original
            return x ^ y
        elif c < 95:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[random.randint(0, n - 1)]
            return ((o ^ x) ^ y) ^ o
        elif c < 98:
            # v2
            nodes = self.target_circuit.nodes[-n:]
            o1 = nodes[random.randint(0, n - 1)]
            o2 = nodes[random.randint(0, n - 1)]
            return (((o1 ^ x) ^ (o2 ^ y)) ^ o1) ^ o2
        elif c < 100:
            # v3
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[random.randint(0, n - 1)]
            return (x & (o ^ y)) ^ ((1 ^ x) & y) ^ (x & (x ^ o))

    def visit_AND(self, node, x, y):
        c = random.randint(0, 99)
        n = self.n
        if c < 90:
            # original
            return x & y
        elif c < 97:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[random.randint(0, n - 1)]
            return ((x ^ o) & y) ^ (o | y) ^ o ^ y
        elif c < 100:
            # v2
            nodes = self.target_circuit.nodes[-n:]
            o1 = nodes[random.randint(0, n - 1)]
            o2 = nodes[random.randint(0, n - 1)]
            return ((x ^ o1) & (y ^ o2)) ^ ((o1 & (o2 ^ y)) ^ (x & o2))

    def visit_NOT(self, node, x):
        c = random.randint(0, 99)
        n = self.n
        if c < 90:
            # original
            return 1 ^ x
        elif c < 97:
            # v1
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[random.randint(0, n - 1)]
            return ((1 ^ o) ^ x) ^ o
        elif c < 100:
            # v2
            nodes = self.target_circuit.nodes[-n:]
            o = nodes[random.randint(0, n - 1)]
            return (x | (1 ^ o)) ^ (x & o) ^ x ^ o


# debugging below

# adjusted prng to smaller size so graph is (somewhat) readable
nfsr = NFSR(taps=[[], [11], [21], [3, 23]],
            clocks_initial=17,
            clocks_per_step=1,)
prng = Pool(prng=nfsr, n=256)

# below simple circuit for debugging and demonstration purposes
C = BooleanCircuit(name="debuggingCircuit")
a = Array(C.add_inputs(25, "a%d"))
s = a[0]
t = a[1]
r = s ^ t   # XOR
u = s & t   # AND
v = ~s      # NOT
C.add_output([s, t, r, u, v])
C.in_place_remove_unused_nodes()
C.print_stats()

C_obfus_1 = ISW(order=1, prng=prng).transform(C)
C_obfus_1.in_place_remove_unused_nodes()
C_obfus_1.print_stats()
# C_obfus_1.digraph().view()

# Here we can chain obfuscation of operators on top of masking schemes
C_obfus_1 = ObfuscatedTransformer(prng=prng, n=2).transform(C_obfus_1)
C_obfus_1.in_place_remove_unused_nodes()
C_obfus_1.print_stats()
# C_obfus_1.digraph().view()

inp = [0] * 25
for _ in range(10000):
    for i in range(25):
        inp[i] = random.getrandbits(1)
    out1 = C.evaluate(inp)
    out2 = C_obfus_1.evaluate(inp)
    # out3 = C_obfus_2.evaluate(inp)
    assert out1 == out2
    # assert out1 == out2 and out2 == out3
