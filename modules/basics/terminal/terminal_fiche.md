# Fiche — terminal

---

## Session — 2026-02-24
Shell aliases and the role of ~/.zshrc as a session configuration file.

### Alias
An alias defines a custom shorthand command that the shell silently expands to a full command at execution time. Aliases are defined as `alias name="full command"` and are typically stored in `~/.zshrc` to persist across sessions.

### ~/.zshrc
A configuration file executed by Zsh every time a new terminal session opens. It is the standard location for aliases, environment variables, and PATH modifications that should be available in every session.

### source ~/.zshrc
Changes to `~/.zshrc` only take effect in new terminal sessions by default, because the file is read at session start. Running `source ~/.zshrc` forces the current session to re-read and apply the file immediately, without restarting the terminal.
