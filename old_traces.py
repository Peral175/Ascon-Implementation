from wboxkit.fastcircuit import FastCircuit

# plaintext = b'hello there ascon!'
plaintext = (1097225512173192901620296578338726613688202740309944764736862352059861986321020448584864249076747).to_bytes(40, byteorder='big', signed=False)
print("Input:", plaintext)
FC = FastCircuit("circuits/ascon128-clear.bin")
ciphertext = FC.compute_one(plaintext, trace_filename="traces/test-1-clear")
print("Output:", ciphertext, "\n", ciphertext.hex(), "\n",  int.from_bytes(ciphertext, byteorder='big'))

# """Process finished with exit code 139 (interrupted by signal 11:SIGSEGV)""" error stems from above

# ciphertexts = FC.compute_batch(
#     [b'Hello ascon1', b'Hello ascon2'] * 4,
#     trace_filename="traces/test-2-clear"
# )
# print(ciphertexts)
#
# with open("traces/test-2-clear", "rb") as f:
#     print(f.read(128).hex())

# with open("traces/test-1-clear", "rb") as f:
#     print("Read hex: ", f.read(32).hex())

# wboxkit.trace -T 256 circuits/aes10.bin traces/
# ls -al traces/aes10/ | tail
print("Traces: ")
with open("traces/ascon128-clear/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()
# d30ea3957a490a4d2a0ab3aac5156a6d9f827f20f20e3cc24cf15c6a85b6f5b2 why?

with open("traces/ascon128-isw_3/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()

with open("traces/ascon128-minq/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()

with open("traces/ascon128-ql/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()

with open("traces/ascon128-cl/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()

with open("traces/ascon128-ds/0000.bin", "rb") as f:
    print(f.read(32).hex())
f.close()

# Why are all the same except clear ascon?
# Trace Boolean circuit serialized by wboxkit on random inputs --> random? ==> bad circuits

# wboxkit.exact traces/ascon128-clear/
# how to specify ascon? --> expand wboxkit with ASCON? ==> DONE
