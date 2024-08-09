from Ascon_P import perm
import argparse
import json
from random import randbytes
from Ascon128 import binary_to_int

parser = argparse.ArgumentParser(
    description='Ascon AEAD implementation',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    '-K',
    '--key',
    type=str,
    help='key to use in encryption'
)
args = parser.parse_args()


def even_mansour():

    with open("myconfig.json", "r") as f:
        data = json.load(f)
    try:
        k1 = bytes(args.key, encoding="utf-8")
    except TypeError:
        k1 = bytes(data.get("key1"), encoding="utf-8")
    print("key1: ", k1, type(k1))

    pt = b"aaaaaaaabbbbbbbbccccccccddddddddeeeeeeee"
    nam = data.get("naming")
    # res = perm(state=pt, key=k1, nr_rounds=2, naming=nam, SERIALIZE=True, STATS=True, NCA=True)
    res = perm(state=pt, key=k1, nr_rounds=2, naming=nam, SERIALIZE=True, STATS=True, NCA=True, OBFUS=True)
    res = binary_to_int(res)
    print("output:   ", res)

    k2 = bytes(data.get("key2"), encoding='utf-8')
    print("key2: ", k2, type(k2))

    """
    In order to decrypt the ciphertext we would need the inverse permutation.
    Also, in whitebox model, the encryption is more important to be secure than the decryption. 
    """


if __name__ == "__main__":
    even_mansour()
