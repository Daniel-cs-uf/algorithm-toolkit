# Algorithm Toolkit

A small collection of classic algorithm-design problems solved from scratch in
Python and C++, each with a short technical write-up explaining the approach,
correctness argument, and complexity.

## Contents

| Folder | Problem | Technique | Language |
|--------|---------|-----------|----------|
| [`stable-matching`](stable-matching) | Stable matching between two equal-size sets of preferences | Shapley algorithm | Python |
| [`highway-coverage-greedy`](highway-coverage-greedy) | Cover a highway of off-ramps with the fewest service locations | Greedy interval covering | Python |
| [`crate-stacking-recursion`](crate-stacking-recursion) | Move a stack of crates between racks under ordering constraints | Recursion (Tower of Hanoi) | Python |
| [`optimal-line-breaking-dp`](optimal-line-breaking-dp) | Break a paragraph into lines minimizing total "slack" cost | Dynamic programming | Python |
| [`fast-exponentiation-benchmark`](fast-exponentiation-benchmark) | Compute large powers efficiently and benchmark time/memory | Divide-and-conquer exponentiation by squaring | C++ |

## Highlights

- **Stable matching** — implements the Shapley proposal algorithm, reading
  preference lists from a file and producing a stable assignment in `O(n²)`.
- **Greedy highway coverage** — a single left-to-right sweep that provably uses
  the minimum number of locations to cover every off-ramp within range.
- **Crate stacking** — recursive solution mirroring the Tower of Hanoi
  recurrence `T(n) = 2T(n-1) + 1`.
- **Optimal line breaking** — the dynamic-programming formulation used by real
  text justifiers, minimizing the sum of squared trailing slack across lines.
- **Fast exponentiation** — exponentiation by squaring in `O(log n)`
  multiplications, with timing and peak-memory instrumentation.

Each subfolder contains the source code.

## Running

The Python programs run with any Python 3 interpreter, e.g.:

```bash
python stable-matching/matching.py
```

The C++ benchmark compiles with any modern C++ compiler:

```bash
g++ -O2 fast-exponentiation-benchmark/powerTests.cpp -o power
```
