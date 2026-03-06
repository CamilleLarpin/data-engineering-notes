
---

## Session — 2026-02-24
Distinction between Git and GitHub, and using gh CLI to create repositories.

### Git vs GitHub
Git is a local, open-source version control system. GitHub is a cloud platform for hosting and sharing Git repositories. Git functions independently of GitHub; GitHub requires Git.

### Creating a Repository with gh CLI
`gh repo create <name> --public --clone` creates a remote repository on GitHub and clones it locally in a single command. This is preferred over `git init` when starting a new project from scratch, as it establishes the remote connection immediately.

### gh Authentication
`gh auth login` is required before any `gh` CLI commands can interact with GitHub. Authentication is separate from Git credential configuration.
