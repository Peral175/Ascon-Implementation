from wboxkit.fastcircuit import FastCircuit

plaintext = b'Hello ascon'
FC = FastCircuit("circuits/ascon128-clear.bin")
ciphertext = FC.compute_one(plaintext, trace_filename="traces/test-1-clear")
print(ciphertext)

ciphertexts = FC.compute_batch(
    [b'Hello ascon', b'Hello ascon2'] * 4,
    trace_filename="traces/test-2-clear"
)
print(ciphertexts)

with open("traces/test-2-clear", "rb") as f:
    print(f.read(32).hex())

# CMD: > wboxkit.trace -T 256 circuits/aes10.bin traces/
