from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt

# Verify Qiskit Aer installation
try:
    from qiskit_aer import Aer
    print("Qiskit Aer imported successfully!")
except ImportError as e:
    print("Error importing Qiskit Aer:", e)

# Function to create a random bit string
def random_bit_string(length):
    return ''.join(np.random.choice(['0', '1'], size=length))

# Function to create a random basis string
def random_basis_string(length):
    return ''.join(np.random.choice(['X', 'Z'], size=length))

# Function to encode bits using the chosen bases
def encode_bits(bits, bases):
    qc = QuantumCircuit(len(bits), len(bits))
    for i, (bit, basis) in enumerate(zip(bits, bases)):
        if basis == 'X':  # Hadamard basis
            qc.h(i)
        if bit == '1':
            qc.x(i)
    return qc

# Function to measure qubits using the chosen bases
def measure_qubits(qc, bases):
    for i, basis in enumerate(bases):
        if basis == 'X':  # Hadamard basis
            qc.h(i)
        qc.measure(i, i)
    return qc

# Alice's random bits and bases
alice_bits = random_bit_string(8)
alice_bases = random_basis_string(8)

# Bob's random bases
bob_bases = random_basis_string(8)

# Alice encodes her bits
qc = encode_bits(alice_bits, alice_bases)

# Bob measures the qubits
qc = measure_qubits(qc, bob_bases)

# Simulate the circuit
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
sim_result = simulator.run(compiled_circuit).result()
counts = sim_result.get_counts()
bob_bits = list(counts.keys())[0]

# Compare Alice's and Bob's bits and bases
shared_key_indices = [i for i in range(len(alice_bases)) if alice_bases[i] == bob_bases[i]]
alice_key = ''.join([alice_bits[i] for i in shared_key_indices])
bob_key = ''.join([bob_bits[i] for i in shared_key_indices])

print("Alice's bits: ", alice_bits)
print("Alice's bases: ", alice_bases)
print("Bob's bases: ", bob_bases)
print("Bob's bits: ", bob_bits)
print("Shared key (Alice): ", alice_key)
print("Shared key (Bob): ", bob_key)

# Plot the results
plot_histogram(counts)
plt.show()
