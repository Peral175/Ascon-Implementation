# Ascon Implementation in Python

This project is done as a Master Thesis at the University of Luxembourg.

It is meant for academic purposes only.

## Getting started:
It is recommended to take a look at Dependencies.txt to get working versions of libraries.\
1. Generate and serialize circuits by running AES.py or Even_Mansour.py and providing a valid key.
2. Generate traces for said circuits by running the bash scripts aes_script.sh or ascon_script.sh.
3. Exact match and LDA attacks can be conducted by calling the respective files directly and providing the path to the traces or by calling the test suite attack_testing.py.

Below are some explanations about the files and what they contain.

## Files:
### AES.py --Key
AES-128 Boolean circuit creation and serialization.\
Requires 128-bit key as command line argument --Key

### AES_ExactMatch.py trace_dir -T
Exact match attack on AES-128 Boolean circuit\
Requires path to traces directory as command line argument trace_dir
and the number of traces to be used -T

### AES_LDA.py trace_dir -T -W -S
Linear Decoding Analysis on AES-128 Boolean circuit\
Requires path to traces directory as command line argument trace_dir
, the number of traces to be used -T, the size for the sliding window -W and the stepsize for the sliding window -S

### aes_script.sh
Bash script to generate circuits by calling AES.py, and then generating traces based on these circuits.



### Ascon128.py
Python implementation of Ascon-128 AEAD

### Ascon_P.py --Key
Ascon permutation function (Ascon-p) Boolean circuit creation and serialization.\
Requires 320-bit key as command line argument --Key\
This file should be called from Ascon128.py of Even_Mansour.py

### Even_Mansour.py --Key
Even-Mansour construction using two cryptographic keys and Ascon-P (unkeyed permutation) to create a very simple block cipher.
Requires 320-bit key as command line argument --Key\

### Ascon_ExactMatch.py trace_dir -T
Exact match attack on Ascon-P Boolean circuit\
Requires path to traces directory as command line argument trace_dir
and the number of traces to be used -T

### Ascon_LDA.py trace_dir -T -W -S
Linear Decoding Analysis on Ascon-P Boolean circuit\
Requires path to traces directory as command line argument trace_dir
, the number of traces to be used -T, the size for the sliding window -W and the stepsize for the sliding window -S

### CubeLinMasking.py
Python implementation of Cubic Monomial + Linear shares from SEL 2021.\
Non-linear masking with 3 non-linear shares and a variable amount of linear shares.

### ascon_script.sh
Bash script to generate (obfuscated) circuits by calling Even_Mansour.py, and then generating traces based on these circuits.
Parameter in Even_Mansour.py must be set to OBFUS=True

### ascon_obfus_script.sh
Bash script to generate circuits by calling Even_Mansour.py, and then generating traces based on these circuits.

### obfuscated_masking.py
Contains ObfuscatedTransformer from circkit library, to transform circuits into obfuscated circuits.\
visit_XOR, visit_AND, visit_NOT have parameters to choose the obfuscation design and random nodes to be used.

### attack_testing.py
Test suite where exact match and LDA attacks are conducted on the previously generated circuits, using the generated traces.

### Dependencies.txt
File containing the dependencies of Python libraries to run the code, and some advice to get started.
