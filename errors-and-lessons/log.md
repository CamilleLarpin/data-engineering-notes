# Journal d'erreurs & leçons apprises

| Date | Module | Erreur / Problème | Leçon apprise |
|------|--------|-------------------|---------------|
| 27/02/2026 | data-handling/numpy | Used `np.zeros(100).reshape(10, 10)` instead of `np.zeros((10, 10))` | `np.zeros()` accepts a shape tuple directly — reshape is redundant here |
| 27/02/2026 | data-handling/numpy | 4 separate slice assignments for borders instead of 2 | Use `f[[0, -1], :] = 1` and `f[:, [0, -1]] = 1` — `-1` selects last element for any size; scalar broadcasts automatically |
| 27/02/2026 | data-handling/pandas | Used `'np.nan'` (string) instead of `np.nan` in `.replace()` call | `np.nan` is a float value, not a string. Also `.replace()` must be assigned or use `inplace=True` — without it, the DataFrame is unchanged |

## [2026-03-06] Quiz error — terminal
**Q**: What syntax is used to define an alias in Zsh?
**A**: zsh?
**Feedback**: The student answered "zsh?" rather than providing the alias syntax. The correct syntax is `alias name="full command"`, where `name` is the shorthand you want to use and the full command is what it expands to.

## [2026-03-06] Quiz error — terminal
**Q**: Why are aliases typically stored in ~/.zshrc rather than entered directly in the terminal?
**A**: for secutiry reason
**Feedback**: Aliases are stored in `~/.zshrc` for **persistence**, not security — an alias entered directly in the terminal only lasts for the current session and is lost when the terminal closes. Storing it in `~/.zshrc` ensures it is automatically available in every new session.
