"""
Author: Alex Perrard
ASCON Authenticated Encryption implementation in Python
for Master Thesis at the University of Luxembourg.
"""

import secrets

key_len = 128           # upto 160 (?) how does this work?
nonce_len = 128
tag_len = 128
ad_len = 40 # 128            # can be of arbitrary size (?) => I think so
msg = """Hello World! \nThis message will be encrypted using ASCON encryption before promptly being decrypted.\
Let's hope the end result of encrypting and decryption will return this original message.\n\r"""
msg_len = len(msg)
rate = 8                # for ASCON-128
# rate = 16               # for ASCON-128a


def permA(S):
    """
    This function calls the ASCON permutation with 12 rounds.
    It is used in the initialization and finalization phases.
    :param S: The 320-bit state as a byte-string array
    :return: The modified 320-bit state
    """
    # The array below contains the constant values that are added to the state as part of the permutation.
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
    """
    This function calls the ASCON permutation with 6 or 8 rounds.
    It is used in the processing of the associated data and plaintext.
    :param S: The 320-bit state as a byte-string array
    :return: The modified 320-bit state
    """
    # The array(s) below contain the constant values that are added to the state as part of the permutation.
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
    This is the ASCON Round Transformation / 320-bit PERMUTATION.
    It consists of three operations:
        1. Addition
        2. Substitution Layer
        3. Linear Diffusion
    :param n: The number of rounds to perform
    :param S: The 320-bit state as a byte-string array
    :param cr: The array containing the round constants for the first operation.
    :return S: The modified 320-bit state
    """

    ############################
    # 1. Round Constant Addition
    ############################

    # Split state into 5 64-bit words and transform the byte-string into integer values for the 3 operations.
    x0 = bytes_to_int(S[0:8])
    x1 = bytes_to_int(S[8:16])
    x2 = bytes_to_int(S[16:24])
    x3 = bytes_to_int(S[24:32])
    x4 = bytes_to_int(S[32:40])

    for i in range(n):
        x2 ^= bytes_to_int(cr[i])       # The constants in array are added in order to the third word.

    ############################
    # 2. Substitution Layer
    ############################

    Sbox = [0x4, 0xb, 0x1f, 0x14, 0x1a, 0x15, 0x9, 0x2,
            0x1b, 0x5, 0x8, 0x12, 0x1d, 0x3, 0x6, 0x1c,
            0x1e, 0x13, 0x7, 0xe, 0x0, 0xd, 0x11, 0x18,
            0x10, 0xc, 0x1, 0x19, 0x16, 0xa, 0xf, 0x17]  # ASCON's 5-bit S-box      ==> less efficient

    # todo: verify
    # can this be parallelized (?)
    x0 ^= x4;   x4 ^= x3;   x2 ^= x1
    t0 = x0;    t1 = x1;    t2 = x2;    t3 = x3;    t4 = x4
    t0 = ~t0;   t1 = ~t1;   t2 = ~t2;   t3 = ~t3;   t4 = ~t4
    t0 &= x1;   t1 &= x2;   t2 &= x3;   t3 &= x4;   t4 &= x0
    x0 ^= t1;   x1 ^= t2;   x2 ^= t3;   x3 ^= t4;   x4 ^= t0
    x1 ^= x0;   x0 ^= x4;   x3 ^= x2;   x2 = ~x2

    # Alternative:
    # x0 ^= x4;           x4 ^= x3;           x2 ^= x1
    # t0 = x0 & (~x4);    t1 = x2 & (~x1)
    # x0 ^= t1;           t1 = x4 & (~x3)
    # x2 ^= t1;           t1 = x1 & (~x0)
    # x4 ^= t1;           t1 = x3 & (~x2)
    # x1 ^= t1;           x3 ^= t0
    # x1 ^= x0;           x3 ^= x2;           x0 ^= x4;       x2 ^= ~x2

    ############################
    # 3. Linear Diffusion Layer
    ############################

    # XOR with rotations of the word
    x0 = x0 ^ (rotr(x0, 19)) ^ (rotr(x0, 28))
    x1 = x1 ^ (rotr(x1, 61)) ^ (rotr(x1, 39))
    x2 = x2 ^ (rotr(x2,  1)) ^ (rotr(x2,  6))
    x3 = x3 ^ (rotr(x3, 10)) ^ (rotr(x3, 17))
    x4 = x4 ^ (rotr(x4,  7)) ^ (rotr(x4, 41))

    # return the words back into their byte-string form.
    x0 = int_to_bytes(x0, 64)
    x1 = int_to_bytes(x1, 64)
    x2 = int_to_bytes(x2, 64)
    x3 = int_to_bytes(x3, 64)
    x4 = int_to_bytes(x4, 64)

    # Concatenate the words to recover the modified 320-bit state.
    S = x0 + x1 + x2 + x3 + x4
    return S


def rotr(x, i):
    """
    Right rotation function. Used for Linear Diffusion Layer operation in the permutation.
    :param x: 64-bit word in integer form
    :param i: rotation amount
    :return: rotated 64-bit word in integer form
    """
    # from https://stackoverflow.com/questions/63759207/circular-shift-of-a-bit-in-python-equivalent-of-fortrans-ishftc
    return ((x << i) % (1 << 64)) | (x >> (64 - i))


def int_to_bytes(i, bits):
    """
    Convert integer to bytes via the python .to_bytes function.
    :param i: integer value
    :param bits: number of bits determine length of the resulting byte string
    :return: byte string corresponding to the integer value
    """
    i = i % 2 ** bits
    return i.to_bytes(length=(bits // 8), byteorder='big')


def bytes_to_int(b):
    """
    Convert bytes-string to integer value via the python int.from_bytes(...) function
    :param b: byte string
    :return: integer value of b
    """
    return int.from_bytes(b, byteorder='big')


def bytes_to_state(S):
    """
    The bytes string contains all 5 64-bit words of the state.
    This function extracts the words and puts them in a list, such that they can be individually manipulated.
    :param S: byte string of the 320-bit state
    :return: list containing 5 64-bit words of the state
    """
    state = []
    for word in range(5):
        state.append(S[8 * word:8 * word + 8])
    return state


def auth_enc(K, N, A, P):
    """
    ASCON Authenticated Encryption Function
    :param K:   128-bit key
    :param N:   128-bit nonce   ==> Same nonce should never be used twice with the same key
    :param A:   128-bit associated date ==> could be arbitrary long!
    :param P:   arbitrary long plaintext P
    :return C,T: C is the ciphertext (equal length to plaintext), T is the 128-bit Tag
    """
    # Initialization
    IV = 0x80400c0600000000         # hard coded ==> ASCON-128
    # IV = 0x80400c0800000000         # hard coded ==> ASCON-128a
    IV = int_to_bytes(IV, 64)   # hex to byte-string
    K = int_to_bytes(K, key_len)    # int to byte-string
    N = int_to_bytes(N, nonce_len)
    S = IV + K + N                  # concatenate IV with Key and Nonce
    z = b'\x00' * 24 + K            # unnecessary
    S = bytes_to_int(permA(S)) ^ bytes_to_int(z)    # perform permutation on state, followed by XOR-ing the key
    S = int_to_bytes(S, 320)    # transform state to byte array for later use

    # Processing Associated Data
    if ad_len > 0:
        pad = b'\x80' + b'\x00' * (rate - (ad_len % rate) - 1)  # todo: maybe mistake here (?)
        A = int_to_bytes(A, 128) + pad

        for i in range(ad_len):
            # first word is XOR-ed with current associated date block
            tmp = bytes_to_int(S[:rate]) ^ bytes_to_int(A[i:i + rate])
            tmp = int_to_bytes(tmp, 64) + S[rate:]  # concatenate the new first word with the remaining 4 words
            S = permB(tmp)  # 6-round permutation

    S = int_to_bytes(bytes_to_int(S) ^ 1, 320)  # XOR 1 to state
    state = bytes_to_state(S)       # transform byte-string to state for later

    # Processing Plaintext
    pad = b'\x80' + b'\x00' * (rate - (msg_len % rate) - 1)     # todo: maybe mistake here (?); What is the purpose (?)
    P += pad

    # below we split the plain text into blocks of size equal to rate( = 8)
    blocks = []
    for i in range(0, len(P), rate):
        blocks.append(P[i:i + rate])

    C = b""     # ciphertext C
    for i in range(len(blocks) - 1):
        # XOR first word with current block of plaintext
        state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(blocks[i]), 64)
        C += state[0]   # add the result to the ciphertext
        S = permB(state[0] + state[1] + state[2] + state[3] + state[4])     # 6-round permutation
        state = bytes_to_state(S)       # update the state to reflect change that occurred in S

    state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(blocks[-1]), 64)  # last block
    C += state[0]

    word1_in_binary = bin(bytes_to_int(state[0])).replace("0b", "")
    P_bits = len(msg.encode("utf8"))
    C_t = word1_in_binary[:(P_bits % rate)]  # truncate first word to bitsize of plaintext mod rate
    C_t = int(C_t, base=2)
    C += int_to_bytes(C_t, 64)

    # Finalization
    S = bytes_to_int(state[0] + state[1] + state[2] + state[3] + state[4])
    z = bytes_to_int(b'\x00' + K + b'\x00' * 23)
    S = bytes_to_int(permA(int_to_bytes(S ^ z, 320)))
    S_binary = bin(S).replace("0b", "")
    K_binary = bin(bytes_to_int(K)).replace("0b", "")
    short_S = S_binary[len(S_binary)-128:]
    short_K = K_binary[len(K_binary)-128:]
    T = int(short_S, base=2) ^ int(short_K, base=2)
    return C, T


def verif_dec(K, N, A, C, T):
    """
    ASCON Verified Decryption Function
    :param K:   128-bit key
    :param N:   128-bit nonce   ==> Same nonce should never be used twice with the same key
    :param A:   128-bit associated date ==> could be arbitrary long!
    :param C:   ciphertext with equal length to plaintext
    :param T:   128-bit tag
    :return P or E: Plaintext P  if tag is equal to T or ERROR E if not
    """
    # Initialization
    IV = 0x80400c0600000000         # hard coded ==> ASCON-128
    # IV = 0x80400c0800000000         # hard coded ==> ASCON-128a
    IV = int_to_bytes(IV, 64)   # hex to byte-string
    K = int_to_bytes(K, key_len)    # int to byte-string
    N = int_to_bytes(N, nonce_len)
    S = IV + K + N                  # concatenate IV with Key and Nonce
    z = b'\x00' * 24 + K            # unnecessary
    S = bytes_to_int(permA(S)) ^ bytes_to_int(z)    # perform permutation on state, followed by XOR-ing the key
    S = int_to_bytes(S, 320)    # transform state to byte array for later use

    # Processing Associated Data
    if ad_len > 0:
        pad = b'\x80' + b'\x00' * (rate - (ad_len % rate) - 1)  # todo: maybe mistake here (?)
        A = int_to_bytes(A, 128) + pad

        for i in range(ad_len):
            # first word is XOR-ed with current associated date block
            tmp = bytes_to_int(S[:rate]) ^ bytes_to_int(A[i:i + rate])
            tmp = int_to_bytes(tmp, 64) + S[rate:]  # concatenate the new first word with the remaining 4 words
            S = permB(tmp)  # 6-round permutation

    S = int_to_bytes(bytes_to_int(S) ^ 1, 320)  # XOR 1 to state
    state = bytes_to_state(S)       # transform byte-string to state for later

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
    P_t = bytes_to_int(state[0][:cipher_bits]) ^ bytes_to_int(blocks[-1])
    p_t = int_to_bytes(P_t, 64)
    P += p_t

    state[0] = int_to_bytes(bytes_to_int(state[0]) ^ bytes_to_int(p_t), 64)

    # Finalization
    S = bytes_to_int(state[0] + state[1] + state[2] + state[3] + state[4])
    z = bytes_to_int(b'\x00' + K + b'\x00' * 23)
    S = bytes_to_int(permA(int_to_bytes(S ^ z, 320)))
    S_binary = bin(S).replace("0b", "")
    K_binary = bin(bytes_to_int(K)).replace("0b", "")
    short_S = S_binary[len(S_binary)-128:]
    short_K = K_binary[len(K_binary)-128:]
    T_prime = int(short_S, base=2) ^ int(short_K, base=2)
    print("Tag from decryption: ", T_prime)
    if T == T_prime:
        return P
    else:
        return Exception("Tag is incorrect!")


def main():
    # K = secrets.randbits(key_len)
    K = 0xb09b82809083974c550bbc8b632f8ffc
    # N = secrets.randbits(nonce_len)     # todo: verify if fine
    N = 0x65c703699df2a1a98ae627f6853a0953
    # A = secrets.randbits(ad_len)        # todo: change according to 2.4.2
    A = 0x4153434f4e
    # P = secrets.randbits(msg_len)     # todo: some message in bytes ?
    # P = str.encode(msg)
    P = 0x6173636f6e.to_bytes(5, byteorder='big')
    C, T = auth_enc(K, N, A, P)
    print("Plain text: ", P)
    print("Ciphertext: ", C, "\nTag from encryption: ", T)
    res = verif_dec(K, N, A, C, T)
    print("Verification: ", res)        # extra '\x80 ...' wrong or (?)


if __name__ == '__main__':
    main()
