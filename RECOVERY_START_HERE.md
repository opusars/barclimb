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

M2.2c is accepted on `main` at `e7b1517dc0a048ecf4b102306dd0e9e86f2401f8`. The active branch is `m2-2d-civpro-federal-question`, containing only the separately authorized federal-question authority/candidate slice. Official House § 1331 and official U.S. Reports Mottley sources are hash-registered with transient bytes; three candidates map to the exact approved `RULE`, `ELEMENT`, and `LIMITATION` slots and reconcile at SHA-256 `a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d` with zero findings. Leo Rayos's three exact `APPROVE` decisions are recorded through the immutable obligation-review workflow; exact replay is idempotent and the candidate-review prerequisite is satisfied. No certification or snapshot exists. Effective authority-plan state remains one acquired, two partially acquired, and 19 planned. M2.2c 27/14/13/43/149 truth, plan-review SHA `6ceea17f91c7523c993a25a702b6e7ab923117d8a918baa7ed916d57bac87c97`, and Rule 4 evidence remain unchanged; zero V3 slots are certified and `subject_complete`, `subject_certified`, and `national_complete` remain false. The branch must stop at post-candidate-approval acceptance review after exact-branch CI; do not certify, acquire another authority family, compile another topic, merge, or begin another slice without authorization. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
