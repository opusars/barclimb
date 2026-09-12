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

M2.2d remains accepted and unchanged. Bounded maintenance on `maintenance/expo-sdk57-patch-4` updates only the live Expo SDK 57 compatible patch set to Expo 57.0.22, Linking 57.0.10, and SecureStore 57.0.4 plus required lockfile transitives; React Native 0.86.3, React 19.2.3, TypeScript 5.9.3, application behavior, providers, curriculum, and controlling specifications are unchanged. After maintenance reaches green main, resume only the separately preserved M2.2e federal-question certification work; do not infer another topic or slice.

If prose conflicts with repository reality, investigate and correct the continuity docs before new architecture work. Never reconstruct missing history from guesses.
