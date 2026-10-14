# Delegation Protocol

This document is read only when the user or the selected task explicitly
authorizes delegation. The repository default is no delegation.

## Controller command

Use exactly:

```bash
~/.claude/skills/codex/scripts/ask_codex.sh \
  --workspace /Users/konan/Desktop/d19 \
  --model gpt-5.6-luna \
  --reasoning max \
  "<focused task>"
```

`gpt-5.6-luna` is the model name and `max` is the reasoning level. `xhigh` is
also verified, but `max` is the project default. Do not modify tasks that were
already running when this contract was adopted.

## Worker boundary

Every delegated prompt must begin exactly with:

```text
You are the Worker. Do not invoke codex, ask_codex.sh, subagents, or delegation skills.
```

Delegation is one level deep. Only the Controller invokes `ask_codex.sh`;
Workers solve the assigned task directly and do not recursively delegate.

Treat exit 130, empty output, or evidence that the Worker invoked Codex as a
failed run. Restore the boundary and retry with a fresh Worker.

## Controller review

Worker output is proposed work, not accepted proof or a completed checkpoint.
The Controller independently checks formulas, converses, exceptional branches,
changed files, focused tests, and targeted Ruff results.
