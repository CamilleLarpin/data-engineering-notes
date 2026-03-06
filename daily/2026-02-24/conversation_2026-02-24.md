
Artefact Data Engineering
/
How does this work?

# More elegant : you can use a dictionary mapping
time_switch = {
    'morning': 'What do you eat for your breakfast?',
    'noon': 'What do you eat for lunch?',
    'afternoon': 'What do you eat for tea time?',
    'evening': 'What do you eat for diner?'
}
print(time_switch.get(time, 'We can\'t treat your demand. Please enter a correct time.'))
24 Feb

Identified dictionary lookup pattern as elegant switch alternative
Identified dictionary lookup pattern as elegant switch alternative
🧠 Concept First: Why does this exist?
In many languages, there's a switch/case statement for branching logic. Python didn't have one until 3.10 (match/case). Before that, developers used dictionaries as lookup tables — a cleaner alternative to chaining if/elif/else.

How it works, line by line
python
time_switch = {
    'morning': 'What do you eat for your breakfast?',
    ...
}
A dict where keys = conditions, values = outcomes. Think of it as a pre-built decision table.

python
time_switch.get(time, 'fallback message')
.get(key, default) is the key move here — it:

Looks up time in the dict
Returns the matching value if found
Returns the default string if the key doesn't exist — no KeyError, no crash
Analogy
Think of it like a restaurant menu. You hand the waiter a time of day, they check the menu (dict), and hand back the right question. If you ask for "midnight," it's not on the menu — they politely say "we can't serve that."

vs. if/elif — the trade-off
if/elif	Dict lookup
Readability	Gets messy at 4+ branches	Clean and flat
Speed	O(n) — checks each condition	O(1) — direct hash lookup
Dynamic?	Hard to modify at runtime	Easy — just add a key
🎯 Pop Question
Without running it, what does this print?

python
d = {'a': 1, 'b': 2}
print(d.get('c', 99))
Take a guess before scrolling — it's the core mechanic of the whole pattern.

99

24 Feb
✅ Correct.

'c' isn't in the dict, so .get() returns the default: 99. No error, no drama.

One step further — what's the difference between these two?

python
d.get('c', 99)   # → ?
d['c']           # → ?
What do you think the second one does when 'c' doesn't exist?

More than cleaner, my instructor just pointed out it was interesting from perofrmance perspective. In the future, highlight these considerations (performance, scalability, costs etc) - or explain why it is cleaneR in this instance.

24 Feb

Acknowledged feedback to emphasize performance and scalability considerations
Acknowledged feedback to emphasize performance and scalability considerations
Got it — noted. I'll lead with performance/scalability trade-offs when they're relevant, not just readability.

To close the loop on why it's faster here:

Dict lookup = O(1) because Python dicts use a hash table — it computes a hash of the key and jumps directly to the value. No comparisons, no iteration.

if/elif = O(n) — Python evaluates each condition in order until one matches. With 4 branches it's negligible, but at 50+ branches (think routing tables, config maps, event dispatchers), the difference compounds.

Rule of thumb: When you have many discrete, known conditions → dict. When conditions involve ranges, logic, or complex expressions → if/elif.

Now, back to the open question — what do you think d['c'] does when 'c' doesn't exist?

Error?

24 Feb
Exactly — a KeyError. Python can't find the key and crashes rather than gracefully falling back.

This is the core reason .get() exists: safe lookup with a default, without try/except overhead.

python
d['c']           # → KeyError: 'c'  💥
d.get('c', 99)   # → 99             ✅
Fiche #1 — Dict as Switch / Safe Lookup

Dict lookup replaces if/elif chains when conditions are discrete and known. O(1) via hash table vs O(n) for if/elif. Use .get(key, default) for safe access — no KeyError, no try/except. Best for: routing, mappings, event dispatch, config tables.

Next time you see an if/elif chain in your code, ask yourself: "are these conditions discrete and static?" — if yes, a dict is likely better. Want to move to the next concept, or is there something else from today's session to unpack?

What is hash table?

24 Feb

Synthesized foundational hash table concepts for explanation
Synthesized foundational hash table concepts for explanation
Mental model first
A hash table is a data structure that trades memory for speed — it uses extra space to achieve O(1) lookups.

How it works
You give it a key (e.g. 'morning')
A hash function converts that key into a number (e.g. 'morning' → 4782)
That number maps to a slot in memory where the value lives
Retrieval = compute hash → jump to slot. One step, regardless of size.
'morning'  →  hash()  →  4782  →  memory[4782]  →  'What do you eat for breakfast?'
Analogy
Think of a library with a perfect index. Instead of scanning every shelf (O(n)), you look up the index, get an exact shelf number, and go directly there (O(1)).

Why it matters for you as a Data Engineer
Hash tables are everywhere in data engineering:

Python dicts
Database indexes
JOIN operations in SQL/Spark (hash joins)
Kafka partition keys
Deduplication logic
Understanding this one structure unlocks why these tools perform the way they do at scale.

🎯 Pop question: If two different keys produce the same hash number, what do you think happens? (This is called a hash collision — worth knowing.)

When you look for one of the key, you might find the content allocated to the other key?

Just to make sure I understood: hashing is leveraging a function that turns item into a number that is more easiliy retrievable? If yes, why is it more easily retrievable as a number?

24 Feb

Examined hash collision nuances and retrieval speed mechanics
Examined hash collision nuances and retrieval speed mechanics
On collisions — almost right
You'd risk getting the wrong value, yes. But Python handles this with collision resolution — when two keys land on the same slot, it stores both and adds a small comparison step to find the right one. So it degrades slightly but never silently returns the wrong value. Good instinct though.

On your second question — this is the sharp one
Yes on the definition. But why is a number more retrievable?

Because a number = a direct memory address.

Think of RAM as a long street with numbered houses. If I say "go to house 4782" — you go directly. If I give you a name like 'morning' — the computer has no idea where that lives without searching.

Hashing converts an unpredictable key → a predictable address. That's the whole trick.

'morning'  →  hash()  →  4782  →  RAM[4782]  ✅ direct jump
Without hashing, the computer would scan every slot asking "is this 'morning'?" — that's your O(n) scenario.

The core insight:

Computers are extremely fast at accessing memory by position. Hashing is just a way to turn anything into a position.

🎯 Pop question: Given this, why do you think only immutable types (strings, integers, tuples) can be dict keys in Python — but not lists?

Because a dictionay key is immutable? I know the value is. 

Taking your example: 'morning' → hash() → 4782 → RAM[4782] ✅ direct jump
How does the computer know that to look for 'morning' it then needs to go to 4782?

24 Feb

Untangled dictionary hashing mechanics and clarified lookup process
Untangled dictionary hashing mechanics and clarified lookup process
Your first point — you're close but circular
"A dict key is immutable" describes what it is, not why. The real reason:

If the key could change after insertion, its hash would change → it would point to a different address → Python could never find it again. The value would be stranded in memory with no way back.

List is mutable → its hash could change → unreliable as an address → Python forbids it.

Your second question — this is exactly the right thing to ask
The computer doesn't store a map of 'morning' → 4782. That would just be another lookup problem.

Instead: it recomputes the hash every time.

# Storing:
hash('morning') → 4782 → write value to RAM[4782]

# Retrieving later:
hash('morning') → 4782 → read RAM[4782]
The hash function is deterministic — same input always produces same output. So retrieval is just: run the same function again, land on the same address.

No map needed. No search needed. Just math.

The core insight:

A hash function is a consistent translator. The address is re-derived on demand, not stored.

🎯 Pop question: Given this, what would break if a hash function returned a different number for the same key on different runs?

You would not be able to find the key again. 

Could you confirm that you can' t have the same outputs with different inputs in a hash function?

24 Feb
✅ Exactly right on the first part.

On your question — actually, you can get the same output from different inputs
That's precisely what a collision is. hash('morning') and hash('xyz') could both return 4782.

Hash functions don't guarantee uniqueness — they guarantee consistency (same input → same output, always).

This is unavoidable mathematically: you're mapping an infinite set of possible inputs to a finite set of addresses. Collisions are guaranteed to exist.

So the two properties that actually matter:

Property	Meaning
Deterministic	Same input → same output, always
Uniform distribution	Spreads outputs evenly to minimize collisions
Uniqueness would be ideal but is impossible. Good hash functions just make collisions rare.

Fiche #2 — Hash Tables

A hash function converts a key → memory address (deterministically). Retrieval = recompute the hash → jump directly to address. O(1). Keys must be immutable — if they changed, their hash would change and the value would be unlocatable. Collisions (two keys → same address) are inevitable but handled internally by Python.

🎯 You've now built a solid mental model of one of CS's most fundamental structures. Ready for the next concept, or anything to clarify?

How do you create a dataset and upload csv/json files in it in bigquery?

24 Feb

Synthesized pedagogical framework for BigQuery dataset creation
Synthesized pedagogical framework for BigQuery dataset creation
Concept first — BigQuery's data hierarchy
Before the how, the mental model:

Project  →  Dataset  →  Table
(like a server) (like a schema/database) (like a table)
A dataset is just a container for tables — it also defines location (where data physically lives, e.g. EU, US), which matters for latency and compliance costs.

Creating a dataset + uploading files
3 ways — worth knowing the trade-offs:

Method	Best for
BigQuery UI (Console)	Quick, manual, learning
bq CLI	Scripting, automation
Python client (google-cloud-bigquery)	Pipelines, programmatic control
Via UI (fastest to learn on):

Go to BigQuery Console → click your project → Create Dataset
Set dataset ID, region, expiration
Inside the dataset → Create Table → Source: Upload → select CSV/JSON
Define schema manually or use auto-detect
Via Python (what you'll use in production):

python
from google.cloud import bigquery

client = bigquery.Client()

# Create dataset
dataset = bigquery.Dataset("your_project.your_dataset")
dataset.location = "EU"
client.create_dataset(dataset)

# Upload CSV
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True,  # infers schema
)
with open("file.csv", "rb") as f:
    client.load_table_from_file(f, "your_project.your_dataset.your_table", job_config=job_config)
Two things to think about
autodetect=True is convenient but risky in production — it can miscast types (e.g. "01" as integer, dropping the leading zero). In real pipelines you define the schema explicitly.

Region matters — once set on a dataset, you can't change it. Cross-region queries cost more and are slower.

🎯 Quick question: Are you doing this via the UI or Python in your bootcamp? That'll shape what to go deeper on.

Are you doing this via the UI or Python in your bootcamp? That'll shape what to go deeper on.
Does not say. There are 4 tables. Python seems quicker is it not? 
Do I need to run it in terminal? from which folder?

24 Feb

Weighed Python efficiency and clarified execution logistics
Weighed Python efficiency and clarified execution logistics
Python quicker? — depends
UI	Python
One-off upload	✅ faster	Overkill
4 tables, repeatable	Tedious	✅ faster
Production pipeline	❌	✅
Since you have 4 tables and are in a Data Engineering context — Python is the right call. You'd loop over files rather than clicking 4 times, and you're building a transferable skill.

Terminal — yes, and folder matters
Run it from wherever your CSV/JSON files are, or specify absolute paths in the script. Simplest approach:

project/
├── data/
│   ├── table1.csv
│   ├── table2.csv
├── upload.py   ← run from here
bash
cd path/to/project
python upload.py
If your files are in a subfolder:

python
open("data/table1.csv", "rb")  # relative path from where you run
Before running — two prerequisites
bash
pip install google-cloud-bigquery
And authentication:

bash
gcloud auth application-default login
This tells Python which Google account to use. If you haven't set up gcloud CLI yet, that's the first step.

🎯 Have you already set up a GCP project and have your credentials configured, or is that still to do?


GCP VM Setup for Data Engineering In this guide, we will walk you through the steps to set up a Google Cloud Platform (GCP) virtual machine (VM) for the Data Engineering Curriculum. SSH Key Generation 🔑 To securely connect with your virtual machine, we’ll use the SSH protocol. This requires genera

pasted

I have a VM - that I installed following this guide - memorise whatever you think is relevant from it. 

How do I pass the downloaded files on my computer to the VM?

24 Feb

Catalogued VM setup details to address file transfer question
Catalogued VM setup details to address file transfer question
3 options — pick based on your use case
Option 1 — scp (simplest, one-off)

bash
# From your LOCAL terminal:
scp -i ~/.ssh/id_rsa /path/to/file.csv <username>@<external_ip>:~/destination/
For a whole folder:

bash
scp -i ~/.ssh/id_rsa -r /path/to/folder/ <username>@<external_ip>:~/
Option 2 — VS Code drag & drop (since you have Remote SSH) Just open the Remote SSH Explorer in VS Code → drag files from your local Finder/Explorer into the VS Code file tree. Simplest for a few files.

Option 3 — Google Cloud Storage bucket (best for large files/pipelines) Upload to GCS first, then pull to VM:

bash
gsutil cp gs://your-bucket/file.csv ~/destination/
This is the production pattern you'll use in Data Engineering — VM ↔ GCS rather than local ↔ VM.

For your 4 CSV/JSON files right now — Option 2 (drag & drop in VS Code) is fastest. Option 1 (scp) if you prefer terminal.

Which files are these exactly — the ones you want to load into BigQuery?

yes

24 Feb

Architected comprehensive BigQuery data loading workflow
Architected comprehensive BigQuery data loading workflow
Then the cleanest end-to-end workflow for you:

Step 1 — Transfer files to VM Drag & drop into VS Code (Remote SSH), into a folder like ~/data/

Step 2 — Activate your environment

bash
pyenv activate Artefact
pip install google-cloud-bigquery
Step 3 — Upload all 4 files in one script

python
from google.cloud import bigquery

client = bigquery.Client(project="your-project-id")

# Create dataset once
dataset = bigquery.Dataset("your-project-id.your_dataset")
dataset.location = "EU"
client.create_dataset(dataset, exists_ok=True)

files = {
    "table1": "~/data/file1.csv",
    "table2": "~/data/file2.csv",
    "table3": "~/data/file3.json",
    "table4": "~/data/file4.csv",
}

job_config = bigquery.LoadJobConfig(autodetect=True)

for table_name, filepath in files.items():
    job_config.source_format = (
        bigquery.SourceFormat.NEWLINE_DELIMITED_JSON 
        if filepath.endswith(".json") 
        else bigquery.SourceFormat.CSV
    )
    with open(filepath, "rb") as f:
        job = client.load_table_from_file(
            f, f"your-project-id.your_dataset.{table_name}", job_config=job_config
        )
    job.result()  # waits for completion
    print(f"Loaded {table_name} ✅")
Step 4 — Run it

bash
cd ~/data
python upload.py
Two things to replace before running: your-project-id (find it in GCP Console) and the actual filenames. What are your 4 files called?

pyenv activate Artefact >> it is already activate when I start a terminal... Was it not part of the setup?

Also, I have this error:                                                                                                            [🐍 Artefact]
➜  data git:(main) ✗ python upload.py                                                                                                                                                                                           [🐍 Artefact]
Traceback (most recent call last):
  File "/home/camille.larpin/code/CamilleLarpin/student-challenges-de/curriculum/00-Basics/04-SQL/data/upload.py", line 8, in <module>
    client.create_dataset(dataset, exists_ok=True)
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/cloud/bigquery/client.py", line 711, in create_dataset
    api_response = self._call_api(
                   ^^^^^^^^^^^^^^^
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/cloud/bigquery/client.py", line 861, in _call_api
    return call()
           ^^^^^^
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 294, in retry_wrapped_func
    return retry_target(
           ^^^^^^^^^^^^^
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 156, in retry_target
    next_sleep = _retry_error_helper(
                 ^^^^^^^^^^^^^^^^^^^^
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/api_core/retry/retry_base.py", line 214, in _retry_error_helper
    raise final_exc from source_exc
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/api_core/retry/retry_unary.py", line 147, in retry_target
    result = target()
             ^^^^^^^^
  File "/home/camille.larpin/.pyenv/versions/Artefact/lib/python3.11/site-packages/google/cloud/_http/__init__.py", line 494, in api_request
    raise exceptions.from_http_response(response)
google.api_core.exceptions.Forbidden: 403 POST https://bigquery.googleapis.com/bigquery/v2/projects/arboreal-blend-488313-m6/datasets?prettyPrint=false: Request had insufficient authentication scopes. [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'ACCESS_TOKEN_SCOPE_INSUFFICIENT', 'domain': 'googleapis.com', 'metadata': {'method': 'google.cloud.bigquery.v2.DatasetService.InsertDataset', 'service': 'bigquery.googleapis.com'}}]

Show more
24 Feb

Identified authentication scope mismatch requiring credential reconfiguration
Identified authentication scope mismatch requiring credential reconfiguration
You're right — pyenv global Artefact was set in the guide, so it auto-activates. My mistake.

The error — authentication scope issue
gcloud auth login (which you ran during setup) authenticates you for the gcloud CLI. But the Python BigQuery client needs a separate credential set.

Fix:

bash
gcloud auth application-default login
This will open a browser, ask you to log in, and grant broader scopes including BigQuery. It's a one-time step.

Then re-run your script.

Why two different auth commands?

gcloud auth login → for you, using the terminal gcloud auth application-default login → for applications (Python scripts) running on your behalf

Think of it as: one badge for you to walk in the building, another badge for your robot assistant to access the filing cabinet.

You are running on a Google Compute Engine virtual machine.
The service credentials associated with this virtual machine
will automatically be used by Application Default
Credentials, so it is not necessary to use this command.
If you decide to proceed anyway, your user credentials may be visible
to others with access to this virtual machine. Are you sure you want
to authenticate with your personal account?
Do you want to continue (Y/n)?  

Also, Like Artefact is activated by default, is it possible to go quickly to a folder (even put it by default) in order to avoid typing all the path ?

24 Feb

Weighed authentication approach and devised folder navigation shortcuts
Weighed authentication approach and devised folder navigation shortcuts
Auth prompt — type Y
The warning is saying: "the VM has its own service account, use that instead." But that service account likely doesn't have BigQuery permissions set up. For a personal learning VM, using your personal credentials is fine — type Y.

In production you'd configure the service account properly, but that's not worth the detour now.

Quick navigation — two options
Option 1 — alias (quick jump from anywhere)

Add to your ~/.zshrc:

bash
alias myproject="cd ~/code/CamilleLarpin/student-challenges-de/curriculum/00-Basics/04-SQL/data"
Then:

bash
source ~/.zshrc  # reload once
myproject        # jumps there instantly
Option 2 — default start directory in VS Code

In VS Code settings, set terminal.integrated.cwd to your project folder — every new terminal opens there.

For now, Option 1 is fastest. You'll also want to update the alias as you move through curriculum modules (SQL → next phase etc).

Try the Y on the auth first — does the script run after?

I love option 1!
What are alias and source ~/.zshrc working?

24 Feb

Prepared explanation of aliases and shell configuration sourcing
Prepared explanation of aliases and shell configuration sourcing
Alias
An alias is just a shortcut — a custom command name that maps to a longer command.

bash
alias myproject="cd ~/code/CamilleLarpin/..."
When you type myproject, the shell silently replaces it with the full command. That's it.

You can alias anything:

bash
alias ll="ls -la"        # detailed file list
alias ..="cd .."         # go up one folder
alias gst="git status"   # common shortcut
~/.zshrc
This is a config file that Zsh runs every time you open a terminal. It's where you store anything you want available in every session — aliases, environment variables, path settings.

Think of it as: "instructions Zsh reads before handing the terminal to you."

source ~/.zshrc
Normally, changes to ~/.zshrc only take effect when you open a new terminal (because that's when Zsh reads it).

source forces Zsh to re-read and apply the file immediately, without restarting.

bash
# Edit the file → save → apply without restarting:
source ~/.zshrc
🎯 Pop question: If you add an alias to ~/.zshrc but don't run source ~/.zshrc, when will it become available?

➜  data git:(main) ✗ python upload.py                                                                                                                                                                       [🐍 Artefact][🐍 Artefact]
Traceback (most recent call last):
  File "/home/camille.larpin/code/CamilleLarpin/student-challenges-de/curriculum/00-Basics/04-SQL/data/upload.py", line 25, in <module>
    with open(filepath, "rb") as f:
         ^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '~/data/items.csv'
➜  data git:(main) ✗ tree                                                                                                                                                                                   [🐍 Artefact][🐍 Artefact]
.
├── items.csv
├── stores.csv
├── transactions.json
├── upload.py
└── vendors.csv
1 directory, 5 files
➜  data git:(main) ✗

Show more
24 Feb

Diagnosed path resolution issue requiring relative file references
Diagnosed path resolution issue requiring relative file references
Simple fix — Python's open() doesn't expand ~ like the shell does. Use relative paths since you're already running from the data folder:

python
files = {
    "items": "items.csv",
    "stores": "stores.csv",
    "vendors": "vendors.csv",
    "transactions": "transactions.json",
}
Just filenames, no path needed. Run it again.

Why can't I see in the left column the data set iowa_liquor?

24 Feb

Investigated missing dataset visibility and identified diagnostic questions
Investigated missing dataset visibility and identified diagnostic questions
A few possible reasons — let's narrow it down quickly:

Did the script finish with all 4 ✅ messages, or did it error out?

And in the BigQuery console, which project is selected in the left panel — does it show arboreal-blend-488313-m6?

1771943419563_image.png
24 Feb

Identified dataset availability and navigation solution
Identified dataset availability and navigation solution
It's there — look at the breadcrumb at the top: arboreal-blend-488313-m6 / Datasets / iowa_liquor_sales. All 4 tables loaded successfully. 🎉

In the left panel, just click on Datasets under your project to expand it — the Explorer tree is collapsed. You'll see iowa_liquor_sales appear there too.

I was used to see it in the let pannel, clicking on arrow down and it would expand into dataset and tables. But it is not working as such now.

24 Feb

Diagnosed expansion issue with project node in explorer panel
Diagnosed expansion issue with project node in explorer panel
In the screenshot I can see arboreal-blend-488313-m6 in the left panel with a dropdown arrow — but the dataset isn't showing under it, only "Datasets", "Connections" etc. (those are menu items, not your actual datasets).

Try this: click the small arrow/triangle right next to arboreal-blend-488313-m6 to expand the project tree. If the dataset still doesn't appear, click the search bar in the Explorer and type iowa — it should surface it directly.

If neither works, it may just be a UI refresh issue — hit Ctrl+Shift+R to hard refresh the page.

How to extract month from date in Bigquery?
concretly get MM-YY from YYYY-MM-DD

24 Feb

Recognized straightforward BigQuery date extraction task
Recognized straightforward BigQuery date extraction task
sql
FORMAT_DATE('%m-%y', date_column)
Example:

sql
SELECT FORMAT_DATE('%m-%y', '2023-07-15')
-- → '07-23'
FORMAT_DATE lets you build any string representation from a date using format codes. The key ones worth knowing:

%Y → 2023 | %y → 23 | %m → 07 | %d → 15 | %B → July

🎯 Quick one: if you wanted Jul-2023 instead, how would you write the format string?

%b-%Y

24 Feb
✅ Exactly.

%b gives the abbreviated month name — Jul, Aug etc. Good instinct to distinguish %b (abbreviated) vs %B (full name).

Ready to move on or is there more SQL to work through?

How do I filter on date in BQ?

24 Feb

Identified straightforward BigQuery date filtering question
Identified straightforward BigQuery date filtering question
Depends on what you want to filter on:

Exact date:

sql
WHERE date_column = '2023-07-15'
Date range:

sql
WHERE date_column BETWEEN '2023-01-01' AND '2023-12-31'
By month/year:

sql
WHERE FORMAT_DATE('%m-%y', date_column) = '07-23'
-- or more efficiently:
WHERE EXTRACT(YEAR FROM date_column) = 2023
AND EXTRACT(MONTH FROM date_column) = 7
Performance note: EXTRACT and FORMAT_DATE on large tables force a full scan — they can't use partition pruning. If your table is partitioned by date (common in Data Engineering), filtering like this is more efficient:

sql
WHERE date_column >= '2023-07-01' AND date_column < '2023-08-01'
Direct date comparisons let BigQuery skip entire partitions it doesn't need — much cheaper at scale.

🎯 Do you know what table partitioning is, or worth a quick explanation?

Comment formater un somme pour avoir suelement 2 decimales, avec un signe de dollard, truncker?

24 Feb

Décortiqué la question sur le formatage BigQuery en français
Décortiqué la question sur le formatage BigQuery en français
sql
SELECT FORMAT('$%.2f', TRUNC(SUM(amount), 2))
Exemple:

sql
SELECT FORMAT('$%.2f', TRUNC(SUM(sale_dollars), 2))
-- → '$1234.56'
Les 3 pièces:

TRUNC(x, 2) → coupe à 2 décimales sans arrondir (ex: 1.999 → 1.99) FORMAT('$%.2f', x) → formate en string avec $ et 2 décimales %.2f → format standard : f = float, .2 = 2 décimales

Note: FORMAT() retourne une string, pas un nombre — donc pas utilisable pour des calculs ensuite. Si tu as besoin de continuer à calculer, utilise ROUND à la place de FORMAT:

sql
ROUND(SUM(amount), 2)  -- reste numérique
🎯 Quelle est la différence entre TRUNC(1.999, 2) et ROUND(1.999, 2) ?

1.99 VS 2.00

Il y a. t il une fonction BQ built in pour extraire les saisons de la date?

24 Feb
✅ Exactement.

Saisons — pas de fonction native dans BigQuery
Il faut la construire, typiquement avec un CASE:

sql
CASE 
  WHEN EXTRACT(MONTH FROM date_column) IN (12, 1, 2)  THEN 'Winter'
  WHEN EXTRACT(MONTH FROM date_column) IN (3, 4, 5)   THEN 'Spring'
  WHEN EXTRACT(MONTH FROM date_column) IN (6, 7, 8)   THEN 'Summer'
  WHEN EXTRACT(MONTH FROM date_column) IN (9, 10, 11) THEN 'Fall'
END AS season
Pourquoi BQ n'a pas cette fonction? Les saisons sont hémisphère-dépendantes — Décembre est l'été en Australie. Impossible de standardiser sans contexte.

🎯 Pop question: CASE WHEN en SQL — c'est l'équivalent de quoi en Python, qu'on a vu récemment?

if XX: elif: else:

24 Feb
✅ Exactement — ou encore plus précisément, le dict as switch qu'on a vu, puisque CASE WHEN mappe des valeurs discrètes à des résultats.

Fiche #3 — Dates dans BigQuery

FORMAT_DATE('%m-%y', col) → string formatée depuis une date EXTRACT(MONTH/YEAR FROM col) → extrait un composant numérique TRUNC(x, 2) → coupe sans arrondir | ROUND(x, 2) → arrondit FORMAT('$%.2f', x) → formate en string avec symbole et décimales Filtrer par range direct (>=, <) est plus performant qu'EXTRACT sur grandes tables (partition pruning) Saisons → pas de fonction native, utiliser CASE WHEN

je souhaite créer un dossier github de markdown files où je vais mettre les cours, mes notes et où tu pourras generer des pop up quiz, résumé etc. 
Comment je commence? je créer un dosier en local puis dans le terminal dans le dossier je mets git init?

25 Feb

Évalué l'approche optimale pour initialiser le dépôt GitHub
Évalué l'approche optimale pour initialiser le dépôt GitHub
Bonne idée — mais depuis ton VM tu as gh CLI, donc plus rapide de créer directement sur GitHub et cloner :

bash
gh repo create data-engineering-notes --public --clone
cd data-engineering-notes
```

Ça fait tout en une commande : crée le repo sur GitHub + clone en local.

---

**`git init` c'est pour quand?**
Quand tu pars d'un dossier existant sans repo GitHub. Ici tu pars de zéro — `gh repo create` est plus propre.

---

**Structure suggérée:**
```
data-engineering-notes/
├── 00-Python/
│   ├── hash-tables.md
│   └── dict-as-switch.md
├── 01-SQL/
│   ├── dates-bigquery.md
│   └── quizzes.md
├── fiches/
└── README.md
Une fois créé, je peux générer les fiches et quizzes directement en markdown que tu pousses dedans. Tu veux commencer par ça?

Donc je fais "gh repo create data-engineering-notes --public --clone cd data-engineering-notes" dans ma VM n'est ce pas?
Comment puis je acceder à ma VM via terminal?

25 Feb
Oui, dans ta VM.

Pour accéder à ta VM via terminal:

bash
ssh -i ~/.ssh/id_rsa <username>@<external_ip>
Ton username est camille.larpin (vu dans le traceback plus tôt). L'IP externe se trouve dans GCP Console → Compute Engine → VM Instances.

Conseil: crée un alias dans ton ~/.zshrc local (sur ton Mac/PC, pas la VM) :

bash
alias myvm="ssh -i ~/.ssh/id_rsa camille.larpin@<external_ip>"
Ensuite tu tapes juste myvm pour te connecter.

Attention: l'IP externe change à chaque redémarrage de la VM sauf si tu as une IP statique réservée. Si ça ne connecte pas, vérifie d'abord l'IP dans GCP Console.

Tu as l'IP sous la main ?

pourquoi ma VM et pas sur mon ordi?

25 Feb
Bonne question — tu peux le faire sur ton ordi local. Mais voici pourquoi la VM est préférable dans ton contexte:

VM:

Tout est déjà configuré : gh, gcloud, Python, pyenv
Même environnement que le reste de ton bootcamp
Tes fichiers de données sont déjà là
Pas de risque de conflits avec ton environnement local
Ordi local:

Tu devrais réinstaller gh, configurer Git, etc.
Environnement différent → risque de divergence
En Data Engineering, le principe est d'avoir un environnement unique et reproductible — c'est exactement ce que ta VM représente. Travailler en local en parallèle crée deux sources de vérité, ce qui complique les choses.

Conclusion: reste sur la VM via VS Code Remote SSH — tu l'as déjà ouverte, c'est le terminal intégré VS Code qui te connecte directement. Pas besoin d'ouvrir un terminal séparé.

OK. Mais le but de ce dossier est purement pedagogique - je ne pense pas faire des exercices dessus car ai deja un dossier student chanllenge. 
De plus à la fin du bootcamp la VM sera suprimée alors que le dossier doit rester et me permettre de revenir sur mes notes si besoin.

25 Feb
Excellent raisonnement — dans ce cas ton ordi local est le bon endroit.

Notes de cours = documentation personnelle, pas du code lié à l'infra du bootcamp. Ça doit survivre à la VM.

Sur ton ordi local donc:

bash
gh repo create data-engineering-notes --public --clone
cd data-engineering-notes
Mais d'abord vérifie que gh est installé localement:

bash
gh --version
Si ce n'est pas le cas:

Mac: brew install gh
Windows: cli.github.com
Tu es sur Mac ou Windows?

camillelarpin ~ % gh repo create data-engineering-notes --public --clone
cd data-engineering-notes
HTTP 401: Requires authentication (https://api.github.com/graphql)
Try authenticating with:  gh auth login
cd: no such file or directory: data-engineering-notes
camillelarpin ~ %

25 Feb
gh n'est pas authentifié sur ton ordi local. Lance:

bash
gh auth login
Choisis:

GitHub.com
SSH
Login with a web browser
Une fois authentifié, relance les deux commandes séparément:

bash
gh repo create data-engineering-notes --public --clone
cd data-engineering-notes
(C'était deux commandes séparées — le cd ne faisait pas partie de gh repo create.)

Title for ssh key?

25 Feb
Mets ce que tu veux, c'est juste un label pour identifier la clé dans GitHub. Par exemple:

MacBook-Camille

PArfait! 
Pour la structure, ej ne suis pas convaincu. Prenons un step en arrière. Reprends mes objectifs et pose moi des questions si besoin.

25 Feb
Tes objectifs tels que je les comprends:

Garder des notes du bootcamp (cours + tes propres annotations)
Pouvoir réviser après la fin du bootcamp
Que je puisse générer des fiches, quizzes, résumés dedans
Quelques questions pour affiner la structure:

Tu veux organiser par thème (Python, SQL, BigQuery...) ou par semaine/jour de bootcamp?
Tu veux un endroit séparé pour les fiches de révision vs tes notes brutes, ou tout mélangé?
Tu comptes écrire tes notes pendant le cours et les enrichir après, ou plutôt tout écrire après coup?
Enfait demarons une nouvelle conversation dans ce projet pour en discuter. Peux tu me generer un prompt?

25 Feb
Voici un prompt à copier-coller dans une nouvelle conversation:

"Je suis en Data Engineering Bootcamp (Feb23–Mar27). Je veux créer un dépôt GitHub de fichiers Markdown pour centraliser mes notes de cours, fiches de révision et quizzes générés par Claude.

Le repo est créé en local sur mon Mac et sera conservé après la fin du bootcamp.

Aide-moi à définir la meilleure structure pour ce repo. Mon objectif est de pouvoir réviser efficacement, retrouver rapidement un concept, et que Claude puisse générer des fiches/quizzes dans le bon fichier.

Pose-moi les questions nécessaires avant de proposer une structure."

Tu veux que j'y ajoute autre chose?

improve my notes
"

# Notes — git-and-github

## Bash commands to try

touch

tree
cd ..
>>
>
cat
&&
||

❓: XXX —help, man XXX, tldr XXX
echo “”

Nano/ VIM: editeur qui permet de modifier un fichier depuis le terminal

- CTR X, Y Enter

## Git

Git VS GitHub:

- Git: open source version control system
- GitHub: collaborative code-hosting

git remote

git diff

## Schedule VM

https://crontab.guru/"
Show more
4 Mar

Restructured fragmented notes into organized study document
Restructured fragmented notes into organized study document
markdown
# Fiche — Terminal, Git & GitHub

## Terminal — Commandes essentielles

| Commande | Description |
|---|---|
| `touch <file>` | Crée un fichier vide |
| `cat <file>` | Affiche le contenu d'un fichier |
| `tree` | Affiche l'arborescence du dossier |
| `cd ..` | Remonte d'un niveau |
| `echo "text"` | Affiche du texte dans le terminal |
| `cmd1 && cmd2` | Exécute cmd2 **seulement si** cmd1 réussit |
| `cmd1 \|\| cmd2` | Exécute cmd2 **seulement si** cmd1 échoue |
| `>` | Redirige output vers un fichier (écrase) |
| `>>` | Redirige output vers un fichier (ajoute) |

**Obtenir de l'aide:**
```bash
man        # documentation complète
 --help    # aide rapide
tldr       # résumé pratique ⭐ (installé sur ta VM)
```

**Éditeurs terminal:**
- `nano` — simple, accessible (`Ctrl+X` → `Y` → `Enter` pour sauvegarder/quitter)
- `vim` — puissant mais courbe d'apprentissage steep (`:wq` pour quitter)

---

## Git vs GitHub

| | Git | GitHub |
|---|---|---|
| Nature | Outil local open-source | Plateforme cloud |
| Rôle | Versionne ton code | Héberge et partage les repos |
| Sans l'autre? | Fonctionne seul | Nécessite Git |

---

## Commandes Git essentielles
```bash
git init              # initialise un repo local
git remote -v         # affiche les remotes connectés
git diff              # montre les changements non stagés
git diff --staged     # montre les changements stagés
```

**Workflow standard:**
```bash
git add .
git commit -m "message"
git push
```

---

## Planifier le démarrage/arrêt de la VM

Utiliser **cron** — un scheduler Unix.
```bash
crontab -e   # éditer les tâches planifiées
```

Référence syntaxe: https://crontab.guru

Format: `minute heure jour mois jour_semaine commande`
```
0 8 * * 1-5   # tous les jours de semaine à 8h00
```
Deux choses que j'ai ajoutées par rapport à tes notes brutes: la distinction > vs >> (écrase vs ajoute — important à ne pas confondre) et le workflow Git standard. Tu veux que j'ajuste quelque chose?






Claude is AI and can make mistakes. Please double-check responses.


