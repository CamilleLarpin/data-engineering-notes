# Journal d'erreurs & leçons apprises

| Date | Module | Erreur / Problème | Leçon apprise |
|------|--------|-------------------|---------------|
| 27/02/2026 | data-handling/numpy | Used `np.zeros(100).reshape(10, 10)` instead of `np.zeros((10, 10))` | `np.zeros()` accepts a shape tuple directly — reshape is redundant here |
| 27/02/2026 | data-handling/numpy | 4 separate slice assignments for borders instead of 2 | Use `f[[0, -1], :] = 1` and `f[:, [0, -1]] = 1` — `-1` selects last element for any size; scalar broadcasts automatically |
| 27/02/2026 | data-handling/pandas | Used `'np.nan'` (string) instead of `np.nan` in `.replace()` call | `np.nan` is a float value, not a string. Also `.replace()` must be assigned or use `inplace=True` — without it, the DataFrame is unchanged |
