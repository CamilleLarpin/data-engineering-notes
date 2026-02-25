# Conversations — data-types-and-data-structures

<!-- Entrées ajoutées par Claude Code à partir des liens partagés -->

## Session du 24 février 2026
<!-- source: (pasted) -->

**[Question/Sujet]** Dictionnaire comme alternative au switch/case — pattern de lookup et performance

**[Explication]**
En Python, pas de `switch/case` natif avant 3.10 (`match/case`). Le pattern classique : utiliser un dict comme table de décision.

```python
time_switch = {
    'morning': 'What do you eat for your breakfast?',
    'noon': 'What do you eat for lunch?',
    'afternoon': 'What do you eat for tea time?',
    'evening': 'What do you eat for diner?'
}
print(time_switch.get(time, 'We can\'t treat your demand. Please enter a correct time.'))
```

`.get(key, default)` : cherche la clé, retourne la valeur si trouvée, sinon le default — pas de `KeyError`, pas de crash.

Comparaison avec `if/elif` :

| | if/elif | Dict lookup |
|---|---|---|
| Lisibilité | Se dégrade à 4+ branches | Flat et clair |
| Performance | O(n) — vérifie chaque condition | O(1) — hash direct |
| Dynamique | Difficile à modifier au runtime | Facile, juste ajouter une clé |

**Performance** : les dicts Python utilisent une hash table — Python calcule le hash de la clé et saute directement à la valeur. Avec `if/elif`, Python évalue chaque condition en ordre. À 50+ branches (routing tables, config maps, event dispatchers), la différence est significative.

Règle : quand les conditions sont **discrètes et connues** → dict. Quand elles impliquent des ranges, de la logique ou des expressions complexes → `if/elif`.

`dict['c']` lève un `KeyError` si la clé n'existe pas. `.get()` est le lookup sécurisé avec fallback.

**[Insight clé]** Dict lookup = O(1) via hash table. `if/elif` = O(n). Pour des conditions discrètes et statiques, préférer le dict — notamment pour routing, mappings, event dispatch, config tables.

---

## Session du 24 février 2026 — Hash Tables
<!-- source: (pasted) -->

**[Question/Sujet]** Qu'est-ce qu'une hash table ? Pourquoi les lookups sont O(1) ?

**[Explication]**
Une hash table échange de la mémoire contre de la vitesse — elle utilise de l'espace supplémentaire pour atteindre O(1) en lookup.

Comment ça fonctionne :
1. On donne une clé (ex : `'morning'`)
2. Une fonction de hachage convertit cette clé en nombre (ex : `'morning' → 4782`)
3. Ce nombre mappe vers un slot en mémoire où la valeur vit
4. Récupération = calculer le hash → sauter au slot. Une étape, quelle que soit la taille.

```
'morning'  →  hash()  →  4782  →  RAM[4782]  ✅ saut direct
```

Analogie : une bibliothèque avec un index parfait. Au lieu de scanner chaque étagère (O(n)), tu consultes l'index, tu obtiens un numéro d'étagère exact, tu vas directement (O(1)).

**Pourquoi un nombre est plus facilement récupérable ?**
Un nombre = une adresse mémoire directe. La RAM est une longue rue avec des maisons numérotées. "Maison 4782" → saut direct. Un nom comme `'morning'` → l'ordinateur ne sait pas où ça se trouve sans chercher. Le hachage convertit une clé imprévisible → une adresse prévisible.

**Comment le computer sait que `'morning'` → 4782 ?**
Il ne stocke pas un mapping. Il **recalcule** le hash à chaque fois :
```python
# Stockage :
hash('morning') → 4782 → écrire valeur en RAM[4782]

# Récupération :
hash('morning') → 4782 → lire RAM[4782]
```
La fonction de hachage est **déterministe** — même input → même output, toujours. L'adresse est re-dérivée à la demande, pas stockée.

**Collisions** (deux clés → même adresse) : inévitables mathématiquement (infinité d'inputs → ensemble fini d'adresses). Python gère ça avec la résolution de collisions — stocke les deux, ajoute une petite étape de comparaison. Dégrade légèrement mais ne retourne jamais silencieusement la mauvaise valeur.

**Pourquoi les clés doivent être immutables ?** Si une clé pouvait changer après insertion, son hash changerait → elle pointerait vers une adresse différente → Python ne pourrait plus jamais la retrouver. La valeur serait orpheline en mémoire. List est mutable → hash changerait → Python l'interdit comme clé de dict.

Les deux propriétés qui comptent :

| Propriété | Signification |
|---|---|
| Déterministe | Même input → même output, toujours |
| Distribution uniforme | Répartit les outputs pour minimiser les collisions |

**En Data Engineering** : hash tables sont partout — Python dicts, index de bases de données, JOINs en SQL/Spark (hash joins), Kafka partition keys, déduplication.

**[Insight clé]** La récupération est O(1) parce que la fonction de hachage est recalculée (pas cherchée) — même input → même adresse. Clés immutables obligatoires : si elles changeaient, leur hash changerait et la valeur serait inaccessible.

---
