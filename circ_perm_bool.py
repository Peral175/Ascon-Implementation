from circkit.boolean import OptBooleanCircuit as BooleanCircuit
from circkit.array import Array
from binteger import Bin

def circ_ascon_perm(state, nr_rounds=12):
    cr = [0xf0, 0xe1, 0xd2, 0xc3, 0xb4, 0xa5, 0x96, 0x87, 0x78, 0x69, 0x5a, 0x4b]
    C = BooleanCircuit(name="ascon_128_perm_boolean")
    pt = Array(C.add_inputs(320, "x%d"))
    x0 = pt[0:64]
    x1 = pt[64:128]
    x2 = pt[128:192]
    x3 = pt[192:256]
    x4 = pt[256:320]
    for r in range(nr_rounds):
        # Round Constant Addition
        # x2 ^= cr[r+12-nr_rounds]
        x2 ^= Array(Bin(cr[r + 12 - nr_rounds], 64))

        # Substitution Layer    -- are these automatically parallelized?
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
    inp = []
    for i in state:
        for j in format(i, '#066b')[2:]:
            inp.append(j)
    out = C.evaluate(inp)

    # C.print_stats()
    # C.digraph()
    # print(out)

    bin_str = ''
    for j in range(320):
        bin_str += str(out[j])
    out = []
    for i in range(0, 320, 64):
        out.append(int(bin_str[i:i+64], 2))
    return out
