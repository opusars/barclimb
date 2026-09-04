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

Accepted main is `8463d68ce2e82d1b105646181da06ef8cf788583`, including bounded Expo SDK 57 patch maintenance to Expo 57.0.20 with Linking 57.0.9, SecureStore 57.0.3, React Native 0.86.3, React 19.2.3, and TypeScript 5.9.3/exclusion unchanged. The active branch is `m2-2d-civpro-federal-question`; accepted main was normally merged into its immutable reviewed federal-question slice without rewriting published history. Official House § 1331 and official U.S. Reports Mottley sources remain hash-registered with transient bytes; three candidates map to the exact approved `RULE`, `ELEMENT`, and `LIMITATION` slots and reconcile at SHA-256 `a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d` with zero findings. Leo Rayos's three exact `APPROVE` decisions remain immutable; no certification or snapshot exists. Effective authority-plan state remains one acquired, two partially acquired, and 19 planned. M2.2c 27/14/13/43/149 truth, plan-review SHA `6ceea17f91c7523c993a25a702b6e7ab923117d8a918baa7ed916d57bac87c97`, and Rule 4 evidence remain unchanged; `subject_complete`, `subject_certified`, and `national_complete` remain false. Stop at post-candidate-approval acceptance review after exact-feature CI.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
