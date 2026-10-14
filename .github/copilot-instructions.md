# Copilot Instructions

Follow the shared [Agent Guide](../AGENTS.md) for task routing, proof and scope
rules, stable-file protection, and verification. Use its
[task-specific reading table](../AGENTS.md#read-for-the-task); local code or
documentation edits do not require restoring research context.

## Code And Tooling References

- Use the [script index](../scripts/README.md) to locate executable entry points
  when needed. The search CLI entry is [scripts/search.py](../scripts/search.py);
  its parser and runners are in
  [src/rational_distance/cli/search/](../src/rational_distance/cli/search/).
  Follow the selected runner's imports to the owning implementation.
- [pyproject.toml](../pyproject.toml) owns dependency, pytest, and Ruff settings.
  The project uses `uv` with `package = false`. Apply the shared guide's
  verification commands to the files and tests affected by the requested change.
- For research recovery, use [current-context.md](../docs/codex/current-context.md)
  to locate the relevant task anchor. Its recorded research entry does not
  select work for the current request.
