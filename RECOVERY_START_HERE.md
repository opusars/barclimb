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

M2.2a is accepted in `main` at `a468fb6d3d850757fe1af82c18f244e95ad77de8`, with exact-main Foundation CI green. M2.2b is active on `m2-2b-real-scope-authority-pilot`: current NCBE Content Scope/Blueprint provenance and the one-leaf Rule 4 pilot are deterministic and body-free. Leo Rayos approved all eight corrected V2 obligations against the hash-identified FRCP authority, and exact-byte operator execution created immutable `PILOT_ONLY` snapshot `8ffc025a-ddac-5765-b7b2-130c84282c83` with `national_complete: false`. Read `docs/project/M2_2B_HUMAN_REVIEW_PACKET.md` and `M2_2B_CERTIFICATION_RECORD.json`; V1 correction history remains separate. Exact-commit CI/review/merge are next—do not broaden the certification, merge automatically, or begin the next slice. Apple enrollment/signing, physical-device authentication/SecureStore, live OS association routing, store ownership/approval, and native production purchase/restore remain mandatory at the applicable Native GA and are not marked verified.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
