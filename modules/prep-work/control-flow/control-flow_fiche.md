# Fiche — control-flow

## 2026-02-24
- Dictionary lookup pattern as elegant switch alternative: `mapping = {'key': 'value'}; mapping.get(key, default)` replaces if/elif chains
- Performance advantage: dictionary lookup is O(1) via hash table vs O(n) for if/elif chains - significant for many conditions (routing tables, config maps, event handlers)
- `.get(key, default)` provides safe lookup without KeyError, eliminating try/except overhead
- Best for discrete, known conditions; use if/elif for ranges or complex logic expressions

---

## Session — 2026-02-24
Dictionary lookup as a performant alternative to if/elif chains, with O(1) vs O(n) trade-off.

### Dict as Switch Pattern
A dictionary maps discrete conditions (keys) to outcomes (values), replacing if/elif chains. Best applied when conditions are known, static, and discrete — such as routing tables, config maps, or event dispatchers.

### Performance Trade-off: Dict vs if/elif
Dict lookup runs in O(1) because Python dicts use a hash table — the key is hashed to a memory address in one step, regardless of the number of entries. if/elif runs in O(n) — Python evaluates each condition sequentially until a match is found. The gap compounds significantly at 50+ branches.

### Safe Lookup with .get()
`.get(key, default)` returns the value if the key exists, or the default if it does not — without raising a KeyError. This avoids the need for try/except blocks for missing-key handling.
