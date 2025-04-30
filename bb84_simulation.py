from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

# Function to encrypt a message using the shared key
def encrypt_message(message, key):
    encrypted_message = ''.join(str(int(m) ^ int(k)) for m, k in zip(message, key))
    return encrypted_message

# Function to decrypt a message using the shared key
def decrypt_message(encrypted_message, key):
    decrypted_message = ''.join(str(int(e) ^ int(k)) for e, k in zip(encrypted_message, key))
    return decrypted_message

# Function to detect eavesdropping by comparing a subset of bits
def detect_eavesdropping(alice_bits, bob_bits, sample_size):
    sample_indices = np.random.choice(len(alice_bits), sample_size, replace=False)
    alice_sample = ''.join([alice_bits[i] for i in sample_indices])
    bob_sample = ''.join([bob_bits[i] for i in sample_indices])
    return alice_sample == bob_sample

# Alice's random bits and bases
alice_bits = random_bit_string(16)
alice_bases = random_basis_string(16)

# Bob's random bases
bob_bases = random_basis_string(16)

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

# Detect eavesdropping
sample_size = 4  # Number of bits to compare
eavesdropping_detected = not detect_eavesdropping(alice_key, bob_key, sample_size)
if eavesdropping_detected:
    print("Eavesdropping detected. Secure communication is not possible.")
else:
    print("No eavesdropping detected. Secure communication is possible.")
    shared_key = alice_key

    # Encrypt a message
    message = "11001100"  # Example message (must be the same length as the shared key)
    encrypted_message = encrypt_message(message, shared_key)
    print("Original message: ", message)
    print("Encrypted message: ", encrypted_message)

    # Decrypt the message
    decrypted_message = decrypt_message(encrypted_message, shared_key)
    print("Decrypted message: ", decrypted_message)

# Create the animation
fig, ax = plt.subplots(figsize=(10, 6))

# Initialize the plot elements
alice_bits_bars = ax.bar(range(len(alice_bits)), [0]*len(alice_bits), color='blue', alpha=0.6, label='Alice\'s Bits')
alice_bases_bars = ax.bar(range(len(alice_bases)), [0]*len(alice_bases), color='red', alpha=0.3, label='Alice\'s Bases')
bob_bases_bars = ax.bar(range(len(bob_bases)), [0]*len(bob_bases), color='red', alpha=0.3, label='Bob\'s Bases')
bob_bits_bars = ax.bar(range(len(bob_bits)), [0]*len(bob_bits), color='green', alpha=0.6, label='Bob\'s Bits')

ax.set_title("BB84 Quantum Key Distribution")
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.legend()

def update(frame):
    if frame < len(alice_bits):
        alice_bits_bars[frame].set_height(int(alice_bits[frame]))
        alice_bases_bars[frame].set_height(1 if alice_bases[frame] == 'X' else 0)
    elif frame < 2 * len(alice_bits):
        idx = frame - len(alice_bits)
        bob_bases_bars[idx].set_height(1 if bob_bases[idx] == 'X' else 0)
        bob_bits_bars[idx].set_height(int(bob_bits[idx]))
    return alice_bits_bars + alice_bases_bars + bob_bases_bars + bob_bits_bars

ani = animation.FuncAnimation(fig, update, frames=range(2 * len(alice_bits)), blit=True, repeat=False)

# Add text to indicate eavesdropping detection
if eavesdropping_detected:
    plt.figtext(0.5, 0.01, "Eavesdropping detected! Secure communication is not possible.", ha="center", fontsize=12, color="red")
else:
    plt.figtext(0.5, 0.01, "No eavesdropping detected. Secure communication is possible.", ha="center", fontsize=12, color="green")

plt.show()
