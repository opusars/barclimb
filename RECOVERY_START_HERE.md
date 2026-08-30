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

Accepted main is `1a264422dcf692e867b1f3642111f41494023c7f`, with exact-main Foundation CI green and the stable Expo SDK 57 compatibility set (`expo` 57.0.18, Linking 57.0.8, SecureStore 57.0.2, React Native 0.86.3, React 19.2.3, and TypeScript 5.9.3/exclusion). That accepted maintenance is integrated into `m2-2c-civpro-subject-foundation` by normal merge without rewriting published history. M2.2c V1's six-leaf/18-requirement/75-slot plan remains **REJECTED — REVISION REQUIRED** immutable history. V2 binds 27 exact official Civil Procedure terminal topics (14 starred/13 unstarred) to six non-authoritative planning aggregates, 43 requirements, 157 typed slots, 22 requirement-sensitive authority plans, and a noncircular terminal-topic certification gate. The immutable Rule 4 pilot remains `PILOT_ONLY` partial/supplemental evidence; zero V2 slots are certified, `subject_complete` and `national_complete` remain false, and no candidate compilation occurred. Read `docs/project/CURRICULUM_COVERAGE.md`, `M2_2C_HUMAN_REVIEW_PACKET_V1.md`, `M2_2C_V1_REVIEW_DISPOSITION.json`, and the active `M2_2C_HUMAN_REVIEW_PACKET.md`. Require green exact-merge CI, then stop at `SECOND_REVIEW_PENDING` for qualified human review—do not infer approval, certify, merge to main, or begin another slice. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
