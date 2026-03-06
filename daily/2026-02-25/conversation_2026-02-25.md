Good morning! 🌅 New day, new neurons.
Before we dive in — quick check-in:
What's on your agenda today? (new topic, lab work, catching up, etc.)
And to warm up your brain, here's a pop question based on common DE fundamentals:


Pop Question: What's the difference between a data warehouse and a data lake? Give me one key distinction and a use case for each.

Take a shot — even a rough answer tells me where to focus. No pressure to be perfect.data warehouse: structured data, potencially architecture en medaillon VS data lake: high volume, different variety.25 FebEvaluated rough answer and prepared constructive feedbackEvaluated rough answer and prepared constructive feedbackGood instincts, and you're circling the right ideas. Let me sharpen the distinction:
The core difference is schema-on-write vs schema-on-read.
A data warehouse enforces structure before data lands — you define the schema upfront, data is clean and queryable immediately. Fast for analytics, rigid for ingestion. The medallion architecture (bronze/silver/gold) you mentioned is actually a pattern that bridges both worlds — it lives in a lakehouse (Delta Lake, BigQuery, etc.), not strictly a warehouse.
A data lake accepts anything — raw files, JSON, images, logs — and you figure out structure later when you query. Flexible for ingestion, can get messy fast ("data swamp" risk).
So a cleaner frame: warehouse = optimized for querying structured data / lake = optimized for storing everything cheaply.
One correction worth noting: volume and variety are characteristics of big data in general, not what defines a lake specifically.

Follow-up question to lock this in:

In the medallion architecture, what does each layer (bronze / silver / gold) roughly contain, and which layer would analysts typically query?

What's your take?les datasets que je crée ne sont pas visible en drop down dans le panel gauche. Pourquoi?25 FebIdentifié problème de visibilité des datasets BigQueryIdentifié problème de visibilité des datasets BigQueryC'est un comportement normal de BigQuery dans la console GCP.
Le panneau gauche ne montre que les projets que tu as épinglés (starred/pinned). Les datasets que tu vois dans la vue centrale "Datasets" appartiennent bien à ton projet artefact-blend-488313-m6, mais pour les voir dans l'arborescence gauche, il faut que ce projet soit épinglé.
Fix rapide : dans le panneau gauche, clique sur l'étoile ⭐ à côté de ton projet, ou utilise "+ Add data" > "Star a project" et entre ton project ID.
Une fois épinglé, tu verras le projet se déplier avec tes datasets iowa_liquor_sales et sql_advanced directement accessibles.

Petite notion utile à retenir : dans BigQuery, la hiérarchie est Project > Dataset > Table. Le panneau gauche est un explorateur de projets épinglés, pas un explorateur de tous tes projets actifs. C'est différent de ce qu'on attend intuitivement.
Tu travailles sur quoi aujourd'hui dans ces datasets — du SQL avancé ?Quel est le soucis:SELECT
region_name,
COUNT(DISTINCT customer_id) count_customers
FROM `sql_advanced.customers` c LEFT JOIN sql_advanced.regions` r ON r.region_id = c.region_id
GROUP BY region_name
ORDER BY count_customers desc;25 FebIdentifié une syntaxe manquante dans la requête SQLIdentifié une syntaxe manquante dans la requête SQLUn backtick manquant avant sql_advanced.regions :
sqlFROM `sql_advanced.customers` c LEFT JOIN `sql_advanced.regions` r ...
Tu as ouvert le backtick sur customers mais pas sur regions. BigQuery ne peut pas parser le nom de table correctement sans les deux.Erreur?SELECT
  customer_id,
  order_id
  COUNT(order_id) OVER(ORDER BY order_date) sequential_order_id
FROM `sql_advanced.orders`
ORDER BY customer_id, order_date;25 FebVirgule manquante après order_id (ligne 3) :
sql  order_id,
  COUNT(order_id) OVER...# Row Numbering Assign a unique sequential integer to rows within each customer's set of orders. Why ? It can be useful for marketing to know if this order is the first or the fifth.25 FebDeciphered sequential numbering mechanism for customer order trackingDeciphered sequential numbering mechanism for customer order trackingBonne occasion d'utiliser ROW_NUMBER() — la window function faite pour ça :
sqlSELECT
  customer_id,
  order_id,
  order_date,
  ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_rank
FROM `sql_advanced.orders`
ORDER BY customer_id, order_date;
Les deux éléments clés ici :
PARTITION BY customer_id — repart le compteur à 1 pour chaque client. Sans ça, tu numérotes toutes les lignes globalement.
ORDER BY order_date — détermine quel ordre est "le 1er". Logiquement : la date la plus ancienne = commande #1.

Pop question rapide : quelle est la différence entre ROW_NUMBER(), RANK(), et DENSE_RANK() ? Dans quel cas les résultats diffèrent-ils ?Row_number: compte le nombre de ligne en partitionant? Rank: ordonne en partitionant dans in ordre donné, dense rank: ordonne par rapport au nbre de fois où la valeur apparait?25 FebDémêlé trois fonctions de fenêtrage SQL distinctesDémêlé trois fonctions de fenêtrage SQL distinctesPas tout à fait — les trois font du ranking, la différence est dans la gestion des ex-aequo. Voici le modèle mental :
Imagine 3 coureurs qui finissent dans cet ordre : A(10s), B(10s), C(12s).
ROW_NUMBER() — attribue un numéro unique sans exception : 1, 2, 3. Pas de logique de classement, juste une numérotation arbitraire des ex-aequo.
RANK() — respecte les ex-aequo mais saute des rangs : 1, 1, 3. (il n'y a pas de 2e car deux personnes sont 1ères)
DENSE_RANK() — respecte les ex-aequo sans sauter de rangs : 1, 1, 2. Continu.

En pratique : si tu veux identifier "la 1ère commande par client" et qu'il ne peut pas y avoir deux commandes exactement à la même seconde, ROW_NUMBER() suffit. Si tu classes des clients par chiffre d'affaires et que les égalités ont du sens, DENSE_RANK() est plus propre.
Pop question : si tu filtrais sur WHERE order_rank = 1 après un ROW_NUMBER(), qu'est-ce que tu obtiendrais concrètement ?toutes les premiere socmmandes de clients25 FebExactement. C'est le pattern classique "first event per user" — très utilisé en analytics marketing (première commande, première session, première activation...).
La forme complète avec CTE :
sqlWITH ranked_orders AS (
  SELECT
    customer_id,
    order_id,
    order_date,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_rank
  FROM `sql_advanced.orders`
)
SELECT * FROM ranked_orders WHERE order_rank = 1;
Note : tu ne peux pas filtrer directement dans la même requête avec WHERE order_rank = 1 — les window functions sont calculées après le WHERE, donc il faut passer par une CTE ou sous-requête.
Tu continues sur les window functions aujourd'hui ou vous passez à autre chose ?# Ranking Customers by Sales Rank customers based on the total amount spent: Create a sales_rank column using a windows function, you should order your result by the sales_rank column to quickly verify your result.
SELECT
  customer_id,
  RANK() OVER(ORDER BY SUM(amount) DESC) sales_rank
FROM `sql_advanced.orders`
ORDER BY sales_rank;25 FebIdentified aggregate function nesting error in window function syntaxIdentified aggregate function nesting error in window function syntaxLe problème : tu ne peux pas utiliser SUM(amount) directement dans ORDER BY d'une window function — il faut d'abord agréger, puis ranker.
Fix avec CTE :
sqlWITH customer_sales AS (
  SELECT
    customer_id,
    SUM(amount) AS total_spent
  FROM `sql_advanced.orders`
  GROUP BY customer_id
)
SELECT
  customer_id,
  total_spent,
  RANK() OVER (ORDER BY total_spent DESC) AS sales_rank
FROM customer_sales
ORDER BY sales_rank;
Règle à retenir : les window functions et les agrégations (GROUP BY) ne peuvent pas vivre dans le même niveau de requête. L'ordre d'exécution SQL est : FROM → WHERE → GROUP BY → HAVING → SELECT (window functions) → ORDER BY. Les window functions arrivent après le GROUP BY, donc si tu veux les combiner, tu dois imbriquer via CTE.# Calculating Moving Average of Sales, Calculate a 7-day moving average of sales.
SELECT
  date_order,
  AVG(amount) OVER(ORDER BY order_date RANGE CURRENT ROW AND 1 FOLLOWING) moving_avg
FROM `sql_advanced.orders`
ORDER BY moving_avg;25 FebIdentified multiple SQL syntax and logic errors in queryIdentified multiple SQL syntax and logic errors in queryPlusieurs problèmes ici :
1. date_order n'existe pas — c'est order_date.
2. Syntaxe du frame incorrecte — il manque BETWEEN et la logique est inversée. Pour une moyenne glissante sur 7 jours passés :
sqlROWS BETWEEN 6 PRECEDING AND CURRENT ROW
3. ORDER BY moving_avg au lieu de order_date — une moyenne glissante se lit dans l'ordre chronologique, pas trié par valeur.
4. Probablement besoin d'agréger d'abord — s'il y a plusieurs commandes par jour, il faut sommer par date avant de calculer la moyenne glissante.
Fix complet :
sqlWITH daily_sales AS (
  SELECT
    order_date,
    SUM(amount) AS total_amount
  FROM `sql_advanced.orders`
  GROUP BY order_date
)
SELECT
  order_date,
  AVG(total_amount) OVER (
    ORDER BY order_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM daily_sales
ORDER BY order_date;

Notion clé — ROWS vs RANGE :
ROWS compte un nombre fixe de lignes physiques (6 lignes avant + la courante = 7).
RANGE opère sur des valeurs — si deux lignes ont la même date, elles sont traitées ensemble. Plus subtil, moins prévisible.
Pour les moyennes glissantes temporelles, ROWS est presque toujours le bon choix.
  SELECT
    customer_id,
    amount,
    order_id,
    order_date,
    RANK() OVER(PARTITION BY customer_id ORDER BY order_date ASC)  AS rank_asc,
    RANK() OVER(PARTITION BY customer_id ORDER BY order_date DESC)  AS rank_desc
  FROM `sql_advanced.orders`
  QUALIFY (rank_asc = 1 OR rank_desc = 1)Show more25 FebDiagnosed query logic flaw; recommended window functions insteadDiagnosed query logic flaw; recommended window functions insteadTa logique de ranking est bonne, mais l'expected result révèle que l'exercice ne demande pas de filtrer les lignes — il veut garder toutes les commandes de chaque client avec first_order_amount et last_order_amount comme colonnes répétées sur chaque ligne.
La bonne approche : FIRST_VALUE et LAST_VALUE :
sqlSELECT
  customer_id,
  order_date,
  amount,
  FIRST_VALUE(amount) OVER (
    PARTITION BY customer_id ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS first_order_amount,
  LAST_VALUE(amount) OVER (
    PARTITION BY customer_id ORDER BY order_date
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  ) AS last_order_amount
FROM `sql_advanced.orders`
ORDER BY customer_id, order_date;
Point crucial — le frame sur LAST_VALUE :
Par défaut, le frame d'une window function va de UNBOUNDED PRECEDING à CURRENT ROW. Donc sans le préciser, LAST_VALUE retourne juste la ligne courante, pas la dernière du groupe. Il faut explicitement étendre le frame jusqu'à UNBOUNDED FOLLOWING.
FIRST_VALUE n'a pas ce problème car la première ligne est toujours déjà dans le frame par défaut.
Pop question : pourquoi ton approche avec RANK + QUALIFY aurait pu produire plus de 2 lignes par client (comme customer_3 dans le résultat) ?Plusieurs amount le meme dernier jour?25 FebExactement. Si un client a 2 commandes le même jour et que c'est son dernier jour, RANK() = 1 s'applique aux deux lignes — donc tu gardes les deux avec QUALIFY, et last_order_amount serait ambigu.
C'est exactement pourquoi LAST_VALUE avec UNBOUNDED FOLLOWING est plus adapté ici : il prend mécaniquement la dernière ligne du frame sans ambiguïté de ranking.
Tu continues sur d'autres exos ou c'est bon pour les window functions ?Je vais passer à cela pour faire une pause sur les windows fonctions. ne me donne pas les reponses, j'essaie d'baord. 
[Optional] Advanced Challenges 🏋️‍♂️📚
To start the challenge with clean and more thorough data start by running 👉 THIS QUERY. You should have a slightly larger dataset
1. Join and Aggregate Queries 🔄🧮
1. Most Borrowed Author: Find the author whose books have been borrowed the most. Display the author's first name, last name, and the total number of times their books have been borrowed.
2. Borrowed Books by Genre: Find the number of books borrowed for each genre. Display the genre and the total number of books borrowed for each genre.
3. Books Borrowed by Year: Find the number of books borrowed each year. Display the year and the total number of books borrowed in that year.
2. Subqueries and Nested Queries 🧩🔍
1. Top 3 Most Borrowed Books: Find the top 3 most borrowed books. Display the book title and the total number of times it has been borrowed.
2. Authors with No Borrowed Books: Find authors whose books have never been borrowed. Display the author's first name and last name.
3. Books Borrowed by Multiple Borrowers: Find books that have been borrowed by more than one borrower. Display the book title and the number of distinct borrowers.Show more25 FebOrchestrated guidance framework sans direct solutionsOrchestrated guidance framework sans direct solutionsBonne initiative — apprendre en essayant d'abord, c'est le bon réflexe.
Quelques rappels mentaux avant de te lancer :
Pour la partie 1 (Join & Aggregate) — pense à identifier les tables impliquées avant d'écrire quoi que ce soit. Dessine mentalement les jointures : qui contient les emprunts ? qui contient les auteurs ? qui contient les genres ?
Pour la partie 2 (Subqueries) — "Top 3" = pense LIMIT. "Never borrowed" = pense NOT IN ou NOT EXISTS ou LEFT JOIN + IS NULL. "More than one" = pense HAVING.
Lance-toi, poste tes requêtes au fur et à mesure — je te dirai si la logique est bonne ou où ça coince, sans te donner la solution directement.#2. Subqueries and Nested Queries 🧩🔍
# Top 3 Most Borrowed Books:Find the top 3 most borrowed books. Display the book title and the total number of times it has been borrowed.
SELECT
  bk.bookid,
  bk.title,
  COUNt(DISTINCT br.borrowerid) nb_times_books_borrowed,
  RANK() OVER(ORDER BY nb_times_books_borrowed DESC) rank_books
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
ORDER BY nb_times_books_borrowed descShow more25 FebIdentified multiple SQL syntax errors requiring restructuringIdentified multiple SQL syntax errors requiring restructuringBonne structure générale, quelques problèmes à identifier — je te pose des questions plutôt que te les dire :
1. Tu veux le nombre de fois qu'un livre a été emprunté. COUNT(DISTINCT borrowerid) compte quoi exactement ? Est-ce bien ça que tu veux ?
2. Tu utilises bk.bookid et bk.title dans le SELECT avec une window function et un COUNT — il manque quelque chose pour que BigQuery sache comment regrouper. Qu'est-ce qui manque ?
3. Tu références nb_times_books_borrowed dans RANK() OVER(...) — est-ce que BigQuery peut utiliser un alias défini dans le même SELECT ?
4. "Top 3" — tu as le ranking, mais comment tu filtres sur les 3 premiers ?
Corrige ces points et reposte — tu es proche.Super la démarche de commencer par me donner des hints en me posant des questions. le nbre de fois où un livre a été emprumpter non?Group by
Mais puis enchainer avec le rank ou dois je faire une CTE?non je ne pense pas.QUALIFY?25 Feb2 / 2Clarified SQL distinctions et validé approches de requêteClarified SQL distinctions et validé approches de requêteBonnes réflexions, quelques précisions :
1. Pas tout à fait — COUNT(DISTINCT borrowerid) compte le nombre d'emprunteurs uniques. Si le même emprunteur prend le même livre 3 fois, ça compte pour 1. Pour le nombre de fois emprunté, que faut-il compter à la place ?
2. Exactement — GROUP BY d'abord, puis CTE pour le RANK. Tu ne peux pas faire les deux dans le même niveau.
3. Correct — il faut répéter l'expression ou passer par une CTE.
4. Oui, QUALIFY fonctionne. Attention : RANK peut donner ex-aequo (1,1,3). Si tu veux exactement 3 lignes quoi qu'il arrive, quelle fonction utiliserais-tu à la place ?
Réessaie avec ces éléments en tête.WITH books_borrowed AS
(
SELECT
  bk.bookid,
  bk.title,
  COUNt(DISTINCT br.borrowerid || br.borrowedbookid) nb_times_books_borrowed
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
GROUP BY 1, 2
ORDER BY nb_times_books_borrowed desc
)

SELECT
  bookid,
  title,
  nb_times_books_borrowed,
  RANK() OVER(ORDER BY nb_times_books_borrowed DESC) rank_books
FROM books_borrowedShow more25 FebIdentified flawed counting logic and missing filtering requirementIdentified flawed counting logic and missing filtering requirementBonne progression — la structure CTE + RANK est correcte. Deux points :
1. Le COUNT — COUNT(DISTINCT borrowerid || borrowedbookid) est une astuce fragile. La concaténation peut créer des collisions (ex: borrowerid=12, bookid=3 → "123" = borrowerid=1, bookid=23).
Mais surtout : si la table borrowers a une ligne par événement d'emprunt, qu'est-ce que tu as besoin de compter réellement ? Pas besoin de DISTINCT ni de concaténation.
2. Le filtre Top 3 — ta requête retourne encore tous les livres. Comment tu filtres ?Voici la table BORROWER:Field nameTypeModeDescriptionKeyCollationDefault ValuePolicy Tags Data Policies
borrowerid
STRINGREQUIRED
-
---
-
-
firstname
STRINGNULLABLE
-
---
-
-
lastname
STRINGNULLABLE
-
---
-
-
borrowedbookid
STRINGNULLABLE
-
---
-
-
borrowdate
DATENULLABLE
-
---
-
-
returndate
DATENULLABLE
-25 FebAnalyzed table structure to determine borrow frequency counting methodAnalyzed table structure to determine borrow frequency counting methodLa table a une ligne par événement d'emprunt — donc COUNT(*) suffit. Chaque ligne = un emprunt.
COUNT(DISTINCT ...) était une sur-complication inutile ici.
Pour le filtre Top 3, tu avais la bonne idée — comment tu l'appliques ?Quand utiliser distinct ou pas?25 FebDistilled straightforward guidance on DISTINCT usageDistilled straightforward guidance on DISTINCT usageRègle simple :
COUNT(*) — compte les lignes. Utilise-le quand chaque ligne = un événement distinct (comme ici, un emprunt).
COUNT(DISTINCT col) — élimine les doublons dans une colonne. Utilise-le quand tu veux compter des entités uniques, pas des événements. Exemple : "combien de clients distincts ont commandé ?" ou "combien de livres différents ont été empruntés ?"
Le bon réflexe : pose-toi la question "est-ce que je peux avoir le même id plusieurs fois dans mes résultats, et est-ce que je veux le compter une seule fois ou à chaque fois ?"
Maintenant — finalise ta requête avec COUNT(*) et le filtre Top 3.#Authors with No Borrowed Books: Find authors whose books have never been borrowed. Display the author's first name and last name.
SELECT

  a.authorid,
  a.firstname,
  a.lastname,
  COUNt(DISTINCT br.borrowerid || br.borrowedbookid) nb_times_books_borrowed
FROM `library.books` bk
LEFT JOIN `library.authors` a ON a.authorid = bk.authorid
FULL OUTER JOIN `library.borrowers` br ON bk.bookid = br.borrowedbookid
GROUP BY a.authorid, a.firstname, a.lastname
HAVING nb_times_books_borrowed < 1;Show more25 FebIdentified join strategy flaws and flagged concatenation syntax issuesIdentified join strategy flaws and flagged concatenation syntax issuesBonne intuition d'utiliser un HAVING pour filtrer, mais quelques points à réfléchir :
1. Tu retrouves le COUNT(DISTINCT borrowerid || borrowedbookid) — qu'est-ce qu'on vient de dire sur ce pattern ? Est-ce que tu en as besoin ici ?
2. Le FULL OUTER JOIN — tu veux les auteurs dont aucun livre n'a été emprunté. Est-ce que tu as besoin de garder les lignes des deux côtés ? Quel type de JOIN est fait pour "je veux les lignes de gauche même sans correspondance à droite" ?
3. Il existe un pattern plus simple et plus lisible pour "jamais emprunté" qui évite même le HAVING. Une idée ?Yes c'est ce que javais mis au début, mais pas de resultat donc j'ai tenté d'autres choseS.25 FebDiagnostiqué problème de jointure SQL et proposé solution alternativeDiagnostiqué problème de jointure SQL et proposé solution alternativeOk — alors le problème n'est pas le type de JOIN mais ailleurs. Revenons au LEFT JOIN.
Avec un LEFT JOIN books → borrowers, les livres jamais empruntés auront NULL dans toutes les colonnes de borrowers.
Plutôt que HAVING avec un COUNT, il y a un pattern plus direct : si br.borrowedbookid IS NULL après un LEFT JOIN, qu'est-ce que ça signifie ? Et où tu mets ce filtre ?Que le Book n'a jamis ete emprumpté - donc on peut filtrer avec un where sans faire le count!25 FebExactement. C'est le pattern anti-join — bien plus lisible et performant que HAVING COUNT < 1.
Réécris la requête avec cette logique.Check ces exos et dis moi si tu vois des erreurs?#1. Join and Aggregate Queries 🔄🧮
#Most Borrowed Author: Find the author whose books have been borrowed the most. Display the author's first name, last name, and the total number of times their books have been borrowed.
SELECT
  a.authorid,
  a.firstname,
  a.lastname,
  COUNt(DISTINCT br.borrowerid || br.borrowedbookid) nb_times_books_borrowed
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
LEFT JOIN `library.authors` a ON a.authorid = bk.authorid
GROUP BY a.authorid, a.firstname, a.lastname
ORDER BY nb_times_books_borrowed desc
;


# Borrowed Books by Genre: Find the number of books borrowed for each genre. Display the genre and the total number of books borrowed for each genre.
SELECT
  bk.genre,
  COUNt(DISTINCT br.borrowedbookid ) nb_books_borrowed
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
GROUP BY bk.genre
ORDER BY nb_books_borrowed desc;



# Books Borrowed by Year: Find the number of books borrowed each year. Display the year and the total number of books borrowed in that year.
SELECT
  EXTRACT(YEAR FROM br.borrowdate) year_date,
  COUNt(DISTINCT br.borrowedbookid ) nb_books_borrowed_yearly
FROM `library.borrowers` br
GROUP BY year_date
ORDER BY nb_books_borrowed_yearly desc;


#2. Subqueries and Nested Queries 🧩🔍
# Top 3 Most Borrowed Books:Find the top 3 most borrowed books. Display the book title and the total number of times it has been borrowed.
WITH books_borrowed AS
(
SELECT
  bk.bookid,
  bk.title,
  COUNt(1) nb_times_books_borrowed
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
GROUP BY 1, 2
ORDER BY nb_times_books_borrowed desc
)

SELECT
  bookid,
  title,
  nb_times_books_borrowed,
  DENSE_RANK() OVER(ORDER BY nb_times_books_borrowed DESC) rank_books
FROM books_borrowed
QUALIFY rank_books < 3


#Authors with No Borrowed Books: Find authors whose books have never been borrowed. Display the author's first name and last name.
SELECT
  a.authorid,
  a.firstname,
  a.lastname
FROM `library.books` bk
LEFT JOIN `library.authors` a ON a.authorid = bk.authorid
LEFT JOIN `library.borrowers` br ON bk.bookid = br.borrowedbookid
WHERE br.borrowedbookid IS NULL
GROUP BY a.authorid, a.firstname, a.lastname
;

# Books Borrowed by Multiple Borrowers: Find books that have been borrowed by more than one borrower. Display the book title and the number of distinct borrowers.
SELECT
  bk.bookid,
  bk.title,
  COUNt(DISTINCT br.borrowerid) nb_borrower_by_book
FROM `library.borrowers` br
LEFT JOIN `library.books` bk ON bk.bookid = br.borrowedbookid
GROUP BY 1, 2
HAVING nb_borrower_by_book > 1
ORDER BY nb_borrower_by_book descShow more25 FebIdentified six SQL queries avec quatre erreurs de syntaxe et logiqueIdentified six SQL queries avec quatre erreurs de syntaxe et logiqueBon travail global — logique solide sur la plupart. Quatre remarques :
Query 1 (Most Borrowed Author) — COUNT(DISTINCT borrowerid || borrowedbookid) — on en a parlé. Chaque ligne = un emprunt, donc COUNT(*) suffit.
Query 2 & 3 (Genre / Year) — même question : COUNT(DISTINCT borrowedbookid) compte les livres uniques empruntés, pas le nombre total d'emprunts. Si le même livre est emprunté 10 fois, ça compte 1. Est-ce bien ce que demande l'exercice ?
Query 4 (Top 3) — QUALIFY rank_books < 3 retourne les rangs 1 et 2 seulement. Pour inclure le rang 3, que faut-il changer ?
Query 5 (No Borrowed Books) — logique correcte, le GROUP BY est inutile ici (pas d'agrégation), mais ça ne casse rien.
Query 6 (Multiple Borrowers) — COUNT(DISTINCT borrowerid) est parfaitement justifié ici. C'est le bon usage de DISTINCT.Question 2&3: J'avais interpreté la question en unique book. Je pense que les 2 sont possibles vu que ce n'est pas precisé. Question 4: Superieur ou egale?25 FebQ2&3 — Oui, les deux interprétations sont défendables. En situation réelle, c'est exactement le genre d'ambiguïté à clarifier avec le métier avant d'écrire la requête. Bonne réflexion.
Q4 — Exactement, rank_books <= 3.Idem - check ces exos:# Aggregate Orders by Customer: Show the total amount spent by each customer on orders. Sort the result by most amount spend.
SELECT
  customer_id,
  SUM(amount) sum_amount
FROM `sql_advanced.orders`
GROUP BY customer_id
ORDER BY sum_amount DESC;

# Region-wise Customer Count: Count the number of customers in each region. Bonus : instead of displaying the region id, use the region name (you will need to JOIN some table 💪)
SELECT
  region_name,
  COUNT(DISTINCT customer_id) count_customers
FROM `sql_advanced.customers` c
LEFT JOIN `sql_advanced.regions` r
  ON r.region_id = c.region_id
GROUP BY region_name
ORDER BY count_customers DESC;

# Order Totals by Region: Calculate the total orders amount ($) for each region.
SELECT
  region_name,
  SUM(amount) sum_amount
FROM `sql_advanced.orders` o
LEFT JOIN `sql_advanced.customers` c
  ON o.customer_id = c.customer_id
LEFT JOIN `sql_advanced.regions` r
  ON r.region_id = c.region_id
GROUP BY region_name
ORDER BY sum_amount DESC;

# Monthly Sales:Compute the monthly sales revenue.There IS multiple possibility here, you can use EXTRACT OR FORMAT_DATE BY example.
SELECT
  FORMAT_DATE('%m-%y', order_date) mm_yy_date,
  FORMAT('%2f', SUM(amount)) sum_amount
FROM `sql_advanced.orders`
GROUP BY mm_yy_date
ORDER BY sum_amount DESC;

# Row Numbering Assign a unique sequential integer to rows within each customer's set of orders. Why ? It can be useful for marketing to know if this order is the first or the fifth.
SELECT
  customer_id,
  order_id,
  ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date) sequential_order_id
FROM `sql_advanced.orders`
ORDER BY customer_id, order_date;

# Ranking Customers by Sales Rank customers based on the total amount spent: Create a sales_rank column using a windows function, you should order your result by the sales_rank column to quickly verify your result.
WITH customer_sales AS (
  SELECT
    customer_id,
    SUM(amount) AS total_spent
  FROM `sql_advanced.orders`
  GROUP BY customer_id
)
SELECT
  customer_id,
  total_spent,
  RANK() OVER (ORDER BY total_spent DESC) AS sales_rank
FROM customer_sales
ORDER BY sales_rank;

# Calculating Moving Average of Sales, Calculate a 7-day moving average of sales.
SELECT
  order_date,
  AVG(amount) OVER(ORDER BY order_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) moving_avg
FROM `sql_advanced.orders`
ORDER BY order_date;


# Compare current sales with the previous and next day's sales, you should try to display the daily amount and current order_dateto verify your query.
WITH daily_sales AS (
  SELECT
    order_date,
    SUM(amount) AS daily_spent
  FROM `sql_advanced.orders`
  GROUP BY order_date
)
SELECT
  order_date,
  daily_spent,
  LAG(daily_spent) OVER (ORDER BY order_date ASC) AS daily_spent_before,
  LAG(daily_spent) OVER (ORDER BY order_date DESC) AS daily_spent_after,
  LEAD(daily_spent) OVER (ORDER BY order_date DESC) AS daily_spent_before,
  LEAD(daily_spent) OVER (ORDER BY order_date ASC) AS daily_spent_after
FROM daily_sales
ORDER BY order_date;


#Percentage of Total Sales - Calculate each order's percentage contribution to the total sales. Sort your result by decreasing amount

  SELECT
    order_id,
    (amount / SUM(amount) OVER() ) * 100 AS contrib
  FROM `sql_advanced.orders`
  ORDER BY contrib DESC;




# Cumulative Distribution - Calculate the cumulative distribution of sales over time.

WITH contrib_sales AS (
  SELECT
    order_id,
    order_date,
    (amount / SUM(amount) OVER() ) * 100 AS contrib
  FROM `sql_advanced.orders`
  ORDER BY contrib DESC
)
SELECT
  order_date,
  contrib,
  SUM(contrib) OVER (ORDER BY order_date) AS cum_contrib
FROM contrib_sales
ORDER BY order_date;


# First and Last Value Analysis Find the amount of the first and last order for each customer.

  SELECT
    customer_id,
    amount,
    order_id,
    order_date,
    RANK() OVER(PARTITION BY customer_id ORDER BY order_date ASC)  AS rank_asc,
    RANK() OVER(PARTITION BY customer_id ORDER BY order_date DESC)  AS rank_desc
  FROM `sql_advanced.orders`
  QUALIFY (rank_asc = 1 OR rank_desc = 1)Show more25 FebIdentified formatting errors and duplicate column issues across queriesIdentified formatting errors and duplicate column issues across queriesGlobalement très propre. Trois remarques :
Monthly Sales — deux problèmes. FORMAT('%2f', ...) devrait être FORMAT('%.2f', ...) (le point est obligatoire). Et surtout : ORDER BY sum_amount DESC trie par montant, pas par date — pour des ventes mensuelles, l'ordre chronologique est plus naturel. Et comme FORMAT retourne une string, le tri numérique ne fonctionnera pas correctement.
Compare previous/next — tu as deux colonnes nommées daily_spent_before et deux daily_spent_after. BigQuery va rejeter les alias dupliqués. Simplifie : LAG ASC = jour précédent, LEAD ASC = jour suivant. Les versions avec DESC sont redondantes.
First and Last Value — on en a parlé ce matin : l'expected result demande toutes les lignes avec les colonnes first_order_amount et last_order_amount. Ton approche RANK + QUALIFY filtre les lignes au lieu d'ajouter des colonnes. La solution reste FIRST_VALUE / LAST_VALUE avec UNBOUNDED FOLLOWING.
Tout le reste est correct et bien écrit. Belle progression sur la journée.

Débrief rapide — quels concepts te semblent bien acquis et lesquels sont encore un peu flous ?
