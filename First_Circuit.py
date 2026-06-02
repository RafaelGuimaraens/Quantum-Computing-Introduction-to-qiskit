from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

# NOTE: The millisecond timings shown below come from a classical software
# simulation of quantum properties (via Qiskit Aer). Real quantum hardware
# is still in active development and would produce very different — and
# likely inconsistent — execution times. These numbers should NOT be used
# to benchmark quantum vs. classical performance in practice.

target = '11'

# ─── CLASSICAL SEARCH ─────────────────────────────────────────
items = ['00', '01', '10', '11']

start = time.perf_counter()
classical_steps = 0

for item in items:
    classical_steps += 1
    if item == target:
        break

end = time.perf_counter()
classical_time = end - start

print("=== CLASSICAL SEARCH ===")
print(f"Target '{target}' found in {classical_steps} step(s)")
print(f"Time: {classical_time*1000:.4f} ms\n")

# ─── QUANTUM SEARCH (GROVER) ──────────────────────────────────
qc = QuantumCircuit(2, 2)

# Step 1: superposition — explores all states simultaneously
qc.h(0)
qc.h(1)

# Step 2: oracle — marks the target state '11' with a negative phase
qc.cz(0, 1)

# Step 3: diffusion — amplifies the marked state
qc.h(0)
qc.h(1)
qc.x(0)
qc.x(1)
qc.cz(0, 1)
qc.x(0)
qc.x(1)
qc.h(0)
qc.h(1)

# Measurement
qc.measure([0, 1], [0, 1])

start = time.perf_counter()
sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
end = time.perf_counter()
quantum_time = end - start

counts = result.get_counts()
most_likely = max(counts, key=counts.get)
confidence = counts[most_likely] / 1024 * 100

print("=== QUANTUM SEARCH (GROVER) ===")
print(f"Most likely result: '{most_likely}' with {confidence:.1f}% confidence")
print(f"Full distribution: {counts}")
print(f"Simulation time: {quantum_time*1000:.4f} ms")
print("(!) This time reflects a classical simulation of quantum behavior,")
print("    not real quantum hardware execution.\n")

print("=== COMPARISON ===")
print(f"Classical: {classical_steps} sequential step(s)")
print(f"Quantum:   1 iteration, all states explored simultaneously")
print(f"For N=4 items, Grover needs at most ~√4 = 2 iterations")
print(f"For N=1,000,000, classical needs up to 1,000,000 steps")
print(f"For N=1,000,000, Grover needs only ~1,000 iterations")
