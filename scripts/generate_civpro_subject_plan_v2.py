#!/usr/bin/env python3
"""Generate the body-free M2.2c V2 Civil Procedure subject-plan manifest."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = (
    ROOT
    / "apps"
    / "backend"
    / "curriculum"
    / "manifests"
    / "civil-procedure-subject-plan-2026-v2.json"
)
SCOPE_VERSION = "NCBE_NEXTGEN_SCOPE_2026_07_2027_02"
SCOPE_SHA256 = "2d8a1052ada18b413f24b7d0eef1c855a76d8a9a31688130757d5dd6511ca56f"
SOURCE_ARTIFACT = "NCBE_NEXTGEN_CONTENT_SCOPE"
START = "2026-07-01"
END = "2027-02-28"


def canonical_sha256(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


GROUPS = {
    "jurisdiction": {
        "scope_item_id": "civil-procedure-jurisdiction",
        "official_label": "Jurisdiction and related court authority",
        "source_locator": "p. 11, I.A–B",
        "treatment": "MIXED_OFFICIAL_MARKERS",
    },
    "service": {
        "scope_item_id": "civil-procedure-service-process-notice",
        "official_label": "Service of process and notice",
        "source_locator": "p. 11, I.C",
        "treatment": "RECOGNITION_WITH_OR_WITHOUT_RESOURCES",
    },
    "venue": {
        "scope_item_id": "civil-procedure-venue-transfer",
        "official_label": "Venue, forum non conveniens, and transfer",
        "source_locator": "p. 11, I.D",
        "treatment": "RECOGNITION_WITH_OR_WITHOUT_RESOURCES",
    },
    "litigation": {
        "scope_item_id": "civil-procedure-litigation",
        "official_label": "Law applied by federal courts and pretrial litigation",
        "source_locator": "pp. 11–12, II–III",
        "treatment": "MIXED_OFFICIAL_MARKERS",
    },
    "motions": {
        "scope_item_id": "civil-procedure-motions-judgments",
        "official_label": "Motions, verdicts, and judgments",
        "source_locator": "p. 13, IV–V",
        "treatment": "MIXED_OFFICIAL_MARKERS",
    },
    "appeals": {
        "scope_item_id": "civil-procedure-appeals",
        "official_label": "Appellate review",
        "source_locator": "p. 13, VI",
        "treatment": "MIXED_OFFICIAL_MARKERS",
    },
}


def hierarchy_node(stable_id, parent_id, label, locator, ordering):
    return {
        "stable_id": stable_id,
        "parent_id": parent_id,
        "official_label": label,
        "source_locator": locator,
        "ordering": ordering,
        "is_terminal": False,
        "official_marker": "NONE",
        "knowledge_treatment": "UNSPECIFIED",
        "source_artifact_id": SOURCE_ARTIFACT,
        "administration_start": START,
        "administration_end": END,
        "normalization_notes": "Official hierarchy heading; not a completeness terminal.",
    }


def terminal(stable_id, parent_id, label, locator, ordering, marker, group):
    treatment = {
        "STARRED": "RECALLED_REQUIRED",
        "UNSTARRED": "RECOGNITION_WITH_OR_WITHOUT_RESOURCES",
    }[marker]
    return {
        "stable_id": stable_id,
        "parent_id": parent_id,
        "official_label": label,
        "source_locator": locator,
        "ordering": ordering,
        "is_terminal": True,
        "official_marker": marker,
        "knowledge_treatment": treatment,
        "planning_group_scope_item_id": GROUPS[group]["scope_item_id"],
        "source_artifact_id": SOURCE_ARTIFACT,
        "administration_start": START,
        "administration_end": END,
        "normalization_notes": (
            "Short factual terminal-topic identity and marker transcribed from the "
            "hash-identified official source; explanatory source prose is not reproduced."
        ),
    }


TOPICS = [
    hierarchy_node(
        "civpro-section-i-jurisdiction-venue",
        "subject-civil-procedure",
        "I. Jurisdiction and venue",
        "p. 11, I",
        100,
    ),
    hierarchy_node(
        "civpro-subsection-i-a-federal-subject-matter",
        "civpro-section-i-jurisdiction-venue",
        "A. Federal subject-matter jurisdiction",
        "p. 11, I.A",
        110,
    ),
    terminal(
        "civpro-topic-federal-question-jurisdiction",
        "civpro-subsection-i-a-federal-subject-matter",
        "Federal question jurisdiction",
        "p. 11, I.A.1",
        111,
        "STARRED",
        "jurisdiction",
    ),
    terminal(
        "civpro-topic-diversity-jurisdiction",
        "civpro-subsection-i-a-federal-subject-matter",
        "Diversity jurisdiction",
        "p. 11, I.A.2",
        112,
        "STARRED",
        "jurisdiction",
    ),
    terminal(
        "civpro-topic-supplemental-jurisdiction",
        "civpro-subsection-i-a-federal-subject-matter",
        "Supplemental jurisdiction",
        "p. 11, I.A.3",
        113,
        "UNSTARRED",
        "jurisdiction",
    ),
    terminal(
        "civpro-topic-concurrent-removal-jurisdiction",
        "civpro-subsection-i-a-federal-subject-matter",
        "Concurrent and removal jurisdiction",
        "p. 11, I.A.4",
        114,
        "STARRED",
        "jurisdiction",
    ),
    terminal(
        "civpro-topic-personal-jurisdiction",
        "civpro-section-i-jurisdiction-venue",
        "Personal jurisdiction",
        "p. 11, I.B",
        120,
        "STARRED",
        "jurisdiction",
    ),
    terminal(
        "civpro-topic-service-process-notice",
        "civpro-section-i-jurisdiction-venue",
        "Service of process and notice",
        "p. 11, I.C",
        130,
        "UNSTARRED",
        "service",
    ),
    terminal(
        "civpro-topic-venue-forum-transfer",
        "civpro-section-i-jurisdiction-venue",
        "Venue, forum non conveniens, and transfer",
        "p. 11, I.D",
        140,
        "UNSTARRED",
        "venue",
    ),
    terminal(
        "civpro-topic-state-law-federal-court",
        "subject-civil-procedure",
        "II. State law in federal court",
        "p. 11, II",
        200,
        "UNSTARRED",
        "litigation",
    ),
    hierarchy_node(
        "civpro-section-iii-pretrial-procedures",
        "subject-civil-procedure",
        "III. Pretrial procedures",
        "p. 12, III",
        300,
    ),
    terminal(
        "civpro-topic-preliminary-injunctions-tro",
        "civpro-section-iii-pretrial-procedures",
        "Preliminary injunctions and temporary restraining orders",
        "p. 12, III.A",
        310,
        "UNSTARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-pleadings-amended-pleadings",
        "civpro-section-iii-pretrial-procedures",
        "Pleadings and amended pleadings",
        "p. 12, III.B",
        320,
        "STARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-rule-11",
        "civpro-section-iii-pretrial-procedures",
        "Rule 11",
        "p. 12, III.C",
        330,
        "STARRED",
        "litigation",
    ),
    hierarchy_node(
        "civpro-subsection-iii-d-joinder",
        "civpro-section-iii-pretrial-procedures",
        "D. Joinder of parties and claims",
        "p. 12, III.D",
        340,
    ),
    terminal(
        "civpro-topic-joinder-claims-parties",
        "civpro-subsection-iii-d-joinder",
        "Joinder of multiple claims, joinder of parties, counterclaims, crossclaims, third-party practice, and severance",
        "p. 12, III.D.1",
        341,
        "STARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-intervention-rule-24",
        "civpro-subsection-iii-d-joinder",
        "Intervention under Rule 24",
        "p. 12, III.D.2",
        342,
        "UNSTARRED",
        "litigation",
    ),
    hierarchy_node(
        "civpro-subsection-iii-e-discovery",
        "civpro-section-iii-pretrial-procedures",
        "E. Disclosures and discovery",
        "p. 12, III.E",
        350,
    ),
    terminal(
        "civpro-topic-discovery-scope-limits",
        "civpro-subsection-iii-e-discovery",
        "Scope and limits of discovery",
        "p. 12, III.E.1",
        351,
        "STARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-discovery-rule-26f",
        "civpro-subsection-iii-e-discovery",
        "Rule 26(f) conference and planning for discovery",
        "p. 12, III.E.2",
        352,
        "STARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-discovery-tools-ediscovery",
        "civpro-subsection-iii-e-discovery",
        "Discovery tools and mechanisms, including e-discovery",
        "p. 12, III.E.3",
        353,
        "STARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-discovery-motions",
        "civpro-subsection-iii-e-discovery",
        "Discovery motions",
        "p. 12, III.E.4",
        354,
        "UNSTARRED",
        "litigation",
    ),
    terminal(
        "civpro-topic-jury-trial-preservation",
        "subject-civil-procedure",
        "IV. Preserving the right to a jury trial",
        "p. 12, IV",
        400,
        "UNSTARRED",
        "motions",
    ),
    hierarchy_node(
        "civpro-section-v-dispositive-motions",
        "subject-civil-procedure",
        "V. Dispositive motions",
        "p. 13, V",
        500,
    ),
    terminal(
        "civpro-topic-rule-12-dismissal",
        "civpro-section-v-dispositive-motions",
        "Motion to dismiss under Rule 12",
        "p. 13, V.A",
        510,
        "STARRED",
        "motions",
    ),
    terminal(
        "civpro-topic-judgment-pleadings",
        "civpro-section-v-dispositive-motions",
        "Motion for judgment on the pleadings",
        "p. 13, V.B",
        520,
        "UNSTARRED",
        "motions",
    ),
    terminal(
        "civpro-topic-summary-judgment",
        "civpro-section-v-dispositive-motions",
        "Summary judgment motion",
        "p. 13, V.C",
        530,
        "STARRED",
        "motions",
    ),
    terminal(
        "civpro-topic-jmol",
        "civpro-section-v-dispositive-motions",
        "Motion for judgment as a matter of law",
        "p. 13, V.D",
        540,
        "UNSTARRED",
        "motions",
    ),
    hierarchy_node(
        "civpro-section-vi-judgments",
        "subject-civil-procedure",
        "VI. Judgments",
        "p. 13, VI",
        600,
    ),
    terminal(
        "civpro-topic-default-default-judgment",
        "civpro-section-vi-judgments",
        "Entry of default and default judgment",
        "p. 13, VI.A",
        610,
        "STARRED",
        "motions",
    ),
    terminal(
        "civpro-topic-effect-judgment-preclusion",
        "civpro-section-vi-judgments",
        "Effect of judgment",
        "p. 13, VI.B",
        620,
        "STARRED",
        "motions",
    ),
    hierarchy_node(
        "civpro-section-vii-appealability-review",
        "subject-civil-procedure",
        "VII. Appealability and review",
        "p. 13, VII",
        700,
    ),
    terminal(
        "civpro-topic-final-judgment-rule",
        "civpro-section-vii-appealability-review",
        "Final judgment rule",
        "p. 13, VII.A",
        710,
        "UNSTARRED",
        "appeals",
    ),
    terminal(
        "civpro-topic-interlocutory-review",
        "civpro-section-vii-appealability-review",
        "Availability of interlocutory review",
        "p. 13, VII.B",
        720,
        "UNSTARRED",
        "appeals",
    ),
    terminal(
        "civpro-topic-standards-review",
        "civpro-section-vii-appealability-review",
        "Standard of review on appeal",
        "p. 13, VII.C",
        730,
        "UNSTARRED",
        "appeals",
    ),
]


TOPIC_BY_ID = {topic["stable_id"]: topic for topic in TOPICS}

RELATIONSHIP_BY_KIND = {
    "ELEMENT": "HAS_ELEMENT",
    "FACTOR": "HAS_FACTOR",
    "EXCEPTION": "HAS_EXCEPTION",
    "LIMITATION": "HAS_LIMITATION",
    "DEFENSE": "HAS_DEFENSE",
    "REMEDY": "HAS_REMEDY",
    "PROCEDURAL_STEP": "HAS_PROCEDURAL_STEP",
    "DISTINCTION": "HAS_DISTINCTION",
    "DEFINITION": "DEFINES",
}


def requirement(
    stable_id, topic_id, description, requirement_type, kinds, allowed=None
):
    topic = TOPIC_BY_ID[topic_id]
    treatment = {
        "STARRED": "RECALL",
        "UNSTARRED": "RECOGNITION_WITH_OR_WITHOUT_RESOURCES",
    }[topic["official_marker"]]
    slots = []
    rule_slot = f"{stable_id}-rule" if "RULE" in kinds else None
    for kind in kinds:
        suffix = kind.lower().replace("_", "-")
        slot = {
            "stable_id": f"{stable_id}-{suffix}",
            "obligation_kind": kind,
            "minimum_count": 1,
        }
        relationship = RELATIONSHIP_BY_KIND.get(kind)
        if rule_slot and relationship:
            slot["relationship_expectations"] = [
                {
                    "source_slot_id": rule_slot,
                    "relationship_kind": relationship,
                }
            ]
        slots.append(slot)
    return {
        "stable_id": stable_id,
        "official_topic_id": topic_id,
        "planning_group_scope_item_id": topic["planning_group_scope_item_id"],
        "doctrinal_subarea": description,
        "requirement_type": requirement_type,
        "treatment_requirement": treatment,
        "allowed_obligation_kinds": allowed or kinds,
        "required_for_subject_completion": True,
        "review_required": True,
        "slots": slots,
    }


R = requirement
REQUIREMENTS = [
    R(
        "civpro-federal-question",
        "civpro-topic-federal-question-jurisdiction",
        "Federal-question jurisdiction, including the well-pleaded-complaint and arising-under boundaries.",
        "GOVERNING_RULE",
        ["RULE", "ELEMENT", "LIMITATION"],
    ),
    R(
        "civpro-diversity",
        "civpro-topic-diversity-jurisdiction",
        "Diversity jurisdiction, citizenship, complete diversity, amount in controversy, and aggregation.",
        "ELEMENTS_FACTORS",
        ["RULE", "ELEMENT", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-supplemental",
        "civpro-topic-supplemental-jurisdiction",
        "Supplemental jurisdiction, statutory inclusion limits, and discretionary declination.",
        "EXCEPTIONS_LIMITATIONS",
        ["RULE", "ELEMENT", "EXCEPTION", "LIMITATION"],
    ),
    R(
        "civpro-concurrent-jurisdiction",
        "civpro-topic-concurrent-removal-jurisdiction",
        "Concurrent federal and state court authority where the official combined topic requires it.",
        "DISTINCTIONS_DEFINITIONS",
        ["RULE", "DISTINCTION"],
    ),
    R(
        "civpro-removal-remand",
        "civpro-topic-concurrent-removal-jurisdiction",
        "Removal eligibility and procedure, remand grounds and procedure, and destination district.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-personal-specific",
        "civpro-topic-personal-jurisdiction",
        "Specific personal jurisdiction and constitutional contacts, relatedness, and reasonableness.",
        "ELEMENTS_FACTORS",
        ["RULE", "FACTOR", "LIMITATION"],
    ),
    R(
        "civpro-personal-general",
        "civpro-topic-personal-jurisdiction",
        "General personal jurisdiction for individuals and entities and the at-home distinction.",
        "DISTINCTIONS_DEFINITIONS",
        ["RULE", "ELEMENT", "DISTINCTION"],
    ),
    R(
        "civpro-personal-authority-consent-waiver",
        "civpro-topic-personal-jurisdiction",
        "Long-arm authority, consent, and waiver within the personal-jurisdiction perimeter.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-notice-constitutional",
        "civpro-topic-service-process-notice",
        "Constitutional sufficiency of notice.",
        "ELEMENTS_FACTORS",
        ["RULE", "FACTOR", "LIMITATION"],
    ),
    R(
        "civpro-service-methods",
        "civpro-topic-service-process-notice",
        "Permitted service methods for individuals and entities.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "DISTINCTION"],
    ),
    R(
        "civpro-service-waiver",
        "civpro-topic-service-process-notice",
        "Waiver of service within the official perimeter.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-venue-selection",
        "civpro-topic-venue-forum-transfer",
        "Initial federal venue selection.",
        "ELEMENTS_FACTORS",
        ["RULE", "ELEMENT", "LIMITATION"],
    ),
    R(
        "civpro-venue-improper-cure",
        "civpro-topic-venue-forum-transfer",
        "Improper venue and available cure.",
        "CONSEQUENCES_REMEDIES",
        ["RULE", "PROCEDURAL_STEP", "REMEDY"],
    ),
    R(
        "civpro-venue-transfer",
        "civpro-topic-venue-forum-transfer",
        "Statutory transfer rules and relevant branch distinctions.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "FACTOR", "PROCEDURAL_STEP", "DISTINCTION"],
    ),
    R(
        "civpro-forum-non-conveniens",
        "civpro-topic-venue-forum-transfer",
        "Forum non conveniens dismissal as distinct from statutory transfer and venue cure.",
        "CONSEQUENCES_REMEDIES",
        ["RULE", "FACTOR", "REMEDY", "DISTINCTION"],
    ),
    R(
        "civpro-erie-substance-procedure",
        "civpro-topic-state-law-federal-court",
        "Erie substance/procedure branch and circumstances in which state substantive law displaces federal decisional law.",
        "DISTINCTIONS_DEFINITIONS",
        ["RULE", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-erie-federal-rule-on-point",
        "civpro-topic-state-law-federal-court",
        "Federal-rule-directly-on-point and Rules Enabling Act branch when those authorities are implicated.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-erie-choice-of-law",
        "civpro-topic-state-law-federal-court",
        "State choice-of-law treatment within the national federal Erie inquiry.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "DISTINCTION"],
    ),
    R(
        "civpro-preliminary-injunctions-tro",
        "civpro-topic-preliminary-injunctions-tro",
        "Temporary restraining orders and preliminary injunctions as status-quo devices, including the preliminary-to-permanent relationship.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "FACTOR", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-pleading-standards-responsive",
        "civpro-topic-pleadings-amended-pleadings",
        "Complaint and answer pleading standards and responsive pleadings within the official pleading topic.",
        "GOVERNING_RULE",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-amendments-relation-back",
        "civpro-topic-pleadings-amended-pleadings",
        "Amended pleadings and relation back.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-rule-11",
        "civpro-topic-rule-11",
        "Rule 11 inquiry, support, purpose, timing, procedure, and bounded sanctions consequences.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-joinder-claims",
        "civpro-topic-joinder-claims-parties",
        "Joinder of multiple claims.",
        "ELEMENTS_FACTORS",
        ["RULE", "ELEMENT", "LIMITATION"],
    ),
    R(
        "civpro-joinder-parties",
        "civpro-topic-joinder-claims-parties",
        "Joinder of parties.",
        "ELEMENTS_FACTORS",
        ["RULE", "ELEMENT", "LIMITATION"],
    ),
    R(
        "civpro-counterclaims-crossclaims",
        "civpro-topic-joinder-claims-parties",
        "Counterclaims and crossclaims with their distinct procedural classifications.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-impleader",
        "civpro-topic-joinder-claims-parties",
        "Third-party practice and impleader.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-severance",
        "civpro-topic-joinder-claims-parties",
        "The court's overriding power to sever within the official joinder topic.",
        "CONSEQUENCES_REMEDIES",
        ["RULE", "FACTOR", "REMEDY"],
    ),
    R(
        "civpro-intervention",
        "civpro-topic-intervention-rule-24",
        "Intervention as of right and permissive intervention, including circumstances barring intervention.",
        "EXCEPTIONS_LIMITATIONS",
        ["RULE", "ELEMENT", "LIMITATION", "DISTINCTION"],
    ),
    R(
        "civpro-discovery-scope-limits",
        "civpro-topic-discovery-scope-limits",
        "Scope and limits of discovery.",
        "EXCEPTIONS_LIMITATIONS",
        ["RULE", "ELEMENT", "LIMITATION"],
    ),
    R(
        "civpro-discovery-rule-26f",
        "civpro-topic-discovery-rule-26f",
        "Rule 26(f) conference and proposed discovery planning.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-discovery-tools-ediscovery",
        "civpro-topic-discovery-tools-ediscovery",
        "Discovery tools and mechanisms, including electronically stored information.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-discovery-motions",
        "civpro-topic-discovery-motions",
        "Protective-order, privilege-claim, and compel-motion procedure, plus recognition—not exhaustive memorization—of possible sanctions.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-jury-preservation-waiver",
        "civpro-topic-jury-trial-preservation",
        "Preserving the jury-trial right and waiver consequences, excluding JMOL and generic verdict doctrine.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-rule-12-dismissal",
        "civpro-topic-rule-12-dismissal",
        "Rule 12 dismissal timing, procedure, grounds, and failure-to-state-a-claim standard.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "DEFENSE", "LIMITATION"],
    ),
    R(
        "civpro-judgment-pleadings",
        "civpro-topic-judgment-pleadings",
        "Motion for judgment on the pleadings.",
        "GOVERNING_RULE",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-summary-judgment",
        "civpro-topic-summary-judgment",
        "Summary-judgment timing, procedure, standards, and Rule 12 conversion.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION"],
    ),
    R(
        "civpro-jmol",
        "civpro-topic-jmol",
        "Judgment as a matter of law, including directed-verdict and post-verdict branches, separate from jury preservation.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-default-default-judgment",
        "civpro-topic-default-default-judgment",
        "Entry of default and default judgment.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "PROCEDURAL_STEP", "LIMITATION", "REMEDY"],
    ),
    R(
        "civpro-claim-preclusion",
        "civpro-topic-effect-judgment-preclusion",
        "Claim-preclusion elements and limits within effect of judgment.",
        "ELEMENTS_FACTORS",
        ["RULE", "ELEMENT", "EXCEPTION", "LIMITATION"],
    ),
    R(
        "civpro-issue-preclusion",
        "civpro-topic-effect-judgment-preclusion",
        "Issue-preclusion elements, limits, and distinctions from claim preclusion.",
        "DISTINCTIONS_DEFINITIONS",
        ["RULE", "ELEMENT", "EXCEPTION", "DISTINCTION", "LIMITATION"],
    ),
    R(
        "civpro-final-judgment-rule",
        "civpro-topic-final-judgment-rule",
        "Final-judgment appealability rule and supported exceptions.",
        "EXCEPTIONS_LIMITATIONS",
        ["RULE", "ELEMENT", "EXCEPTION"],
    ),
    R(
        "civpro-interlocutory-review",
        "civpro-topic-interlocutory-review",
        "Availability and distinct routes of interlocutory review within the official perimeter.",
        "PROCEDURAL_BRANCHING",
        ["RULE", "ELEMENT", "EXCEPTION", "DISTINCTION"],
    ),
    R(
        "civpro-standards-review",
        "civpro-topic-standards-review",
        "Standards of review and distinctions among the specified levels of appellate deference.",
        "DISTINCTIONS_DEFINITIONS",
        ["RULE", "DISTINCTION", "LIMITATION"],
    ),
]


def authority(stable_id, family, level, title, uri, case=False, acquired=False):
    entry = {
        "stable_id": stable_id,
        "source_family": family,
        "authority_level": level,
        "planned_title": title,
        "canonical_source_uri": uri,
        "version_requirement": "The controlling national authority effective for the July 2026–February 2027 administration period.",
        "freshness_requirement": "Verify official version, effective date, amendments, and controlling status before candidate certification.",
        "drift_action": "A material change triggers deterministic impact analysis and re-reconciliation of every mapped requirement and candidate.",
        "case_authority_required": case,
        "acquisition_status": "ACQUIRED" if acquired else "PLANNED",
    }
    if acquired:
        entry["acquired_authority"] = {
            "stable_id": "USCOURTS_FRCP",
            "source_version": "2025-12-01",
        }
    if case:
        entry["case_requirements"] = [
            {
                "stable_id": f"{stable_id}-proposition-plan",
                "proposition_type": "REQUIREMENT_SPECIFIC_CONTROLLING_HOLDING",
                "required_court": "Supreme Court of the United States",
                "exact_case_identity_required": True,
                "decision_date_required": True,
                "reliable_source_uri_required": True,
                "proposition_locator_required": True,
                "authority_status_required": True,
                "later_treatment_review_required": True,
            }
        ]
    return entry


A = authority
AUTHORITIES = [
    A(
        "authority-us-constitution-article-iii",
        "U.S. Constitution, Article III",
        "CONTROLLING_CONSTITUTION",
        "Article III",
        "https://constitution.congress.gov/constitution/article-3/",
    ),
    A(
        "authority-us-constitution-due-process",
        "U.S. Constitution, Due Process Clauses",
        "CONTROLLING_CONSTITUTION",
        "Fifth and Fourteenth Amendment Due Process Clauses",
        "https://constitution.congress.gov/",
    ),
    A(
        "authority-us-constitution-seventh",
        "U.S. Constitution, Seventh Amendment",
        "CONTROLLING_CONSTITUTION",
        "Seventh Amendment",
        "https://constitution.congress.gov/constitution/amendment-7/",
    ),
    A(
        "authority-28-usc-jurisdiction-removal",
        "Title 28 jurisdiction, removal, and remand provisions",
        "CONTROLLING_STATUTE",
        "Current Title 28 district-court jurisdiction, removal, and remand provisions",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-28-usc-venue-transfer",
        "Title 28 venue and transfer provisions",
        "CONTROLLING_STATUTE",
        "Current Title 28 venue and transfer provisions",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-rules-of-decision-act",
        "Rules of Decision Act",
        "CONTROLLING_STATUTE",
        "28 U.S.C. § 1652",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-rules-enabling-act",
        "Rules Enabling Act",
        "CONTROLLING_STATUTE",
        "28 U.S.C. §§ 2071–2077 as applicable",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-28-usc-preclusion",
        "Title 28 judgment-recognition provisions",
        "CONTROLLING_STATUTE",
        "Current Title 28 judgment-recognition provisions where applicable",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-28-usc-appellate",
        "Title 28 appellate-jurisdiction provisions",
        "CONTROLLING_STATUTE",
        "Current Title 28 appellate-jurisdiction provisions",
        "https://uscode.house.gov/",
    ),
    A(
        "authority-frcp-current",
        "Federal Rules of Civil Procedure",
        "CONTROLLING_RULE",
        "Federal Rules of Civil Procedure, amended through December 1, 2025",
        "https://www.uscourts.gov/forms-rules/current-rules-practice-procedure/federal-rules-civil-procedure",
        acquired=True,
    ),
    A(
        "authority-frap-conditional",
        "Federal Rules of Appellate Procedure",
        "CONTROLLING_RULE",
        "Current Federal Rules of Appellate Procedure only for propositions that genuinely require them",
        "https://www.uscourts.gov/forms-rules/current-rules-practice-procedure/federal-rules-appellate-procedure",
    ),
    A(
        "authority-incorporated-state-law",
        "State primary law incorporated by a federal choice-of-law inquiry",
        "OTHER_PRIMARY",
        "Exact state primary source only when a national federal rule makes the comparison necessary",
        "",
    ),
    A(
        "authority-scotus-jurisdiction",
        "U.S. Supreme Court jurisdiction authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court subject-matter-jurisdiction authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-personal-jurisdiction",
        "U.S. Supreme Court personal-jurisdiction authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court personal-jurisdiction authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-notice",
        "U.S. Supreme Court constitutional-notice authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court notice authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-venue",
        "U.S. Supreme Court venue and forum non conveniens authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court venue, transfer, or forum non conveniens authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-erie",
        "U.S. Supreme Court Erie/Hanna authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court Erie/Hanna authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-pleading-injunction",
        "U.S. Supreme Court pleading and preliminary-injunction authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court pleading or preliminary-injunction authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-preclusion",
        "U.S. Supreme Court preclusion authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court claim- and issue-preclusion authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-jury",
        "U.S. Supreme Court jury-trial authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court jury-trial authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-scotus-appellate",
        "U.S. Supreme Court appealability and review authority",
        "BINDING_SUPREME_COURT",
        "Requirement-specific controlling Supreme Court appealability or review authority",
        "https://www.supremecourt.gov/opinions/opinions.aspx",
        case=True,
    ),
    A(
        "authority-optional-secondary-reconciliation",
        "Authoritative secondary reconciliation",
        "OPTIONAL_SECONDARY",
        "Optional current secondary reconciliation source",
        "https://www.law.cornell.edu/",
    ),
]


MAPPINGS = []


def map_authority(requirement_id, authority_id, role, propositions, condition=""):
    entry = {
        "requirement_id": requirement_id,
        "authority_plan_id": authority_id,
        "role": role,
        "proposition_types": propositions,
    }
    if condition:
        entry["condition_expression"] = condition
    MAPPINGS.append(entry)


def required(requirements, authority_id, *propositions):
    for requirement_id in requirements:
        map_authority(requirement_id, authority_id, "REQUIRED", list(propositions))


def conditional(requirements, authority_id, condition, *propositions):
    for requirement_id in requirements:
        map_authority(
            requirement_id,
            authority_id,
            "CONDITIONAL",
            list(propositions),
            condition,
        )


required(
    [
        "civpro-federal-question",
        "civpro-diversity",
        "civpro-supplemental",
        "civpro-concurrent-jurisdiction",
        "civpro-removal-remand",
    ],
    "authority-28-usc-jurisdiction-removal",
    "GOVERNING_STATUTORY_TEXT",
)
conditional(
    ["civpro-federal-question", "civpro-diversity", "civpro-supplemental"],
    "authority-scotus-jurisdiction",
    "A candidate states a proposition not responsibly established by statutory text alone.",
    "CONTROLLING_HOLDING",
)
conditional(
    ["civpro-federal-question"],
    "authority-us-constitution-article-iii",
    "A candidate distinguishes constitutional judicial power from statutory jurisdiction.",
    "CONSTITUTIONAL_BOUNDARY",
)
required(
    [
        "civpro-personal-specific",
        "civpro-personal-general",
        "civpro-personal-authority-consent-waiver",
    ],
    "authority-us-constitution-due-process",
    "CONSTITUTIONAL_STANDARD",
)
required(
    [
        "civpro-personal-specific",
        "civpro-personal-general",
        "civpro-personal-authority-consent-waiver",
    ],
    "authority-scotus-personal-jurisdiction",
    "CONTROLLING_HOLDING",
)
conditional(
    ["civpro-personal-authority-consent-waiver"],
    "authority-frcp-current",
    "A candidate states a waiver or procedural-defense proposition governed by the FRCP.",
    "CONTROLLING_RULE_TEXT",
)
required(
    ["civpro-notice-constitutional"],
    "authority-us-constitution-due-process",
    "CONSTITUTIONAL_STANDARD",
)
required(
    ["civpro-notice-constitutional"], "authority-scotus-notice", "CONTROLLING_HOLDING"
)
required(
    ["civpro-service-methods", "civpro-service-waiver"],
    "authority-frcp-current",
    "CONTROLLING_RULE_TEXT",
)
required(
    [
        "civpro-venue-selection",
        "civpro-venue-improper-cure",
        "civpro-venue-transfer",
        "civpro-forum-non-conveniens",
    ],
    "authority-28-usc-venue-transfer",
    "GOVERNING_STATUTORY_TEXT",
)
conditional(
    ["civpro-venue-transfer"],
    "authority-scotus-venue",
    "The candidate states a transfer proposition not fully established by statutory text.",
    "CONTROLLING_HOLDING",
)
required(
    ["civpro-forum-non-conveniens"], "authority-scotus-venue", "CONTROLLING_HOLDING"
)
required(
    ["civpro-erie-substance-procedure"],
    "authority-rules-of-decision-act",
    "GOVERNING_STATUTORY_TEXT",
)
required(
    [
        "civpro-erie-substance-procedure",
        "civpro-erie-federal-rule-on-point",
        "civpro-erie-choice-of-law",
    ],
    "authority-scotus-erie",
    "CONTROLLING_HOLDING",
)
conditional(
    ["civpro-erie-substance-procedure"],
    "authority-us-constitution-article-iii",
    "The candidate expressly relies on a constitutional allocation proposition.",
    "CONSTITUTIONAL_BOUNDARY",
)
conditional(
    ["civpro-erie-federal-rule-on-point"],
    "authority-frcp-current",
    "A Federal Rule of Civil Procedure is directly on point for the candidate proposition.",
    "CONTROLLING_RULE_TEXT",
)
conditional(
    ["civpro-erie-federal-rule-on-point"],
    "authority-rules-enabling-act",
    "The candidate requires Rules Enabling Act validity or scope analysis.",
    "GOVERNING_STATUTORY_TEXT",
)
conditional(
    ["civpro-erie-federal-rule-on-point"],
    "authority-rules-of-decision-act",
    "No federal rule is directly on point and the Rules of Decision Act branch controls.",
    "GOVERNING_STATUTORY_TEXT",
)
required(
    ["civpro-erie-choice-of-law"],
    "authority-rules-of-decision-act",
    "GOVERNING_STATUTORY_TEXT",
)
conditional(
    ["civpro-erie-choice-of-law"],
    "authority-incorporated-state-law",
    "A national federal choice-of-law proposition requires an exact state-law fact for comparison.",
    "INCORPORATED_STATE_PRIMARY_TEXT",
)
required(
    ["civpro-preliminary-injunctions-tro", "civpro-pleading-standards-responsive"],
    "authority-frcp-current",
    "CONTROLLING_RULE_TEXT",
)
required(
    ["civpro-preliminary-injunctions-tro", "civpro-pleading-standards-responsive"],
    "authority-scotus-pleading-injunction",
    "CONTROLLING_HOLDING",
)
required(
    [
        "civpro-amendments-relation-back",
        "civpro-rule-11",
        "civpro-joinder-claims",
        "civpro-joinder-parties",
        "civpro-counterclaims-crossclaims",
        "civpro-impleader",
        "civpro-severance",
        "civpro-intervention",
        "civpro-discovery-scope-limits",
        "civpro-discovery-rule-26f",
        "civpro-discovery-tools-ediscovery",
        "civpro-discovery-motions",
    ],
    "authority-frcp-current",
    "CONTROLLING_RULE_TEXT",
)
conditional(
    ["civpro-amendments-relation-back"],
    "authority-scotus-pleading-injunction",
    "A candidate states a controlling relation-back proposition not responsibly established by rule text alone.",
    "CONTROLLING_HOLDING",
)
required(
    ["civpro-jury-preservation-waiver"],
    "authority-us-constitution-seventh",
    "CONSTITUTIONAL_TEXT",
)
required(
    ["civpro-jury-preservation-waiver"],
    "authority-frcp-current",
    "CONTROLLING_RULE_TEXT",
)
conditional(
    ["civpro-jury-preservation-waiver"],
    "authority-scotus-jury",
    "A candidate states a constitutional jury proposition not established by text and rules alone.",
    "CONTROLLING_HOLDING",
)
required(
    [
        "civpro-rule-12-dismissal",
        "civpro-judgment-pleadings",
        "civpro-summary-judgment",
        "civpro-jmol",
        "civpro-default-default-judgment",
    ],
    "authority-frcp-current",
    "CONTROLLING_RULE_TEXT",
)
conditional(
    ["civpro-rule-12-dismissal", "civpro-summary-judgment"],
    "authority-scotus-pleading-injunction",
    "A candidate states a controlling federal pleading or summary-judgment standard requiring case support.",
    "CONTROLLING_HOLDING",
)
conditional(
    ["civpro-jmol"],
    "authority-scotus-jury",
    "A candidate states a constitutional or controlling case-driven JMOL proposition.",
    "CONTROLLING_HOLDING",
)
required(
    ["civpro-claim-preclusion", "civpro-issue-preclusion"],
    "authority-scotus-preclusion",
    "CONTROLLING_HOLDING",
)
conditional(
    ["civpro-claim-preclusion", "civpro-issue-preclusion"],
    "authority-28-usc-preclusion",
    "A candidate requires a federal judgment-recognition statute.",
    "GOVERNING_STATUTORY_TEXT",
)
required(
    ["civpro-final-judgment-rule", "civpro-interlocutory-review"],
    "authority-28-usc-appellate",
    "GOVERNING_STATUTORY_TEXT",
)
required(
    ["civpro-standards-review"], "authority-scotus-appellate", "CONTROLLING_HOLDING"
)
conditional(
    ["civpro-final-judgment-rule", "civpro-interlocutory-review"],
    "authority-scotus-appellate",
    "A candidate states a case-driven appealability or review proposition not established by statute alone.",
    "CONTROLLING_HOLDING",
)
conditional(
    [
        "civpro-final-judgment-rule",
        "civpro-interlocutory-review",
        "civpro-standards-review",
    ],
    "authority-frap-conditional",
    "The exact candidate proposition genuinely depends on an appellate procedural rule.",
    "CONTROLLING_RULE_TEXT",
)


def planning_group(group):
    entry = GROUPS[group]
    return {
        **entry,
        "hierarchy_path": [
            "nextgen-current-root",
            "foundational-concepts",
            "subject-civil-procedure",
            entry["scope_item_id"],
        ],
        "classification": "CURRICULUM_PLANNING_GROUP",
        "coverage_status": (
            "PARTIALLY_COVERED" if group == "service" else "AUTHORITY_PLANNED"
        ),
        "review_required": True,
    }


payload = {
    "schema": "BARCLIMB_SUBJECT_COVERAGE_PLAN_V2",
    "manifest": {
        "stable_id": "BARCLIMB_CIVPRO_CURRICULUM_MANIFEST",
        "manifest_version": "2026_V2",
        "subject_id": "CIVIL_PROCEDURE",
        "subject_label": "Civil Procedure",
        "official_scope_version": SCOPE_VERSION,
        "official_scope_sha256": SCOPE_SHA256,
        "expected_terminal_topic_count": 27,
        "terminal_inventory_sha256": canonical_sha256(TOPICS),
        "source_class": "PRODUCTION",
        "supersedes": {
            "stable_id": "BARCLIMB_CIVPRO_CURRICULUM_MANIFEST",
            "manifest_version": "2026_V1",
        },
    },
    "coverage_policy": {
        "stable_id": "BARCLIMB_CIVPRO_COVERAGE_POLICY",
        "policy_version": "2026_V2",
        "administration_start": START,
        "administration_end": END,
        "requires_primary_authority": True,
        "requires_human_review": True,
        "certification_gate_version": "BARCLIMB_SUBJECT_CERTIFICATION_GATE_V2",
        "supersedes": {
            "stable_id": "BARCLIMB_CIVPRO_COVERAGE_POLICY",
            "policy_version": "2026_V1",
        },
        "subject_certification_requires": [
            "EVERY_ACTIVE_OFFICIAL_TERMINAL_TOPIC_ACCOUNTED_FOR",
            "EVERY_REQUIRED_SLOT_CERTIFIED",
            "APPLICABLE_REQUIRED_PRIMARY_AUTHORITY_CURRENT",
            "ZERO_BLOCKING_OMISSIONS",
            "ZERO_SUBSTANTIVE_CONFLICTS",
            "ZERO_UNSUPPORTED_JURISDICTION_CONTENT",
            "ALL_REQUIRED_HUMAN_REVIEWS_COMPLETE",
            "DETERMINISTIC_RECONCILIATION_PASSES",
            "EXACT_SCOPE_TOPIC_MANIFEST_AUTHORITY_COMPILER_POLICY_CHECKSUMS_CAPTURED",
            "EXPLICIT_SUBJECT_CERTIFICATION_OPERATION",
        ],
        "prohibited_completeness_shortcuts": [
            "SIX_PLANNING_GROUP_ROLLUP",
            "PERCENTAGE_ONLY",
            "ONE_OBLIGATION_PER_GROUP",
            "RULE4_PILOT_ONLY",
        ],
    },
    "planning_groups": [planning_group(group) for group in GROUPS],
    "official_topics": TOPICS,
    "coverage_requirements": REQUIREMENTS,
    "authority_plans": AUTHORITIES,
    "requirement_authority_mappings": MAPPINGS,
    "certified_subsets": [
        {
            "planning_group_scope_item_id": "civil-procedure-service-process-notice",
            "snapshot_id": "8ffc025a-ddac-5765-b7b2-130c84282c83",
            "compile_version": "BARCLIMB_PILOT_FRCP_RULE4_2025_V2",
            "compile_sha256": "0148dea24c906e2e257265681044ae57ad4b60b9a1e290f291e95dc2315825ec",
            "certification_sha256": "60e160e3c1a458e4c5b98569fcf3f04d409086d328496f2ed41a020a5b591ae0",
            "coverage_class": "PILOT_ONLY",
            "contribution_class": "PARTIAL_LEAF_COVERAGE",
            "national_complete": False,
            "perimeter_attribution": {
                "official_topic_id": "civpro-topic-service-process-notice",
                "required_perimeter_candidate_ids": [
                    "frcp4-waiver-request",
                    "frcp4-waiver-expense-consequence",
                    "frcp4-domestic-individual-service",
                ],
                "supplemental_candidate_ids": [
                    "frcp4-service-plaintiff-responsibility",
                    "frcp4-service-server-qualification",
                    "frcp4-service-time-limit",
                    "frcp4-good-cause-extension",
                    "frcp4-untimely-service-response",
                ],
                "timing_content_required_for_subject_completion": False,
                "attribution_note": "The immutable snapshot remains valid production evidence. Rule 4(m) timing and other content outside the exact terminal-topic perimeter are supplemental and cannot inflate subject completeness.",
            },
        }
    ],
    "planning_limitations": [
        "No new substantive Rule Obligation statements are defined.",
        "The six coarse accepted scope items are planning aggregates, not official terminal completeness units.",
        "The Rule 4 pilot remains immutable partial and supplemental evidence; it does not complete its terminal topic.",
        "No Rule 59, Rule 60, new-trial, generic verdict, broad appellate-procedure, or state-specific doctrine is required for perimeter completeness.",
        "No terminal topic, planning group, subject, assessment inventory, learner evidence, readiness, or national-completeness truth is certified.",
    ],
}
payload["canonical_sha256"] = canonical_sha256(payload)
OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
print(OUTPUT)
print(payload["canonical_sha256"])
print(f"terminal_topics={sum(topic['is_terminal'] for topic in TOPICS)}")
print(f"requirements={len(REQUIREMENTS)}")
print(f"slots={sum(len(requirement['slots']) for requirement in REQUIREMENTS)}")
print(f"authority_plans={len(AUTHORITIES)}")
print(f"authority_mappings={len(MAPPINGS)}")
