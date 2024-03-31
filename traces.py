from wboxkit.fastcircuit import FastCircuit

# plaintext = b'\x80@\x0c\x06\x00\x00\x00\x00\x99\x9c\xc6>\x91\xd1\xb4\xdd>\x9e/6\x1d\xcc\xd2Q\xf7\x94\xf7\x04\xaa\xf24:\x9a4\xa2?\xc2\x16,'
# print("ASDF", (1456368917841900354909994607035206380306984454581905284118412146294954714463664271767293188202296).to_bytes(40, byteorder='big', signed=False))
# print("ADFG", int.from_bytes(b'R\x12\xa0\x89\xf51K\x98\xe5\xf0\x1c[`E-\xe5huo\x8c+4\x1c\x0c\xa1\xce-\x8a\x18\x92m\xf9\x9d:\xdc\x881\xe0\xeb\xba', byteorder='big'))
# print("ADFG", int.from_bytes(b'\xe3\xceg^\xaaY(e\xe6\xc6\xaf]\xd3\xd4\x03\x87\xa2W5x+\t)k\x8f\xb2\xd4w\x17\x14*&\xfd\x17]\x19\x15\x15\xf1\xf1', byteorder='big'))
###
# not yet fully understood!
plaintext = b'hello there ascon!'

FC = FastCircuit("circuits/ascon128-clear.bin")
ciphertext = FC.compute_one(plaintext, trace_filename="traces/test-1-clear")
print(ciphertext)

# ciphertexts = FC.compute_batch(
#     [b'Hello ascon1', b'Hello ascon2'] * 4,
#     trace_filename="traces/test-2-clear"
# )
# print(ciphertexts)
#
# with open("traces/test-2-clear", "rb") as f:
#     print(f.read(128).hex())

with open("traces/test-1-clear", "rb") as f:
    print(f.read(32).hex())

# CMD: > wboxkit.trace -T 256 circuits/aes10.bin traces/
