#!/usr/bin/env python3
"""Generate the complete M2.2c V2 human-review packet from its body-free manifest."""

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "apps"
    / "backend"
    / "curriculum"
    / "manifests"
    / "civil-procedure-subject-plan-2026-v2.json"
)
OUTPUT = ROOT / "docs" / "project" / "M2_2C_HUMAN_REVIEW_PACKET.md"
V1_DISPOSITION = ROOT / "docs" / "project" / "M2_2C_V1_REVIEW_DISPOSITION.json"


def inline(values):
    return ", ".join(f"`{value}`" for value in values)


manifest = json.loads(MANIFEST_PATH.read_text())
disposition = json.loads(V1_DISPOSITION.read_text())
topics = manifest["official_topics"]
topic_by_id = {topic["stable_id"]: topic for topic in topics}
terminal_topics = [topic for topic in topics if topic["is_terminal"]]
requirements_by_topic = defaultdict(list)
for requirement in manifest["coverage_requirements"]:
    requirements_by_topic[requirement["official_topic_id"]].append(requirement)
authority_by_id = {
    authority["stable_id"]: authority for authority in manifest["authority_plans"]
}
mappings_by_requirement = defaultdict(list)
for mapping in manifest["requirement_authority_mappings"]:
    mappings_by_requirement[mapping["requirement_id"]].append(mapping)


def hierarchy_path(topic):
    path = [topic["stable_id"]]
    parent_id = topic["parent_id"]
    while parent_id != "subject-civil-procedure":
        path.append(parent_id)
        parent_id = topic_by_id[parent_id]["parent_id"]
    path.append("subject-civil-procedure")
    return list(reversed(path))


lines = [
    "# M2.2c Civil Procedure Coverage-Plan Human Review Packet — V2",
    "",
    "Status: **SECOND REVIEW PENDING — NOT APPROVED — NOT SUBJECT CERTIFIED**",
    "",
    "This packet asks a qualified human reviewer to assess the corrected Civil Procedure official-topic normalization, curriculum decomposition, treatment fidelity, typed completeness requirements, and requirement-level authority plan. It does not ask for approval of substantive Rule Obligation statements. M2.2c V2 creates none.",
    "",
    "Official source bytes remain transient and are not reproduced. The short factual topic labels, hierarchy identifiers, locators, and star classifications below were normalized from the accepted hash-identified NCBE source.",
    "",
    "## Immutable inputs and review history",
    "",
    f"- Official scope: `{manifest['manifest']['official_scope_version']}`",
    f"- Official scope SHA-256: `{manifest['manifest']['official_scope_sha256']}`",
    "- Official source artifact: `NCBE_NEXTGEN_CONTENT_SCOPE@2025-08_JUL2026-FEB2027`",
    "- Official source PDF SHA-256: `22aa277048c04fdd887db66284c28bade9989b9f8a654fab05781bafa5b19b1a`",
    "- Administration period: July 2026 through February 2027",
    f"- Active subject manifest: `{manifest['manifest']['stable_id']}@{manifest['manifest']['manifest_version']}`",
    f"- Active subject-manifest SHA-256: `{manifest['canonical_sha256']}`",
    f"- Coverage policy: `{manifest['coverage_policy']['stable_id']}@{manifest['coverage_policy']['policy_version']}`",
    f"- Certification gate: `{manifest['coverage_policy']['certification_gate_version']}`",
    f"- V1 packet: `M2_2C_HUMAN_REVIEW_PACKET_V1.md`, SHA-256 `{disposition['review_packet']['sha256']}`",
    "- V1 disposition: **REJECT — REVISION REQUIRED**",
    "- V1 reviewer identity/qualification: not supplied in repository-controlled input; no formal workflow attestation was fabricated.",
    "- Existing Rule 4 compile: `BARCLIMB_PILOT_FRCP_RULE4_2025_V2`",
    "- Existing Rule 4 snapshot: `8ffc025a-ddac-5765-b7b2-130c84282c83` (`PILOT_ONLY`)",
    "- Existing compile SHA-256: `0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec`",
    "- Existing certification SHA-256: `60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0`",
    "",
    "## Changes from rejected V1",
    "",
    "1. The six coarse accepted scope items are now explicitly BarClimb planning aggregates, never terminal completeness units.",
    "2. Twenty-seven official terminal topics are represented individually with exact source hierarchy, locator, marker, treatment, and effective-period binding.",
    "3. Supplemental jurisdiction and concurrent/removal jurisdiction remain separate; concurrent jurisdiction is explicit; personal jurisdiction is decomposed without flattening.",
    "4. Rule 4(m) timing remains valid historical pilot evidence but is supplemental and not required for official-perimeter completeness.",
    "5. Venue selection, improper-venue cure, transfer, and forum non conveniens are separate planning requirements.",
    "6. Erie/Hanna authority is branch-dependent; no candidate must cite every constitutional, statutory, rule, and case family at once.",
    "7. TRO/preliminary injunctions and Rule 11 are explicit. Pleadings, joinder, intervention, discovery, and e-discovery follow terminal-topic treatment.",
    "8. Rule 12, judgment on the pleadings, summary judgment, and JMOL are separate dispositive-motion topics. Summary judgment is not pretrial-disposition coverage.",
    "9. Jury preservation is separate from JMOL. Default/default judgment and claim/issue preclusion are explicit. Rule 59/60-style posttrial relief is not required.",
    "10. Appeals are limited to final judgment, interlocutory review, and standards of review. FRAP is conditional, not a blanket completeness dependency.",
    "",
    "## Operative treatment interpretation",
    "",
    "- `STARRED` / `RECALLED_REQUIRED`: the topic requires recalled knowledge and understanding without supplied legal resources.",
    "- `UNSTARRED` / `RECOGNITION_WITH_OR_WITHOUT_RESOURCES`: the topic may be tested with or without resources; without resources, recalled understanding must be sufficient to recognize that the topic is at issue.",
    "- Aggregate `MIXED_OFFICIAL_MARKERS` is display metadata only. It cannot govern candidate treatment or establish completeness.",
    "- V2 contains 14 starred terminal topics and 13 unstarred terminal topics.",
    "",
    "## Six BarClimb planning aggregates — not official terminal leaves",
    "",
    "| Accepted coarse scope item | Display label | Locator | Aggregate treatment | Terminal topics |",
    "|---|---|---|---|---:|",
]
for group in manifest["planning_groups"]:
    count = sum(
        topic.get("planning_group_scope_item_id") == group["scope_item_id"]
        for topic in terminal_topics
    )
    lines.append(
        f"| `{group['scope_item_id']}` | {group['official_label']} | {group['source_locator']} | `{group['treatment']}` | {count} |"
    )

lines.extend(
    [
        "",
        "Completeness is computed over the 27 terminal topics and their required slots. A six-group rollup, percentage, one obligation per group, or the Rule 4 pilot cannot establish subject completeness.",
        "",
        "## Exact official terminal-topic inventory",
        "",
        "| # | Stable topic ID | Exact parent hierarchy | Official label | Locator | Marker / treatment | Planning aggregate |",
        "|---:|---|---|---|---|---|---|",
    ]
)
for number, topic in enumerate(terminal_topics, 1):
    path = " → ".join(f"`{item}`" for item in hierarchy_path(topic))
    lines.append(
        f"| {number} | `{topic['stable_id']}` | {path} | {topic['official_label']} | {topic['source_locator']} | `{topic['official_marker']}` / `{topic['knowledge_treatment']}` | `{topic['planning_group_scope_item_id']}` |"
    )

lines.extend(
    [
        "",
        "## Corrected coverage requirements, typed slots, and authority mappings",
        "",
        "Every terminal topic has at least one required planning state. Required slots state the minimum structural Rule Obligation kinds future certified candidates must satisfy; allowed kinds bound what may be proposed without implying that every allowed kind is mandatory.",
        "",
    ]
)
for topic in terminal_topics:
    lines.extend(
        [
            f"### `{topic['stable_id']}` — {topic['official_label']}",
            "",
            f"- Hierarchy: {' → '.join(f'`{item}`' for item in hierarchy_path(topic))}",
            f"- Locator: {topic['source_locator']}",
            f"- Treatment: `{topic['official_marker']}` / `{topic['knowledge_treatment']}`",
            f"- Planning aggregate: `{topic['planning_group_scope_item_id']}`",
            "",
        ]
    )
    for requirement in requirements_by_topic[topic["stable_id"]]:
        required_kinds = [slot["obligation_kind"] for slot in requirement["slots"]]
        lines.extend(
            [
                f"#### `{requirement['stable_id']}`",
                "",
                f"- Description: {requirement['doctrinal_subarea']}",
                f"- Requirement type: `{requirement['requirement_type']}`",
                f"- Treatment inherited from terminal topic: `{requirement['treatment_requirement']}`",
                f"- Required for subject completeness: `{str(requirement['required_for_subject_completion']).lower()}`",
                f"- Required Rule Obligation kinds: {inline(required_kinds)}",
                f"- Allowed Rule Obligation kinds: {inline(requirement['allowed_obligation_kinds'])}",
                "- Typed slots:",
            ]
        )
        for slot in requirement["slots"]:
            relationships = slot.get("relationship_expectations", [])
            relation_note = ""
            if relationships:
                relation_note = "; relationships: " + ", ".join(
                    f"`{item['source_slot_id']}` → `{item['relationship_kind']}`"
                    for item in relationships
                )
            lines.append(
                f"  - `{slot['stable_id']}` — `{slot['obligation_kind']}`; minimum `{slot['minimum_count']}`{relation_note}"
            )
        lines.append("- Authority mappings:")
        for mapping in mappings_by_requirement[requirement["stable_id"]]:
            authority = authority_by_id[mapping["authority_plan_id"]]
            condition = (
                f" Condition: {mapping['condition_expression']}"
                if mapping.get("condition_expression")
                else ""
            )
            lines.append(
                f"  - `{mapping['role']}` → `{mapping['authority_plan_id']}` ({authority['source_family']}); propositions: {inline(mapping['proposition_types'])}.{condition}"
            )
        lines.append("")

status_counts = Counter(
    authority["acquisition_status"] for authority in manifest["authority_plans"]
)
lines.extend(
    [
        "## Authority acquisition, conditionality, freshness, and drift",
        "",
        f"There are {len(manifest['authority_plans'])} authority plans: {status_counts['ACQUIRED']} acquired and {status_counts['PLANNED']} planned. A planned family is not evidence and cannot support certification.",
        "",
        "| Authority plan | Level | Status | Case proposition plan | Intended boundary |",
        "|---|---|---|---|---|",
    ]
)
for authority in manifest["authority_plans"]:
    lines.append(
        f"| `{authority['stable_id']}` | `{authority['authority_level']}` | `{authority['acquisition_status']}` | `{str(authority['case_authority_required']).lower()}` | {authority['planned_title']} |"
    )

lines.extend(
    [
        "",
        "Every primary family requires version/effective-date verification and deterministic drift analysis before candidate certification. Every case plan requires exact case identity, court, decision date, reliable source URI, proposition locator, current authority status, and later-treatment review. Case law is requirement-specific: text may suffice for one proposition while controlling holdings are required or conditional for another. Optional secondary reconciliation can never replace primary authority.",
        "",
        "### Erie/Hanna conditional cluster",
        "",
        "- `civpro-erie-substance-procedure` requires the Rules of Decision Act and requirement-specific controlling Supreme Court support; Article III is conditional only when a candidate expressly relies on constitutional allocation.",
        "- `civpro-erie-federal-rule-on-point` requires controlling Supreme Court support. FRCP is conditional on a federal rule being directly on point; Rules Enabling Act support is conditional on validity/scope analysis; Rules of Decision Act support is conditional on the no-direct-rule branch.",
        "- `civpro-erie-choice-of-law` requires Rules of Decision Act and controlling Supreme Court support. Exact state primary law is conditional only when the national federal inquiry makes a state-law comparison necessary.",
        "- No single generic obligation can satisfy all three branches, and no branch universally requires all authority families at once.",
        "",
        "### National federal/state boundary",
        "",
        "Federal doctrine directing incorporation or comparison of state law remains national NextGen core. Exact state-law facts may be conditional primary evidence only when a federal proposition requires them. Standalone California, New York, or other jurisdiction-specific procedure remains prohibited from national-core candidate truth.",
        "",
        "## Existing Rule 4 pilot attribution",
        "",
    ]
)
subset = manifest["certified_subsets"][0]
attribution = subset["perimeter_attribution"]
lines.extend(
    [
        f"- Snapshot: `{subset['snapshot_id']}`",
        f"- Compile SHA-256: `{subset['compile_sha256']}`",
        f"- Certification SHA-256: `{subset['certification_sha256']}`",
        f"- Classification: `{subset['coverage_class']}` / `{subset['contribution_class']}`",
        f"- Official terminal topic attribution: `{attribution['official_topic_id']}`",
        f"- Required-perimeter-relevant candidate evidence: {inline(attribution['required_perimeter_candidate_ids'])}",
        f"- Supplemental candidate evidence: {inline(attribution['supplemental_candidate_ids'])}",
        "- Rule 4(m) timing/consequences remain certified historical production evidence but are not required for Civil Procedure subject completeness.",
        "- The snapshot does not complete service/notice, Rule 4, Civil Procedure, or the national curriculum, and no obligation, review, compile, or snapshot is reopened or mutated.",
        "",
        "## Current completeness state",
        "",
        f"- Official terminal topics: `{len(terminal_topics)}`",
        f"- Planning aggregates: `{len(manifest['planning_groups'])}`",
        f"- Coverage requirements: `{len(manifest['coverage_requirements'])}`",
        f"- Required typed slots: `{sum(len(requirement['slots']) for requirement in manifest['coverage_requirements'])}`",
        f"- Authority plans: `{len(manifest['authority_plans'])}` (`{status_counts['ACQUIRED']}` acquired; `{status_counts['PLANNED']}` planned)",
        "- Certified V2 requirement slots: `0`",
        "- V2 human-review status: `PENDING`",
        "- `subject_complete: false`",
        "- `subject_certified: false`",
        "- `national_complete: false`",
        "",
        "Future `SUBJECT_CERTIFIED` requires every active terminal topic, every required slot, all applicable current primary authority, completed human review, deterministic reconciliation, zero blocking omission/conflict/jurisdiction/authority gaps, exact captured checksums, and a separate explicit certification operation. Aggregate or percentage coverage is insufficient.",
        "",
        "## Open reviewer judgments",
        "",
        "For each terminal topic and requirement, record `APPROVE`, `REJECT`, or a precise required revision. Specifically determine:",
        "",
        "1. Whether the 27-topic identities, exact parent hierarchy, locators, and 14-starred/13-unstarred classifications faithfully normalize the accepted NCBE source.",
        "2. Whether each planning aggregate is useful without being mistaken for official terminal truth.",
        "3. Whether the 43 requirements and 157 slots achieve complete structural coverage without artificial uniformity or doctrinal excess.",
        "4. Whether federal question, diversity, supplemental, concurrent/removal, and personal jurisdiction are separated at the correct level; whether concurrent jurisdiction is explicit enough.",
        "5. Whether personal-jurisdiction planning appropriately covers specific/general jurisdiction, long-arm authority, consent, waiver, and constitutional limits without exceeding the source.",
        "6. Whether service methods, waiver, and constitutional notice match the exact perimeter; whether the required-versus-supplemental Rule 4 evidence classifications are correct.",
        "7. Whether venue selection, improper-venue cure, transfer, and forum non conveniens are appropriately distinct and nationally scoped.",
        "8. Whether the three Erie/Hanna branches and their conditional constitutional/statutory/rule/state/case authority combinations are correct.",
        "9. Whether the TRO/preliminary-injunction, pleading/amendment, Rule 11, joinder, intervention, and discovery decompositions match the official pretrial perimeter.",
        "10. Whether discovery-sanctions coverage correctly requires recognition of possible sanctions without an exhaustive memorized taxonomy.",
        "11. Whether jury preservation and waiver are complete while correctly excluding JMOL and generic verdict doctrine.",
        "12. Whether Rule 12 dismissal, judgment on the pleadings, summary judgment, and JMOL remain distinct and carry correct topic-level treatment.",
        "13. Whether default/default judgment and separate claim/issue-preclusion requirements exhaust the official judgments perimeter without importing Rule 59/60 posttrial relief.",
        "14. Whether final judgment, interlocutory review, and standards of review exhaust the official appellate perimeter without broad procedure, preservation, or generic remedies.",
        "15. Whether FRAP is correctly conditional and whether every case-law family is required, conditional, or unnecessary at the correct requirement level.",
        "16. Whether any requirement should be split, combined, renamed, narrowed, or removed before substantive candidate compilation begins.",
        "",
        "## Attestation boundary",
        "",
        "A future V2 review record must identify the reviewer and qualification, the exact V2 packet SHA-256, resolution, rationale, attestation, and review time through `record_subject_plan_review`. Approval would cover this corrected planning structure only. It would not approve substantive candidate statements, complete Civil Procedure doctrine, another subject, assessment inventory, learner mastery/readiness, or national NextGen curriculum completeness.",
    ]
)

OUTPUT.write_text("\n".join(lines) + "\n")
packet_sha256 = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
print(OUTPUT)
print(packet_sha256)
print(f"lines={len(lines)}")
