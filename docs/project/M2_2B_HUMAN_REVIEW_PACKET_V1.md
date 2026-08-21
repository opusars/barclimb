# M2.2b Human Review Packet V1 — Superseded for Correction

Status: **REVIEWED; CORRECTIONS REQUIRED; NOT APPROVED**

This immutable review-history record preserves the first human substantive-review disposition. No candidate received a final production attestation, and V1 was never certified.

## V1 identities

- Compile: `BARCLIMB_PILOT_FRCP_RULE4_2025_V1`
- Compile checksum: `32bbdc32306236809c066ca84a22f9b0bb8c4ba60a6745c2dbbd18f631c53a94`
- Policy: `BARCLIMB_FRCP_RULE4_SERVICE_PILOT@2025_V1`
- Scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Scope checksum: `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f`
- Target leaf: `civil-procedure-service-process-notice`
- Primary authority: `Fed. R. Civ. P. 4 (Dec. 1, 2025)`
- Authority SHA-256: `bd8705fc038d87e4fe222a7ea2e4324222c9430e2373fce56826bd2dfa2f8baf`

## First-review disposition

1. `frcp4-service-plaintiff-responsibility` — substantively approved, but relationship correction required. The two `HAS_PROCEDURAL_STEP` edges to Candidates 2 and 3 were misleading and must be removed.
2. `frcp4-service-server-qualification` — substantively approved, but obligation-kind correction required from `PROCEDURAL_STEP` to `LIMITATION`.
3. `frcp4-waiver-request` — rejected as written; the generic “authorized representative” language failed to preserve the Rule 4(h) addressee distinction.
4. `frcp4-waiver-expense-consequence` — rejected as written; the condition that the waiver was requested by a plaintiff located within the United States was omitted.
5. `frcp4-domestic-individual-service` — substantively approved, but wording refinement required to replace “federal delivery methods” with the precise forum-state/service-state and listed-method formulation.
6. `frcp4-service-time-limit` — approved without substantive change.
7. `frcp4-good-cause-extension` — approved without substantive change.
8. `frcp4-untimely-service-response` — approved without substantive change.

The first review did not provide or authorize a reviewer identity suitable for runtime attestation. It did not grant blanket approval. The corrected V2 candidate set requires a new human substantive review before certification.
