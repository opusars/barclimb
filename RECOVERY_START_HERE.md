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

M2.2b is accepted in `main` at `2b042d158bb68307a0af223acec1542b62702d20`, with exact-main Foundation CI green. M2.2c is active on `m2-2c-civpro-subject-foundation`: the exact six-leaf Civil Procedure perimeter now has a versioned 18-requirement/75-slot subject plan, 16 authority-family plans, explicit case/freshness/drift needs, and a noncircular subject-certification gate. The immutable Rule 4 pilot remains only `PILOT_ONLY` partial evidence. No new substantive obligations or subject certification exist; `subject_complete` and `national_complete` remain false. Read `docs/project/CURRICULUM_COVERAGE.md` and `M2_2C_HUMAN_REVIEW_PACKET.md`. The coverage plan is `REVIEW_PENDING`; finish validation/CI and obtain qualified human review before approval, merge, or any substantive Civil Procedure candidate compilation. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
