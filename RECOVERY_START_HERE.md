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

M2.2e is accepted on `main` through `29b675e135fc07b1d4c2ef15bfdb76abd28117a8`. It certifies only `civpro-topic-federal-question-jurisdiction` through the canonical immutable snapshot workflow: three reviewed §1331/Mottley candidates satisfy the exact `RULE`, `ELEMENT`, and `LIMITATION` slots. Snapshot `e3afd28e-f846-5e1a-b318-d4d6b58ec40c` has certification SHA-256 `b94770c91dd3666ff37365fdd583bc1c173f2ad3a677b71581525c1a3fe211b7`. Civil Procedure is 3/149 slots with 146 unresolved; effective authority plans remain one acquired, two partially acquired, and 19 planned. The lockfile-only `js-yaml` 4.3.1 → 4.3.2 patch removes the high advisory without an override or behavior change. Expo/Linking/SecureStore remain 57.0.22/57.0.10/57.0.4; Rule 4 evidence is unchanged; `subject_complete`, `subject_certified`, and `national_complete` remain false. Do not begin another topic or Milestone 2 slice without separate authorization.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
