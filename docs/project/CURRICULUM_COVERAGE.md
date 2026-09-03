# Curriculum Coverage Ledger

This ledger is cold-recovery state, not a release certification.

## Civil Procedure — M2.2c V3 planning state

- Official scope: `NCBE_NEXTGEN_SCOPE_2026_07_2027_02`
- Scope SHA-256: `2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f`
- Rejected historical manifest: `BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V1`
- V1 packet SHA-256: `153746608c27abad008dbfa5cd858113c746696ed05fc410a1b6242e558b1f6c`
- V1 disposition: `REJECT — REVISION REQUIRED`; reviewer identity was not supplied, so no formal
  workflow review record was fabricated.
- Archived V2 manifest: `BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V2`
- V2 manifest SHA-256: `ff98c996ac55135b6e7c0dc6410cac4be965a1c7f482a9c8cc6aff7a9b7cba20`
- V2 packet SHA-256: `9f7b27c1270f60dbf71a5c2baf15c7c5183a484e6e381737442ee29999b1047a`
- V2 disposition: `REVISE — NARROW V3 CORRECTION REQUIRED`; reviewer identity was not supplied,
  so no formal workflow review record was fabricated.
- Active subject manifest: `BARCLIMB_CIVPRO_CURRICULUM_MANIFEST@2026_V3`
- V3 manifest SHA-256: `b706b7182ab165377a9e60520b083cdaf87562b256dfb0c371f9aa38d948c0c3`
- Coverage policy: `BARCLIMB_CIVPRO_COVERAGE_POLICY@2026_V3`
- Human review: `APPROVE — COVERAGE PLAN ACCEPTED`
- Reviewed commit: `d4908c78cf185ce4bb5342802dfa79d7866af2d1`
- Exact reviewed V3 packet SHA-256: `5a0b02efe178e2c8996a95cd19a5e1b0122ac242ad8505dad2b079e94dd9646b`
- Immutable review-manifest SHA-256: `6ceea17f91c7523c993a25a702b6e7ab923117d8a918baa7ed916d57bac87c97`
- Active post-review packet SHA-256: `07bc499231dbd32a7854b551f9bfc3ba34453ea702ce714f06624d930cc4376e`
- Official terminal topics: 27 (`STARRED`: 14; `UNSTARRED`: 13)
- BarClimb planning aggregates: 6; never completeness units
- Coverage requirements: 43
- Required typed slots: 149 (V2: 157)
- Certified V3 slots: 0
- Authority plans before M2.2d: 22 (`ACQUIRED`: 1, `PLANNED`: 21)
- Effective authority state after bounded federal-question acquisition: 22 (`ACQUIRED`: 1,
  `PARTIALLY_ACQUIRED`: 2, `PLANNED`: 19). The two partial shared plans are
  `authority-28-usc-jurisdiction-removal` and `authority-scotus-jurisdiction`; no unrelated plan is
  treated as acquired.
- Current status: service/process/notice retains a bounded historical partial subset; all terminal
  topics remain incomplete for V3 subject certification.
- `subject_complete`: `false`
- `subject_certified`: `false`
- `national_complete`: `false`

The linked historical subset is Rule 4 snapshot `8ffc025a-ddac-5765-b7b2-130c84282c83`, compile
`0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`, certification
`60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`, `PILOT_ONLY`. Its approved
obligations and review evidence are unchanged. Waiver and domestic-individual-service candidates are
perimeter-relevant evidence; Rule 4(m) timing and other out-of-perimeter content remain valid
supplemental evidence. Nothing in the snapshot automatically satisfies a V3 slot or completes the
service terminal topic.

The plan-review gate is satisfied by Leo Rayos's exact supplied approval, recorded through
`record_subject_plan_review`. The reviewed packet bytes remain at
`M2_2C_HUMAN_REVIEW_PACKET_V3_REVIEWED.md`; the operator input and immutable bindings remain at
`M2_2C_V3_HUMAN_REVIEW_RECORD.json`. The V1 and V2 packet/disposition history is unchanged. Approval
permitted the separately authorized bounded M2.2d compilation; it did not itself acquire authority,
approve candidate statements, satisfy any slot, or mass-certify Civil Procedure. The current gate is
qualified review of the three exact federal-question candidates only.

## Civil Procedure — M2.2d federal-question candidate state

- Topic: `civpro-topic-federal-question-jurisdiction` (`STARRED` / `RECALLED_REQUIRED`)
- Requirement: `civpro-federal-question`
- Candidate slots: `RULE`, `ELEMENT`, `LIMITATION`; all three have one reconciled candidate
- Candidate compile SHA-256: `a46fbd51a441ec54fa74f2826a50241ff94e4fd3eefa49e24e568174d15b606d`
- Human candidate review: `PENDING` for all three
- Certification eligibility: `false`
- Certified V3 slots: 0 of 149; the other 146 slots received no candidate in this slice
- Review packet: `M2_2D_CIVPRO_FEDERAL_QUESTION_HUMAN_REVIEW_PACKET.md`; SHA-256
  `4fdf1c70c1a4228537880c500856198809ef368d53abbc465027bb5389696eda`
- `subject_complete`: `false`
- `subject_certified`: `false`
- `national_complete`: `false`

The §1331 and Mottley sources are registered by exact hash and proposition locator; raw bytes remain
transient. The cluster neither mutates the Rule 4 pilot nor covers removal, diversity, supplemental
jurisdiction, personal jurisdiction, Erie, venue, complete preemption, Article III boundaries, or
embedded-federal-question doctrine.
