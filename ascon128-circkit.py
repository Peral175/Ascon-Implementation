"""
Author: Alex Perrard
ASCON Authenticated Encryption implementation in Python
for Master Thesis at the University of Luxembourg.
"""
import random

import circ_perm_bool as circ_perm
# import circ_perm


def state_to_binary(s):
    i = state_to_int(s)
    b = int_to_bytes(i, 320)
    return bytes_to_binary(b)


def int_to_binary(i):
    arr = []
    binary = bin(i)[2:].zfill(320)
    for i in binary:
        arr.append(i)
    return arr


def bytes_to_binary(byte):
    arr = []
    integer = bytes_to_int(byte)
    binary = bin(integer)[2:]
    for i in binary:
        arr.append(i)
    while len(arr) < 320:
        arr.insert(0, 0)
    return arr


def binary_to_int(b_arr):
    r = "0b"
    for i in b_arr:
        r += str(i)
    r = int(r, base=2)
    return r


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
    return int.from_bytes(b, byteorder='big', signed=False)


def bytes_to_state(S):
    """
    The bytes string contains all 5 64-bit words of the state.
    This function extracts the words and puts them in a list, such that they can be individually manipulated.
    :param S: byte string of the 320-bit state
    :return: list containing 5 64-bit words of the state
    """
    state = []
    for word in range(5):
        state.append(bytes_to_int(S[8 * word:8 * word + 8]))
    return state


def state_to_int(state):
    s = b''
    for i in range(5):
        s += int_to_bytes(state[i], 64)
    return bytes_to_int(s)


def initialization(K, N, len_k, len_n):
    IV = int_to_bytes(0x80400c0600000000, 64)  # hard coded ==> ASCON-128 (64 bits); hex to byte-string
    k = int_to_bytes(K, len_k)  # int to byte-string
    n = int_to_bytes(N, len_n)
    # s = bytes_to_state(IV + k + n)  # concatenate IV with Key and Nonce
    s = bytes_to_binary(IV + k + n)
    p_a = (circ_perm.ascon_perm(s, nr_rounds=12))
    s_int = binary_to_int(p_a) ^ K
    # s_int = state_to_int(p_a) ^ K  # perform permutation on state, followed by XOR-ing the key
    s = bytes_to_state(int_to_bytes(s_int, 320))  # transform to state for later
    return k, s


def processing_associated_data(A, s, len_a, rate):
    if len_a > 0:
        pad = b'\x80' + b'\x00' * (rate // 8 - ((len_a // 8) % (rate // 8)) - 1)
        a = int_to_bytes(A, len_a) + pad
        for i in range(0, len_a, rate):
            # first word is XOR-ed with current associated date block
            s[0] ^= bytes_to_int(a[i:i + rate])
            s_b = state_to_binary(s)
            s = circ_perm.ascon_perm(s_b, nr_rounds=6)
            s = bytes_to_state(int_to_bytes(binary_to_int(s), 320))
    s[4] ^= 1
    return s


def processing_plaintext(P, s, len_p, rate):
    pad = b'\x80' + b'\x00' * ((rate // 8) - ((len_p // 8) % (rate // 8)) - 1)
    p = int_to_bytes(P, len_p) + pad
    # below we split the plain text into blocks of size equal to rate( = 8 bytes)
    blocks = []
    for i in range(0, len(p), rate // 8):  # while loop instead ?
        blocks.append(p[i:i + rate // 8])
    C = b""  # empty ciphertext C
    for i in range(len(blocks) - 1):
        # XOR first word with current block of plaintext
        s[0] ^= bytes_to_int(blocks[i])
        C += int_to_bytes(s[0], 64)  # add the result to the ciphertext
        s_b = state_to_binary(s)
        s = circ_perm.ascon_perm(s_b, nr_rounds=6)
        s = bytes_to_state(int_to_bytes(binary_to_int(s), 320))

    s[0] ^= bytes_to_int(blocks[-1])
    word1_in_binary = bin(s[0]).replace("0b", "")
    while len(word1_in_binary) < 64:
        word1_in_binary = "0" + word1_in_binary

    cut = (len_p % rate)
    if cut != 0:  # todo: is this correct ?
        C_t = word1_in_binary[:cut]  # truncate first word to bitsize of plaintext mod rate
        C_t = int(C_t, base=2)
        C += int_to_bytes(C_t, cut)
    return s, C


def processing_ciphertext(C, s, rate):
    blocks = []
    len_c = (bin(bytes_to_int(C)).replace("0b", "").__len__() + 1) // 8 * 8
    for i in range(0, len_c // 8, rate // 8):
        blocks.append(C[i:i + (rate // 8)])
    # print(blocks, len(blocks[-1]), bytes_to_int(blocks[-1]).bit_length())

    if len(blocks[-1]) == 8:
        blocks.append(b'\x00')  # todo: verify this
    # print(blocks, len(blocks[-1]), bytes_to_int(blocks[-1]).bit_length())

    P = b""
    for i in range(len(blocks) - 1):
        P_i = int_to_bytes(s[0] ^ bytes_to_int(blocks[i]), 64)
        P += P_i
        s[0] = bytes_to_int(blocks[i])
        s_b = state_to_binary(s)
        s = circ_perm.ascon_perm(s_b, nr_rounds=6)
        s = bytes_to_state(int_to_bytes(binary_to_int(s), 320))

    cipher_bits = len_c
    word1_in_binary = bin(s[0]).replace("0b", "")
    while len(word1_in_binary) < 64:
        word1_in_binary = "0" + word1_in_binary
    cut = (cipher_bits % 64)
    if cut != 0:
        P_t = int(word1_in_binary[:cut], base=2) ^ bytes_to_int(blocks[-1])
        P_t = int_to_bytes(P_t, cut)
        P += P_t
        P_t += b'\x80' + b'\x00' * (rate // 8 - ((cipher_bits // 8) % (rate // 8)) - 1)
        s[0] ^= bytes_to_int(P_t) % 2 ** 64
    else:
        P_t = int(0) ^ bytes_to_int(blocks[-1])
        P_t = int_to_bytes(P_t, cut)
        P += P_t
        P_t += b'\x80' + b'\x00' * (rate // 8 - ((cipher_bits // 8) % (rate // 8)) - 1)
        s[0] ^= bytes_to_int(P_t) % 2 ** 64
    return P, s


def finalize(k, s):
    z = bytes_to_int(k + b'\x00' * 16)
    tmp = bytes_to_state(int_to_bytes(state_to_int(s) ^ z, 320))
    s_b = state_to_binary(s)
    s = circ_perm.ascon_perm(s_b, nr_rounds=12)
    s = bytes_to_state(int_to_bytes(binary_to_int(s), 320))

    s_binary = bin(state_to_int(s)).replace("0b", "")
    k_binary = bin(bytes_to_int(k)).replace("0b", "")
    short_s = s_binary[len(s_binary) - 128:]
    short_k = k_binary[len(k_binary) - 128:]
    T = int(short_s, base=2) ^ int(short_k, base=2)
    return T


def auth_enc(K, N, A, P, len_a, len_k, len_n, len_p, rate):
    k, s = initialization(K, N, len_k, len_n)  # Initialization
    s = processing_associated_data(A, s, len_a, rate)  # Processing Associated Data
    s, C = processing_plaintext(P, s, len_p, rate)  # Processing Plaintext
    T = finalize(k, s)  # Finalization
    return C, T


def verif_dec(K, N, A, C, T, len_a, len_k, len_n, rate):
    k, s = initialization(K, N, len_k, len_n)  # Initialization
    s = processing_associated_data(A, s, len_a, rate)  # Processing Associated Data
    P, s = processing_ciphertext(C, s, rate)  # Processing Ciphertext
    T_prime = finalize(k, s)  # Finalization
    print("Tag from decryption: ", T_prime, hex(T_prime))
    if T == T_prime:
        return P
    return None


def even_mansour():
    # random_bits = random.getrandbits(320)

    pt = 812545564329713676245859916367026775365407289012783556426457997015311926679201529462946091394920
    # b"abcdefghabcdefghabcdefghabcdefghabcdefgh"

    k1 = 812512715624816776440459237248810020064558190857236543862207984151981621179302483734224793854305
    # k2 = 812512715624816776440459237248810020064558190857236543862207984151981621179302483734224793854305
    # b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    pt_b = int_to_binary(pt)
    res = circ_perm.ascon_perm(state=pt_b, key=k1, nr_rounds=1)
    r1 = binary_to_int(res)
    print("output:   ", r1)

    # what about inverse/decryption ?


def main():
    # msg = "hello there ascon!"
    # rate = 64  # 64 bits / 8 bytes for ASCON-128
    # Key = 0x999cc63e91d1b4dd3e9e2f361dccd251
    # Nonce = 0xf794f704aaf2343a9a34a2203fc2162c
    # AssData = 0x4153434f4e  # "ASCON"
    # Plaintext = int(hex(int.from_bytes(msg.encode(), "big")), base=16)  # 0x6173636f6e
    # len_k = (bin(Key).replace("0b", "").__len__() + 1) // 8 * 8
    # len_n = (bin(Nonce).replace("0b", "").__len__() + 1) // 8 * 8
    # len_a = (bin(AssData).replace("0b", "").__len__() + 1) // 8 * 8
    # len_p = (bin(Plaintext).replace("0b", "").__len__() + 1) // 8 * 8
    # print("bit sizes: ", len_k, len_n, len_a, len_p)
    #
    # C, T = auth_enc(Key, Nonce, AssData, Plaintext, len_a, len_k, len_n, len_p, rate)
    # print("Plain text:  ", msg, hex(Plaintext))
    # print("Ciphertext: ", C, hex(int.from_bytes(C, byteorder='big')), "\nTag from encryption: ", T, hex(T))
    # res = verif_dec(Key, Nonce, AssData, C, T, len_a, len_k, len_n, rate)
    # if res is None:
    #     print("Tag did not match!")
    # else:
    #     assert (res.decode() == msg)
    #     print("Verification:", res.decode(), hex(int.from_bytes(res, byteorder='big')))

    even_mansour()


if __name__ == '__main__':
    main()
