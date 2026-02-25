# Conversations — control-flow

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Dict comme alternative à `if/elif` — quand utiliser l'un ou l'autre

**[Explication]**
En Python, avant `match/case` (3.10), on utilisait des dicts comme tables de lookup pour remplacer les chaînes `if/elif/else`.

```python
time_switch = {
    'morning': 'What do you eat for your breakfast?',
    'noon': 'What do you eat for lunch?',
    'afternoon': 'What do you eat for tea time?',
    'evening': 'What do you eat for diner?'
}
print(time_switch.get(time, 'fallback message'))
```

vs. `if/elif` classique :
```python
if time == 'morning':
    print('What do you eat for your breakfast?')
elif time == 'noon':
    ...
else:
    print('fallback message')
```

Règle de décision :
- Conditions **discrètes et statiques** → dict (O(1), plus lisible, modifiable dynamiquement)
- Conditions impliquant **ranges, logique, expressions complexes** → `if/elif`

**Performance** : `if/elif` est O(n) — chaque condition est évaluée en séquence. Dict lookup est O(1) via hash table. À 4 branches c'est négligeable ; à 50+ (routing tables, event dispatchers), la différence est réelle.

**CASE WHEN en SQL** = équivalent direct de `if/elif` (ou du dict as switch pour des valeurs discrètes) :
```sql
CASE
  WHEN condition1 THEN result1
  WHEN condition2 THEN result2
  ELSE default_result
END
```

**[Insight clé]** Quand tu vois un `if/elif` dans du code, demande-toi : "les conditions sont-elles discrètes et statiques ?" Si oui, un dict est probablement meilleur.

---
