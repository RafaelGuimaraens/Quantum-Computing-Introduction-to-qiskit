# ⚛️ Quantum Computing — Introduction to Qiskit

> A hands-on introduction to quantum computing using IBM's Qiskit framework, covering foundational concepts from qubits and quantum gates to Grover's search algorithm and its real-world applications.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Requirements & Installation](#requirements--installation)
- [Part 1 — What is a Qubit?](#part-1--what-is-a-qubit)
- [Part 2 — Superposition & The Bloch Sphere](#part-2--superposition--the-bloch-sphere)
- [Part 3 — Quantum Gates](#part-3--quantum-gates)
- [Part 4 — Building Your First Circuit](#part-4--building-your-first-circuit)
- [Part 5 — The Mathematics of Quantum State Vectors](#part-5--the-mathematics-of-quantum-state-vectors)
- [Part 6 — Grover's Search Algorithm](#part-6--grovers-search-algorithm)
- [Part 7 — Real-World Application: Fraud Detection](#part-7--real-world-application-fraud-detection)
- [Part 8 — Classical vs Quantum: Benchmark](#part-8--classical-vs-quantum-benchmark)
- [Next Steps](#next-steps)
- [References](#references)

---

## Overview

This repository documents the first steps in Quantum Computing using **Qiskit 2.4.1** and **Qiskit-Aer 0.17.2**. It covers the core building blocks of quantum computation and implements Grover's Search Algorithm — one of the most celebrated quantum algorithms — which provides a provable quadratic speedup over classical search.

**Key topics covered:**
- Qubits, quantum states, and measurement
- Superposition and the Bloch Sphere
- Quantum gates as matrix transformations
- Circuit construction in Qiskit
- Grover's Algorithm: oracle, diffusion, and amplitude amplification
- Simulation using AerSimulator

---

## Repository Structure

```
Quantum-Computing-Introduction-to-qiskit/
│
├── First_Circuit.py        # First quantum circuit + Grover's algorithm implementation
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Requirements & Installation

**Python 3.8+** is required.

```bash
# 1. Clone the repository
git clone https://github.com/RafaelGuimaraens/Quantum-Computing-Introduction-to-qiskit.git
cd Quantum-Computing-Introduction-to-qiskit

# 2. Create a virtual environment (recommended)
python -m venv venv_quantum

# Activate — Linux/macOS
source venv_quantum/bin/activate

# Activate — Windows
venv_quantum\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

**requirements.txt**
```
qiskit==2.4.1
qiskit-aer==0.17.2
```

> ⚠️ **Important:** Never name your Python files `qiskit.py`, `numpy.py`, or any name that matches a library you import. Python will try to import your file instead of the actual library and raise an `ImportError`.

---

## Part 1 — What is a Qubit?

A classical bit can only be **0 or 1**. A **qubit** (quantum bit) can exist in a combination of both states simultaneously — a phenomenon called **superposition**.

The general state of a qubit is written using Dirac notation:

```
|ψ⟩ = α|0⟩ + β|1⟩
```

Where:
- `|0⟩` and `|1⟩` are the two basis states (analogous to classical 0 and 1)
- `α` and `β` are **complex numbers** called **probability amplitudes**
- The fundamental constraint is: **|α|² + |β|² = 1**

The probability of measuring each state follows the **Born Rule**:

```
P(measuring 0) = |α|²
P(measuring 1) = |β|²
```

**Key distinction:**
```
Classical bit:   IS 0 or IS 1  (definite value at all times)
Qubit:           EXISTS as both simultaneously (until measured)
```

Measurement causes the qubit to **collapse** — it irreversibly picks one state. This is not a limitation of technology; it is a fundamental property of quantum mechanics.

---

## Part 2 — Superposition & The Bloch Sphere

Every possible state of a single qubit can be represented as a point on the surface of a unit sphere called the **Bloch Sphere**.

```
                    |0⟩  (north pole)
                     │
                     │
  |−⟩ ───────────── ● ─────────────── |+⟩
                     │
                     │
                    |1⟩  (south pole)
```

The general parametric form using two angles is:

```
|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ) · sin(θ/2)|1⟩
```

| Parameter | Range | Meaning |
|-----------|-------|---------|
| θ (theta) | 0° to 180° | Mixture between \|0⟩ and \|1⟩ |
| φ (phi)   | 0° to 360° | Relative phase between states |

**Special states:**

| θ | φ | State | Description |
|---|---|-------|-------------|
| 0° | any | \|0⟩ | Pure zero — north pole |
| 180° | any | \|1⟩ | Pure one — south pole |
| 90° | 0° | \|+⟩ = (\|0⟩+\|1⟩)/√2 | Perfect superposition |
| 90° | 180° | \|−⟩ = (\|0⟩−\|1⟩)/√2 | Superposition with phase |

> **Why does phase (φ) matter if it doesn't change probabilities?**
> Phase becomes critical when qubits interact or when multiple gates are applied sequentially. Phases can interfere constructively or destructively — and this interference is exactly what quantum algorithms exploit to amplify the correct answer.

---

## Part 3 — Quantum Gates

Quantum gates are **unitary matrix transformations** applied to qubit state vectors. All quantum gates are reversible.

### Hadamard Gate (H)

The most important gate for creating superposition:

```
H = (1/√2) · [ 1   1 ]
              [ 1  -1 ]
```

Effect:
```
H|0⟩ = (|0⟩ + |1⟩)/√2    →  50% chance of 0, 50% chance of 1
H|1⟩ = (|0⟩ - |1⟩)/√2    →  50% chance of 0, 50% chance of 1 (different phase)
```

### Pauli-X Gate (NOT Gate)

Classical NOT equivalent — flips the qubit:
```
X = [ 0  1 ]
    [ 1  0 ]

X|0⟩ = |1⟩
X|1⟩ = |0⟩
```

### Controlled-Z Gate (CZ)

A two-qubit gate. Applies a phase flip **only** when both qubits are |1⟩:
```
CZ|00⟩ =  |00⟩
CZ|01⟩ =  |01⟩
CZ|10⟩ =  |10⟩
CZ|11⟩ = -|11⟩   ← phase flipped
```

This gate is the oracle used in Grover's algorithm for a 2-qubit system targeting |11⟩.

### CNOT Gate (Controlled-NOT)

Flips qubit 1 only when qubit 0 is |1⟩. Used to create entanglement:
```
CNOT|00⟩ = |00⟩
CNOT|01⟩ = |01⟩
CNOT|10⟩ = |11⟩
CNOT|11⟩ = |10⟩
```

---

## Part 4 — Building Your First Circuit

A quantum circuit in Qiskit is a sequence of gates applied to qubits, followed by measurement.

```python
from qiskit import QuantumCircuit

# Create a circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)

# Apply Hadamard gate — creates superposition
qc.h(0)

# Measure qubit 0 → store result in classical bit 0
qc.measure(0, 0)

print(qc.draw())
```

**Circuit diagram:**
```
     ┌───┐ ░ ┌─┐
  q: ┤ H ├─░─┤M├
     └───┘ ░ └─┘
           ░
c: 1/══════════╝
               0
```

**Running on the simulator:**

```python
from qiskit_aer import AerSimulator

sim = AerSimulator()
job = sim.run(qc, shots=1024)
counts = job.result().get_counts()

print(counts)
# Output: {'0': ~512, '1': ~512}
```

The qubit starts in `|0⟩`. After Hadamard, it enters perfect superposition. Each of the 1024 measurements independently collapses to 0 or 1 with equal probability, producing an approximately 50/50 distribution.

---

## Part 5 — The Mathematics of Quantum State Vectors

### Multi-Qubit Systems

With 2 qubits, the state space has **4 basis vectors**:

```
|00⟩, |01⟩, |10⟩, |11⟩
```

The general state is:

```
|ψ⟩ = α₀₀|00⟩ + α₀₁|01⟩ + α₁₀|10⟩ + α₁₁|11⟩
```

With normalization: `|α₀₀|² + |α₀₁|² + |α₁₀|² + |α₁₁|² = 1`

### After Applying Hadamard to Both Qubits

```
H⊗H|00⟩ = (1/2)(|00⟩ + |01⟩ + |10⟩ + |11⟩)
```

Each amplitude = 1/2, each probability = (1/2)² = **25%**

This is the uniform superposition — all 4 states equally likely. This is the starting point for Grover's algorithm.

### The Diffusion Operator

The diffusion operator reflects the state vector about the uniform superposition `|s⟩`:

```
D = 2|s⟩⟨s| - I
```

For each amplitude, the transformation is:

```
new_amplitude(x) = 2·mean(all amplitudes) − old_amplitude(x)
```

This is a reflection about the mean — states below the mean are pushed up, states above are pushed down.

---

## Part 6 — Grover's Search Algorithm

Grover's algorithm solves the **unstructured search problem**: given a function `f(x)` that returns 1 for exactly one input (the target) and 0 for all others, find the target with as few evaluations of `f` as possible.

**Classical complexity:** O(N) — up to N evaluations  
**Grover's complexity:** O(√N) — approximately π/4 · √N iterations

### The Algorithm — Step by Step

#### Step 1: Initialization
Apply Hadamard to all qubits — creates uniform superposition over all N states.

```
Amplitudes: [ 1/√N,  1/√N,  1/√N,  ...,  1/√N ]
```

#### Step 2: Oracle
The oracle marks the target state by flipping its amplitude sign:

```
Before oracle: [ +1/√N,  +1/√N,  +1/√N,  +1/√N ]
After oracle:  [ +1/√N,  +1/√N,  +1/√N,  -1/√N ]  ← target marked
```

The probabilities are **still equal** after the oracle — the phase change is invisible to direct measurement. The oracle has embedded information about the target into the phase structure of the quantum state.

> **Key insight:** The oracle doesn't "find" the target. It is a mathematical function that you construct, embodying the criterion for what you're looking for. It evaluates that criterion for **all states simultaneously** because they exist in superposition.

#### Step 3: Diffusion (Amplitude Amplification)
The diffusion operator reflects all amplitudes about the mean:

```
For N=4, target = |11⟩:

Before diffusion: [+0.5,  +0.5,  +0.5,  -0.5]
Mean = (0.5 + 0.5 + 0.5 - 0.5) / 4 = 0.25

After diffusion:
  |00⟩: 2×0.25 − 0.50 =  0.00  →  P = 0%
  |01⟩: 2×0.25 − 0.50 =  0.00  →  P = 0%
  |10⟩: 2×0.25 − 0.50 =  0.00  →  P = 0%
  |11⟩: 2×0.25 − (−0.50) = 1.00  →  P = 100%
```

#### Step 4: Repeat & Measure

For N items, repeat oracle + diffusion **k = ⌊π/4 · √N⌋** times, then measure.

```
Amplitude narrowing by iteration (N = 1,000,000):

Iteration 1:    target ≈ 0.3%
Iteration 100:  target ≈ 10%
Iteration 500:  target ≈ 70%
Iteration 785:  target ≈ 99.9%  ← optimal k = π/4 · √N ≈ 785
Iteration 900:  target ≈ 80%    ← overshot! probability decreases
```

> **Why does probability decrease after the optimal iteration?**  
> Grover's algorithm is a **geometric rotation** in the Hilbert space. Each iteration rotates the state vector by a fixed angle `2θ` where `sin(θ) = 1/√N`. The optimal point is when the total rotation reaches π/2 (pointing directly at the target). Continuing past this point rotates away from it — like a pendulum swinging past vertical.

### Geometric Interpretation

The algorithm lives in a 2D plane spanned by two vectors:
- `|t⟩` — the target state
- `|s⊥⟩` — the uniform superposition over all non-target states

```
|t⟩ ↑
    │         ← state after k optimal iterations
    │       ↗
    │     ↗ (each iteration = rotation by 2θ)
    │   ↗
    │ ↗ θ (initial angle)
    └──────────────────→ |s⊥⟩
```

Each oracle + diffusion pair rotates the state vector by `2θ` toward `|t⟩`. After `π/4·√N` rotations, the vector points almost directly at `|t⟩` — measurement yields the target with near-certainty.

### Implementation

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

target = '11'

# ── CLASSICAL SEARCH ───────────────────────────────────────────
items = ['00', '01', '10', '11']
start = time.perf_counter()
steps = 0

for item in items:
    steps += 1
    if item == target:
        break

classical_time = time.perf_counter() - start
print(f"Classical: found '{target}' in {steps} step(s) | {classical_time*1000:.4f} ms")

# ── GROVER'S ALGORITHM ────────────────────────────────────────
qc = QuantumCircuit(2, 2)

# Step 1: Superposition over all 4 states
qc.h(0)
qc.h(1)

# Step 2: Oracle — marks |11⟩ by flipping its phase
qc.cz(0, 1)

# Step 3: Diffusion — amplifies the marked state
qc.h(0)
qc.h(1)
qc.x(0)
qc.x(1)
qc.cz(0, 1)
qc.x(0)
qc.x(1)
qc.h(0)
qc.h(1)

# Step 4: Measure
qc.measure([0, 1], [0, 1])

start = time.perf_counter()
sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
grover_time = time.perf_counter() - start

counts = result.get_counts()
most_likely = max(counts, key=counts.get)
confidence = counts[most_likely] / 1024 * 100

print(f"Grover:    found '{most_likely}' with {confidence:.1f}% confidence")
print(f"Distribution: {counts}")

# ── COMPARISON ────────────────────────────────────────────────
print(f"\n{'─'*45}")
print(f"  N items     Classical (worst)    Grover (√N)")
print(f"{'─'*45}")
for n in [4, 100, 10_000, 1_000_000, 1_000_000_000]:
    import math
    print(f"  {n:<12,}  {n:<20,}  {math.ceil(math.pi/4 * math.sqrt(n)):,}")
```

**Expected Output:**
```
Classical: found '11' in 4 step(s) | 0.0021 ms
Grover:    found '11' with 97.3% confidence
Distribution: {'11': 996, '00': 9, '01': 10, '10': 9}

─────────────────────────────────────────────
  N items     Classical (worst)    Grover (√N)
─────────────────────────────────────────────
  4             4                    2
  100           100                  8
  10,000        10,000               79
  1,000,000     1,000,000            785
  1,000,000,000 1,000,000,000        24,851
```

> **Note on simulation time:** The Qiskit-Aer simulator runs on classical hardware, so wall-clock time does not reflect the actual speedup of real quantum hardware. The advantage shown above is in **number of oracle evaluations** — the true measure of algorithmic complexity.

---

## Part 7 — Classical vs Quantum: Benchmark

### Algorithm Complexity Summary

| Algorithm | Classical | Grover (Quantum) | Speedup |
|-----------|-----------|-------------------|---------|
| Unstructured search | O(N) | O(√N) | Quadratic |
| Factoring (Shor's) | O(exp(N^1/3)) | O(N³) | Exponential |
| Database search | O(N) | O(√N) | Quadratic |
| Optimization (QAOA) | O(exp(N)) | O(poly(N))* | Exponential* |

*Theoretical for certain problem classes.

### The Quantum Advantage — When It Matters

```
Quantum computers are NOT universally faster.
They provide provable advantages for specific problem structures:

✓ Unstructured search          → Grover's algorithm
✓ Integer factorization        → Shor's algorithm  
✓ Simulating quantum systems   → Native quantum simulation
✓ Certain optimization problems → QAOA
✓ Linear systems (HHL)         → Quantum linear algebra

✗ Sorting already-sorted data  → No advantage
✗ Simple arithmetic            → Classical is faster
✗ Sequential decision making   → Classical is faster
```

### Why Simulate on Classical Hardware?

Real quantum computers today (NISQ era — Noisy Intermediate-Scale Quantum) have:
- Limited qubit counts (100–1000 physical qubits)
- High error rates from decoherence
- Short coherence times (microseconds)
- No full error correction

The Qiskit-Aer simulator allows you to:
- Develop and test quantum algorithms without hardware access
- Prove theoretical speedup through benchmarks
- Publish research and establish expertise before hardware matures

---

## Next Steps

Having completed this introduction, the natural progression is:

```
Current (this repository)
└── Basic circuits, Hadamard gate, Grover's algorithm

Next
├── Bell States — quantum entanglement
├── Quantum Teleportation — entanglement applied
├── Shor's Algorithm — quantum factoring
└── PennyLane — Quantum Machine Learning framework

Advanced
├── Variational Quantum Eigensolver (VQE)
├── Quantum Approximate Optimization Algorithm (QAOA)
├── Quantum Neural Networks
└── Quantum Error Correction
```

**Recommended resources:**
- [Qiskit Textbook](https://learning.quantum.ibm.com) — IBM's official learning platform
- [PennyLane Demos](https://pennylane.ai/qml/) — Quantum Machine Learning tutorials
- Nielsen & Chuang — *Quantum Computation and Quantum Information* (the standard reference)
- [IMPA Summer Program](https://impa.br) — world-class mathematics and quantum computing (Brazil)
- [IBM Quantum Experience](https://quantum.ibm.com) — run circuits on real quantum hardware for free

---

## References

- Grover, L. K. (1996). *A fast quantum mechanical algorithm for database search*. Proceedings of the 28th Annual ACM Symposium on Theory of Computing.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
- IBM Qiskit Documentation: https://docs.quantum.ibm.com
- Born, M. (1926). *Zur Quantenmechanik der Stoßvorgänge*. Zeitschrift für Physik.

---

<div align="center">

**Built with Qiskit 2.4.1 · Python 3.x · First steps in Quantum Computing**

*"If you think you understand quantum mechanics, you don't understand quantum mechanics." — Richard Feynman*

</div>
