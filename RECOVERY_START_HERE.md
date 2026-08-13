# BarClimb Recovery — Start Here

This repository must be sufficient to resume BarClimb with **zero chat history**.

1. Run `python3 scripts/validate_continuity.py` (or execute the script directly on systems where its Python 3 shebang is honored).
2. Read `docs/specs/SPEC_MANIFEST.json` and the four controlling specs only as needed.
3. Read `docs/project/PROJECT_STATE.json`.
4. Read `docs/project/PROJECT_HANDOFF.md`.
5. For context, consult `BUILD_HISTORY.md`, `DECISION_LOG.md`, `TEST_LEDGER.md`, `PROVIDER_STATUS.md`, and `CLIENT_PARITY.md`.
6. Follow `docs/project/RECOVERY_PLAYBOOK.md`.
7. Continue from **Exact next task** in the handoff.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
