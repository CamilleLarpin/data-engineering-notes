# Fiche — testing-ci-cd

---

## Session — 2026-03-06
Building a GitHub Actions CI workflow with Poetry, and understanding each YAML directive

### Three mandatory keys in a GitHub Actions workflow
Every workflow requires: a trigger (`on`), a runner (`runs-on`), and one or more jobs with their steps.

### Trigger (`on`)
Defines which Git events activate the workflow. Restricting to `push: branches: [main]` means the workflow only runs on direct pushes to main, not on pull requests or other branches.

### Runner (`runs-on`)
Specifies the virtual machine GitHub provisions to execute the job. `ubuntu-latest` is a Linux VM managed and provided free of charge by GitHub for public repositories.

### `actions/checkout`
Clones the repository onto the runner VM. Without this step, the VM has no access to the project's source code.

### `actions/setup-python`
Installs a specific Python version on the runner VM, ensuring the environment matches the declared `requires-python` constraint.

### Installing dependencies with Poetry in CI
Poetry is installed via `pip`, then `poetry install --with dev` installs all runtime and dev dependencies (including pytest) declared in `pyproject.toml`, without needing a separate `requirements.txt`.

### `pyproject.toml` as the single source of truth
Using `pyproject.toml` with `[dependency-groups]` (PEP 735, supported by Poetry 2.x) replaces `requirements.txt` for both local and CI dependency management.

### `.git/index.lock` error
This lock file is a residual artifact left by a git process that crashed. It must be removed manually (`rm .git/index.lock`) before git commands can run again. Using `&` (background execution) instead of `&&` (sequential execution) between git commands can cause this conflict because the backgrounded process may still hold the lock when the next command starts.

---

## Session — 2026-03-09
Writing and understanding a GitHub Actions pytest workflow using Poetry

### GitHub Actions trigger
The `on:` key defines when a workflow runs. `push: branches: [main]` restricts execution to pushes targeting the `main` branch only.

### Job runner
`runs-on: ubuntu-latest` provisions a fresh Ubuntu virtual machine hosted by GitHub for each workflow run. It has no project code, no Python, and no dependencies pre-installed.

### actions/checkout
Clones the repository onto the runner VM. Without this step the runner has no access to any project files.

### actions/setup-python
Installs a specified Python version on the runner VM.

### Installing dependencies via Poetry in CI
Poetry is not pre-installed on GitHub runners. It must be installed with `pip install poetry` first, then `poetry install --with dev` installs all dependency groups including the dev group that contains pytest.

### Running tests in CI
`poetry run pytest` executes pytest inside the Poetry-managed virtual environment on the runner, equivalent to running `pytest` locally after activating the environment.

### Empty YAML workflow file
An empty `.github/workflows/*.yml` file is not a valid GitHub Actions workflow and will cause all triggered runs to fail with a parse error.
