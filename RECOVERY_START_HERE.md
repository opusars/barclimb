# BarClimb Recovery — Start Here

This repository must be sufficient to resume BarClimb with **zero chat history**.

Controlling release sequence: **Web GA → iOS Native GA → Android Native GA**. Web-first never means Web-only: shared server/domain truth and explicit native architecture/parity obligations begin in Milestone 1.

1. Run `python3 scripts/validate_continuity.py` (or execute the script directly on systems where its Python 3 shebang is honored).
2. Read `docs/specs/SPEC_MANIFEST.json` and the four controlling specs only as needed.
3. Read `docs/project/PROJECT_STATE.json`.
4. Read `docs/project/PROJECT_HANDOFF.md`.
5. For context, consult `BUILD_HISTORY.md`, `DECISION_LOG.md`, `TEST_LEDGER.md`, `PROVIDER_STATUS.md`, `CLIENT_PARITY.md`, and `SECURITY_ADVISORIES.md`.
6. Follow `docs/project/RECOVERY_PLAYBOOK.md`.
7. Continue from **Exact next task** in the handoff.

M2.2b is accepted in `main` at `2b042d158bb68307a0af223acec1542b62702d20`, with exact-main Foundation CI green. A bounded Expo SDK 57 patch-maintenance branch updates only the live compatibility set (`expo` 57.0.18, Linking 57.0.8, SecureStore 57.0.2, and React Native 0.86.3) plus npm-resolved transitive patches and continuity evidence; it changes no product behavior. M2.2c remains paused and untouched at `m2-2c-civpro-subject-foundation@0436b0d63cbab2fd1a0ef15125683da5967e4150` until this maintenance branch is reviewed, merged separately, and brought forward without rewriting history. Do not begin M2.2c second human review, approval, or candidate compilation from this branch. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
