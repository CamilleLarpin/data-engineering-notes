# Fiche — Data Types & Data Structures

## Concept

> Core Python data types (strings, lists, sets, dictionaries) and their key operations — including how Python's dict uses hash tables under the hood.

## En une phrase

Python's built-in data structures each have a specific purpose: lists for ordered sequences, sets for unique values, dicts for key-value lookups (O(1) via hash tables).

## Explication simple

### Operators
| Operator | Symbol | Example | Result |
|---|---|---|---|
| Power | `**` | `2 ** 3` | 8 |
| Division | `/` | `7 / 2` | 3.5 |
| Integer division | `//` | `7 // 2` | 3 |
| Modulo | `%` | `7 % 2` | 1 |

### Strings
- `.find('x')` — returns the lowest index of a substring, `-1` if not found (no crash)
- `.index('x')` — same, but raises `ValueError` if not found
- `.format()` — inserts values: `'{} loves {}'.format('Mary', 'Python')`
- **f-strings** (preferred): `f"{name} loves {thing}"` — more readable and faster

### Lists
- `.append(x)` — adds **one element** to the end. Warning: `list.append([1,2])` inserts a list-in-a-list
- `.extend([x, y])` — merges another list's **elements** into the list

### Sets
- Unordered collection of **unique** values — automatically removes duplicates
- `set(lst)` — converts a list to a set, dropping duplicates

### Dictionaries
- `dict.get('key')` — safe lookup, returns `None` (or a custom default) if key doesn't exist
- `dict['key']` — direct lookup, raises `KeyError` if key doesn't exist
- **Dict as switch pattern**: replace `if/elif` chains with a dict for discrete, known conditions → O(1) vs O(n)

### Hash Tables (how dicts work internally)
- A hash function converts a key → memory address (e.g. `'morning'` → 4782)
- Retrieval = recompute hash → jump directly to address → **O(1)**
- The function is **deterministic**: same input always → same output (address is re-derived, never stored)
- **Collisions** (two keys → same address) are inevitable but handled internally — never silently returns wrong value
- **Keys must be immutable**: if a key changed, its hash would change → value becomes unreachable

## Analogie

A dictionary is like a library with a perfect index: instead of scanning every shelf (O(n)), you look up the index, get an exact shelf number, and go directly (O(1)).

## Exemple concret

```python
# Dict as switch — O(1) lookup, safe fallback
time_switch = {
    'morning': 'Breakfast?',
    'noon':    'Lunch?',
    'evening': 'Dinner?'
}
print(time_switch.get(time, 'Invalid time'))  # no KeyError

# Set for deduplication
cities = ['Tokyo', 'Berlin', 'Tokyo', 'Paris']
unique_cities = set(cities)  # → {'Tokyo', 'Berlin', 'Paris'}

# List operations
numbers = [1, 2, 3]
numbers.append(4)       # [1, 2, 3, 4]
numbers.extend([5, 6])  # [1, 2, 3, 4, 5, 6]
numbers.append([7, 8])  # [1, 2, 3, 4, 5, 6, [7, 8]] ← list-in-a-list!
```

## Commandes / Code clés

```python
# String methods
'hello world'.find('l')       # → 2  (no crash if not found)
'hello world'.index('l')      # → 2  (ValueError if not found)
f"{name} loves {thing}"       # f-string (preferred over .format())

# Safe vs unsafe dict lookup
d.get('key', 'default')       # → 'default' if missing, no crash
d['key']                      # → KeyError if missing

# Deduplication
unique = set(['a', 'b', 'a']) # → {'a', 'b'}
sorted(unique)                # → ['a', 'b'] (sets are unordered — sort for predictable output)
```

## À retenir

- `dict.get(key, default)` → safe; `dict[key]` → `KeyError` if missing
- Dict lookup = **O(1)** (hash table); `if/elif` = **O(n)** — use dicts for discrete, static conditions
- Hash function is **deterministic** and re-computed on every lookup — no stored mapping needed
- Dict keys must be **immutable** — mutable keys (like lists) would break hash lookup
- `set()` is the fastest way to deduplicate a list; always `sorted()` for predictable order
- `list.append()` adds one element; `list.extend()` merges a list — don't confuse them
