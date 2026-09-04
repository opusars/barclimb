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

M2.2c is accepted and merged into `main`. The current bounded maintenance branch refreshes only stable Expo SDK 57 patch metadata (`expo` 57.0.19 → 57.0.20 plus required transitive Expo patches) while retaining Linking 57.0.9, SecureStore 57.0.3, React Native 0.86.3, React 19.2.3, and TypeScript 5.9.3/exclusion. Accepted V3 preserves 27 official Civil Procedure terminal topics (14 starred/13 unstarred), six non-authoritative planning aggregates, 43 requirements, 149 typed slots, and 22 authority plans (one acquired/21 planned); V1/V2 remain immutable history. M2.2d remains separately published at `c3e71259c6839ec3ae46d57e92e1da402b04a370` with its reviewed federal-question candidates immutable and awaiting this accepted-main maintenance integration. The immutable Rule 4 pilot remains `PILOT_ONLY` partial/supplemental evidence; Civil Procedure subject/national completeness remain false. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
