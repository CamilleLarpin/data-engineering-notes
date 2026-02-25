# Quiz — Data Types & Data Structures

---

## Question 1 — MCQ

**Question:** What is the difference between `d.get('key')` and `d['key']` when the key does not exist in the dictionary?

- A) Both return `None`
- B) `d.get('key')` raises a `KeyError`, `d['key']` returns `None`
- C) `d.get('key')` returns `None` (or a custom default), `d['key']` raises a `KeyError`
- D) Both raise a `KeyError`

<details>
<summary>Answer</summary>

**Correct answer: C)**

`.get()` is a safe lookup — returns `None` by default, or a custom fallback with `.get('key', default)`. `d['key']` raises a `KeyError` if the key doesn't exist. Use `.get()` when absence is expected; use `d['key']` when absence means a bug you want to catch.

</details>

---

## Question 2 — Open question

**Question:** Explain why dict lookups are O(1) while `if/elif` chains are O(n). Why does this matter in Data Engineering?

<details>
<summary>Answer</summary>

A Python dict uses a **hash table**: a hash function converts the key to a memory address, and retrieval is a direct jump to that address — one step, regardless of dict size → **O(1)**.

An `if/elif` chain evaluates each condition in order until a match → **O(n)**. At 4 branches it's negligible, but at 50+ (routing tables, event dispatchers, config maps) the difference is significant.

In Data Engineering: hash tables appear in hash joins (SQL/Spark), Kafka partition key routing, and deduplication logic — all performance-critical paths.

</details>

---

## Question 3 — Practical case

**Context:** You have a list of cities with duplicates and you want to print them sorted alphabetically, without duplicates.

```python
cities = ['Tokyo', 'Berlin', 'Helsinki', 'Rio', 'Tokyo', 'Berlin', 'Paris']
```

**Task:** Write the code in one or two lines.

<details>
<summary>Answer</summary>

```python
unique_cities = set(cities)   # remove duplicates
print(sorted(unique_cities))  # → ['Berlin', 'Helsinki', 'Paris', 'Rio', 'Tokyo']
```

Key point: `set()` is unordered — never rely on the iteration order of a set directly. Use `sorted()` to get a predictable, alphabetical result.

</details>
