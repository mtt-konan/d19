# Agent guidance priority maintenance

- Status: complete
- Updated: 2026-09-21
- Authorization: The user asked to implement the priority changes after the read-only audit; this task covers recommendations 1-3.
- Goal: Resolve conflicting research-entry descriptions, replace stale Copilot instructions, and route document reading by the current task.
- Allowed changes: AGENTS.md, README.md, .github/copilot-instructions.md, docs/NEXT_RESEARCH_GATE.md, docs/OPEN_DIRECTIONS.md, docs/codex/current-context.md, docs/codex/index.md, and this maintenance anchor.
- Protected behavior: Preserve mathematical claims, code, tests, certificates, existing task anchors, proof/scope rules, stable-file protection, delegation policy, and verification requirements.
- Boundary: No research continuation, numbered checkpoint, new skill, commit, or implementation of audit recommendations 4-9.
- Source: [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra); current workspace files are the implementation baseline.
- Baseline: Pre-edit copies, hashes for 911 existing tracked/unignored files, Git HEAD, index entries, and status were captured in /private/tmp/d19-guidance-priority-v_l9effw. Existing uncommitted work is preserved.
- Completion criterion: Entry documents defer task details to the selected anchor, stale Copilot references are removed, task-specific reading routes are consistent, and document links, diff checks, and preservation checks pass.
- Result: Research entry pages now defer mutable task details to the original anchor; Copilot uses current code/tooling references and the shared guide; code and documentation work no longer require a fixed research-document reading sequence.
- Validation: All 97 local link destinations and 5 heading fragments in the eight changed/new documents passed. Diff review and git diff --check passed; obsolete entry text and incoming links to renamed headings were checked. Hash comparison confirms 904 other existing tracked/unignored files are unchanged, including mathematical records, code, tests, and prior task anchors. AGENTS proof/scope, stable-file protection, delegation, and verification requirements are preserved; Git HEAD and index entries are unchanged. No research computation or tests were run for this documentation-only change.
- Next step: None for this maintenance task. The remaining audit recommendations are outside this task's scope.
