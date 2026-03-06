## Session — 2026-02-24
Hash tables as the underlying mechanism behind Python dict O(1) lookup.

### Hash Table
A data structure that trades memory for speed. A hash function converts a key into a numeric memory address. Retrieval recomputes the same hash to jump directly to that address — one step, regardless of the size of the structure.

### Hash Function Properties
A hash function must be deterministic: the same input always produces the same output. This allows the address to be re-derived on demand rather than stored. Hash functions do not guarantee uniqueness — collisions (two different keys producing the same hash) are mathematically inevitable when mapping an infinite input space to a finite address space.

### Why Dict Keys Must Be Immutable
If a key could change after insertion, its hash would change, pointing to a different memory address. The stored value would become unreachable. Python enforces immutability on keys (strings, integers, tuples are allowed; lists are not) to guarantee that the hash remains stable.

### Collision Handling
When two keys hash to the same address, Python uses collision resolution to store both and adds a small comparison step at retrieval to return the correct value. Performance degrades slightly but correctness is preserved.
