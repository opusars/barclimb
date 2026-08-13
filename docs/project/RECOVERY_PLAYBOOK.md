# BarClimb Cold Recovery Playbook

Use this when all prior chat context is unavailable.

1. Run `python3 scripts/validate_continuity.py`. Stop if it fails. On systems that honor the executable Python 3 shebang, invoking `scripts/validate_continuity.py` directly is also valid.
2. Read `docs/project/PROJECT_STATE.json` and `PROJECT_HANDOFF.md`.
3. Read `docs/specs/SPEC_MANIFEST.json`; verify only its four specs are controlling.
4. Read only spec sections relevant to the current milestone/task.
5. Inspect build history, decisions, tests, provider status, and client parity.
6. Inspect actual source, migrations, config, and test state. Do not assume prose is newer than code.
7. Run documented local smoke/tests.
8. Reconcile any discrepancy before architecture changes.
9. Continue from the handoff's **Exact next task**.
10. Before finishing a material slice, update state/handoff/history/tests and affected ledgers; run continuity validation again.

## Recovery success criterion
A new agent must be able to explain current milestone, completed work, blockers, latest verified tests/providers, and exact next step without using any prior conversation.
