
---

## Session — 2026-02-24
Distinction between Git and GitHub, and using gh CLI to create repositories.

### Git vs GitHub
Git is a local, open-source version control system. GitHub is a cloud platform for hosting and sharing Git repositories. Git functions independently of GitHub; GitHub requires Git.

### Creating a Repository with gh CLI
`gh repo create <name> --public --clone` creates a remote repository on GitHub and clones it locally in a single command. This is preferred over `git init` when starting a new project from scratch, as it establishes the remote connection immediately.

### gh Authentication
`gh auth login` is required before any `gh` CLI commands can interact with GitHub. Authentication is separate from Git credential configuration.

---

## Session — 2026-03-09
Git branching, remotes, stash, and PR management across a fork

### .git/index.lock
A residual lock file created when a git process crashes mid-operation. It prevents subsequent git commands from running. Safe to delete manually with `rm .git/index.lock`.

### Background vs sequential operators
`&` runs a command in the background (non-blocking), while `&&` runs the next command only if the previous one succeeded. Mixing them in a git workflow can cause race conditions between `git add` and `git commit`.

### git fetch
Downloads the remote state without modifying the local working directory or branches.

### git stash / git stash pop
`git stash` saves uncommitted changes to a temporary stack, leaving a clean working directory. `git stash pop` reapplies those changes onto the current branch.

### git checkout -b <branch> <remote/branch>
Creates a new local branch starting from the exact commit of a specified remote branch.

### git branch -d vs git push <remote> --delete
`git branch -d` deletes a branch locally (only if already merged). `git push <remote> --delete <branch>` deletes the corresponding branch on the remote.

### git branch -a
Lists all branches, both local and remote-tracking.

### Forked repo remotes
A fork typically has two remotes: `origin` (the upstream bootcamp repo, read-only) and `fork` (the personal fork, writable). Pushes and PRs target `fork`.

### Default branch and PR target
A PR's base branch cannot be changed after creation. To retarget, close the existing PR, change the default branch in the fork's Settings → Branches, then open a new PR.
