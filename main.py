"""
Author: Alex Perrard
ASCON Authenticated Encryption implementation in Python
for academic Master Thesis at the University of Luxembourg.
"""

import secrets

key_len = 128  # or 160 (?)
nonce_len = 128
tag_len = 128  # unused so far (?)
ad_len = 128  # or * ?
msg = """Hello World! Hello there! General Kenobi? Some more text here. \
This message is about long enough I think... OR MAYBE NOT!!!!"""
msg_len = len(msg)
rate = 8  # for ASCON-128


def permA(S):
    crA = [b'\x00\x00\x00\x00\x00\x00\x00\xf0',
           b'\x00\x00\x00\x00\x00\x00\x00\xe1',
           b'\x00\x00\x00\x00\x00\x00\x00\xd2',
           b'\x00\x00\x00\x00\x00\x00\x00\xc3',
           b'\x00\x00\x00\x00\x00\x00\x00\xb4',
           b'\x00\x00\x00\x00\x00\x00\x00\xa5',
           b'\x00\x00\x00\x00\x00\x00\x00\x96',
           b'\x00\x00\x00\x00\x00\x00\x00\x87',
           b'\x00\x00\x00\x00\x00\x00\x00\x78',
           b'\x00\x00\x00\x00\x00\x00\x00\x69',
           b'\x00\x00\x00\x00\x00\x00\x00\x5a',
           b'\x00\x00\x00\x00\x00\x00\x00\x4b']
    return perm(12, S, crA)


def permB(S):
    crB6 = [b'\x00\x00\x00\x00\x00\x00\x00\x96',
            b'\x00\x00\x00\x00\x00\x00\x00\x87',
            b'\x00\x00\x00\x00\x00\x00\x00\x78',
            b'\x00\x00\x00\x00\x00\x00\x00\x69',
            b'\x00\x00\x00\x00\x00\x00\x00\x5a',
            b'\x00\x00\x00\x00\x00\x00\x00\x4b']
    crB8 = [b'\x00\x00\x00\x00\x00\x00\x00\xb4',
            b'\x00\x00\x00\x00\x00\x00\x00\xa5',
            b'\x00\x00\x00\x00\x00\x00\x00\x96',
            b'\x00\x00\x00\x00\x00\x00\x00\x87',
            b'\x00\x00\x00\x00\x00\x00\x00\x78',
            b'\x00\x00\x00\x00\x00\x00\x00\x69',
            b'\x00\x00\x00\x00\x00\x00\x00\x5a',
            b'\x00\x00\x00\x00\x00\x00\x00\x4b']
    n = 6
    if n == 6:
        return perm(n, S, crB6)
    else:
        return perm(n, S, crB8)


def perm(n, S, cr):
    """
    Round transformation
    320-bit PERMUTATION
    1. Addition
    2. Substitution Layer
    3. Linear Diffusion
    :param n:
    :param S:
    :param cr:
    :return None: (S is modified in place)
    """
    # round constant addition
    #
    x0 = bytes_to_int(S[0:8])
    x1 = bytes_to_int(S[8:16])
    x2 = bytes_to_int(S[16:24])
    x3 = bytes_to_int(S[24:32])
    x4 = bytes_to_int(S[32:40])

    for i in range(n):
        x2 ^= bytes_to_int(cr[i])

    # substitution layer
    #
    Sbox = [0x4, 0xb, 0x1f, 0x14, 0x1a, 0x15, 0x9, 0x2,
            0x1b, 0x5, 0x8, 0x12, 0x1d, 0x3, 0x6, 0x1c,
            0x1e, 0x13, 0x7, 0xe, 0x0, 0xd, 0x11, 0x18,
            0x10, 0xc, 0x1, 0x19, 0x16, 0xa, 0xf, 0x17]  # ASCON's 5-bit S-box
    # todo: verify + parallelize
    x0 ^= x4;           x4 ^= x3;           x2 ^= x1
    t0 = x0 & (~x4);    t1 = x2 & (~x1)
    x0 ^= t1;           t1 = x4 & (~x3)
    x2 ^= t1;           t1 = x1 & (~x0)
    x4 ^= t1;           t1 = x3 & (~x2)
    x1 ^= t1;           x3 ^= t0
    x1 ^= x0;           x3 ^= x2;           x0 ^= x4;       x2 ^= ~x2

    # Linear Diffusion Layer
    #
    x0 = x0 ^ (rotr(x0, 19)) ^ (rotr(x0, 28))
    x1 = x1 ^ (rotr(x1, 61)) ^ (rotr(x1, 39))
    x2 = x2 ^ (rotr(x2, 1)) ^ (rotr(x2, 6))
    x3 = x3 ^ (rotr(x3, 10)) ^ (rotr(x3, 17))
    x4 = x4 ^ (rotr(x4, 7)) ^ (rotr(x4, 41))

    x0 = int_to_bytes(x0, 64)
    x1 = int_to_bytes(x1, 64)
    x2 = int_to_bytes(x2, 64)
    x3 = int_to_bytes(x3, 64)
    x4 = int_to_bytes(x4, 64)

    S = x0 + x1 + x2 + x3 + x4
    return S


def rotr(x, i):
    # from https://stackoverflow.com/questions/63759207/circular-shift-of-a-bit-in-python-equivalent-of-fortrans-ishftc
    return ((x << i) % (1 << 64)) | (x >> (64 - i))


def int_to_bytes(i, bits):
    i = i % 2 ** bits
    return i.to_bytes(length=(bits // 8))


def bytes_to_int(b):
    return int.from_bytes(b)


def bytes_to_state(S):
    state = []
    for word in range(5):
        state.append(S[8 * word:8 * word + 8])
    return state


def auth_enc(K, N, A, P):
    """
    ASCON Authenticated Encryption Function
    :param K:
    :param N:
    :param A:
    :param P:
    :return: C,T
    """
    # Init
    IV = 0x80400c0600000000  # hard coded
    IV = int_to_bytes(IV, 64)  # 320 - 128 - 128 = 64 bits = 8 bytes
    K = int_to_bytes(K, 128)
    N = int_to_bytes(N, 128)
    S = IV + K + N  # concatenate IV with Key and Nonce
    z = b'\x00' * 24 + K
    # print("Z:", len(z))
    S = bytes_to_int(permA(S)) ^ bytes_to_int(z)  # XOR
    S = int_to_bytes(S, 320)  # back to byte array for later

    # Processing Associated Data
    if ad_len > 0:  # A.bit_length()
        pad = b'\x80' + b'\x00' * (rate - (ad_len % rate) - 1)
        A = int_to_bytes(A, 128) + pad

        for i in range(ad_len):
            tmp = bytes_to_int(S[:rate]) ^ bytes_to_int(A[i:i + rate])
            tmp = int_to_bytes(tmp, 64) + S[rate:]
            S = permB(tmp)

    S = int_to_bytes(bytes_to_int(S) ^ 1, 320)
    state = bytes_to_state(S)
    # print("STATE:" + str(state))

    # Processing Plaintext
    pad = b'\x80' + b'\x00' * (rate - (msg_len % rate) - 1)
    P += pad
    blocks = []
    for i in range(0, len(P), rate):
        blocks.append(P[i:i + rate])

    C = b""
    for i in range(len(blocks) - 1):
        state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(blocks[i]), 64)
        C += state[0]
        S = permB(state[0] + state[1] + state[2] + state[3] + state[4])
        state = bytes_to_state(S)

    state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(blocks[-1]), 64)
    C += state[0]
    bl = bytes_to_int(state[0])
    bla = bin(bl).replace("0b", "")
    # print("§: ", state[0], bla, hex(bl))
    plaintext_bits = len(msg.encode("utf8"))
    tmp = bla[:(plaintext_bits % rate)]
    C_t = int(tmp, base=2)
    # print("§: ", C_t, int_to_bytes(C_t, 64))
    C += int_to_bytes(C_t, 64)
    S = bytes_to_int(state[0] + state[1] + state[2] + state[3] + state[4])
    z = bytes_to_int(b'\x00' + K + b'\x00' * 23)
    S = permA(int_to_bytes(S ^ z, 320))
    S = bytes_to_int(S)
    blaa_s = bin(S).replace("0b", "")
    kk = bytes_to_int(K)
    blaa_k = bin(kk).replace("0b", "")
    tr1 = blaa_s[len(blaa_s)-128:]
    tr2 = blaa_k[len(blaa_k)-128:]
    T = int(tr1, base=2) ^ int(tr2, base=2)
    return C, T


def verif_dec(K, N, A, C, T):
    """
    ASCON Verified Decryption Function
    :param K:
    :param N:
    :param A:
    :param C:
    :param T:
    :return: Plaintext P or ERROR
    """
    # Init
    IV = 0x80400c0600000000
    IV = int_to_bytes(IV, 64)  # 320 - 128 - 128 = 64 bits = 8 bytes
    K = int_to_bytes(K, 128)
    N = int_to_bytes(N, 128)
    S = IV + K + N  # concatenate IV with Key and Nonce
    z = b'\x00' * 24 + K
    S = bytes_to_int(permA(S)) ^ bytes_to_int(z)  # XOR
    S = int_to_bytes(S, 320)  # back to byte array for later

    # Processing Associated Data
    if ad_len > 0:  # A.bit_length()
        pad = b'\x80' + b'\x00' * (rate - (ad_len % rate) - 1)
        A = int_to_bytes(A, 128) + pad

        for i in range(ad_len):
            tmp = bytes_to_int(S[:rate]) ^ bytes_to_int(A[i:i + rate])
            tmp = int_to_bytes(tmp, 64) + S[rate:]
            S = permB(tmp)

    S = int_to_bytes(bytes_to_int(S) ^ 1, 320)
    state = bytes_to_state(S)
    # print("STATE:" + str(state))

    # Processing Ciphertext
    blocks = []
    for i in range(0, len(C), rate):
        blocks.append(C[i:i + rate])
    if len(blocks[-1]) == 8:
        blocks.pop()
    P = b""
    for i in range(len(blocks) - 1):
        P_i = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(blocks[i]), 64)
        P += P_i
        state[0] = blocks[i]
        S = permB(state[0] + state[1] + state[2] + state[3] + state[4])
        state = bytes_to_state(S)

    cipher_bits = len(blocks[-1])*8
    print(blocks[-1])
    P_t = bytes_to_int(state[0][:cipher_bits]) ^ bytes_to_int(blocks[-1])
    p_t = int_to_bytes(P_t, 64)
    print(p_t)
    P += p_t

    state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(p_t), 64)
    S = bytes_to_int(state[0] + state[1] + state[2] + state[3] + state[4])
    z = bytes_to_int(b'\x00' + K + b'\x00' * 23)
    S = permA(int_to_bytes(S ^ z, 320))
    S = bytes_to_int(S)
    blaa_s = bin(S).replace("0b", "")
    kk = bytes_to_int(K)
    blaa_k = bin(kk).replace("0b", "")
    tr1 = blaa_s[len(blaa_s)-128:]
    tr2 = blaa_k[len(blaa_k)-128:]
    T_prime = int(tr1, base=2) ^ int(tr2, base=2)
    print(T)
    print(T_prime)
    print(P)
    if T == T_prime:
        return P
    else:
        return Exception("Tag is incorrect!")


def main():
    K = secrets.randbits(key_len)
    N = secrets.randbits(nonce_len)  # todo: verify if fine
    A = secrets.randbits(ad_len)  # todo: change according to 2.4.2
    # P = secrets.randbits(msg_len)       # todo: some message in bytes ?
    P = str.encode(msg)
    C, T = auth_enc(K, N, A, P)
    print("Plain text: ", P)
    print("Ciphertext: ", C, "\nTag: ", T)
    res = verif_dec(K, N, A, C, T)
    print("Verification: ", res)


if __name__ == '__main__':
    main()
