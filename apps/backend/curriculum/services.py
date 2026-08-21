import base64
import re
import unicodedata
from collections import Counter, defaultdict

from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from official_scope.models import OfficialScopeVersion
from official_scope.services import canonical_sha256, sha256_bytes

from .models import (
    AuthorityEvidence,
    AuthoritySource,
    CoveragePolicy,
    CoverageReleaseSnapshot,
    CurriculumCompileVersion,
    ObligationHumanReview,
    ObligationRelationship,
    ObligationScopeMapping,
    ReconciliationIssue,
    ReviewResolution,
    RuleObligation,
)

RELATIONSHIP_TARGET_KIND = {
    "HAS_ELEMENT": "ELEMENT",
    "HAS_FACTOR": "FACTOR",
    "HAS_EXCEPTION": "EXCEPTION",
    "HAS_LIMITATION": "LIMITATION",
    "HAS_DEFENSE": "DEFENSE",
    "HAS_REMEDY": "REMEDY",
    "HAS_PROCEDURAL_STEP": "PROCEDURAL_STEP",
    "HAS_DISTINCTION": "DISTINCTION",
    "DEFINES": "DEFINITION",
    "HAS_ETHICS_DUTY": "ETHICS_DUTY",
}


def normalize_statement(value):
    normalized = unicodedata.normalize("NFKC", value or "")
    return re.sub(r"\s+", " ", normalized).strip().casefold()


def _issue(compile_version, stable_id, category, severity, message, **links):
    checksum = canonical_sha256(
        {
            "stable_id": stable_id,
            "category": category,
            "severity": severity,
            "message": message,
            "scope_item": str(getattr(links.get("scope_item"), "pk", "")),
            "obligation": str(getattr(links.get("obligation"), "pk", "")),
        }
    )
    issue, created = ReconciliationIssue.objects.get_or_create(
        compile_version=compile_version,
        stable_id=stable_id,
        defaults={
            "category": category,
            "severity": severity,
            "message": message,
            "canonical_sha256": checksum,
            **links,
        },
    )
    if not created and issue.canonical_sha256 != checksum:
        raise ValidationError(f"Issue identity changed during deterministic rerun: {stable_id}")
    return issue


def register_authority(*, content, **metadata):
    checksum = sha256_bytes(content)
    identity = {
        "stable_id": metadata["stable_id"],
        "source_version": metadata["source_version"],
    }
    existing = AuthoritySource.objects.filter(**identity).first()
    if existing:
        immutable = (
            "authority_class",
            "authority_type",
            "title",
            "canonical_citation",
            "source_uri",
            "source_class",
            "is_national",
            "jurisdiction",
            "issuing_authority",
            "publication_date",
            "effective_date",
            "retrieved_at",
            "media_type",
            "storage_disposition",
            "rights_basis",
        )
        if existing.content_sha256 != checksum or any(
            getattr(existing, key) != metadata.get(key, getattr(existing, key)) for key in immutable
        ):
            raise ValidationError("Authority identity exists with different immutable input.")
        return existing, False
    authority = AuthoritySource(content_sha256=checksum, **metadata)
    authority.save()
    return authority, True


def _register_policy(definition, source_class):
    allowed = sorted(definition.get("allowed_obligation_kinds", RuleObligation.Kind.values))
    unknown = set(allowed) - set(RuleObligation.Kind.values)
    if unknown:
        raise ValidationError(f"Unknown policy obligation kinds: {sorted(unknown)}")
    canonical = {
        "stable_id": definition["stable_id"],
        "policy_version": definition["policy_version"],
        "minimum_obligations_per_leaf": definition.get("minimum_obligations_per_leaf", 1),
        "requires_primary_authority": definition.get("requires_primary_authority", True),
        "allowed_obligation_kinds": allowed,
        "source_class": source_class,
        "coverage_class": definition.get("coverage_class", "NATIONAL"),
        "target_scope_item_ids": sorted(definition.get("target_scope_item_ids", [])),
        "requires_human_review": definition.get("requires_human_review", False),
    }
    checksum = canonical_sha256(canonical)
    policy = CoveragePolicy.objects.filter(
        stable_id=canonical["stable_id"], policy_version=canonical["policy_version"]
    ).first()
    if policy:
        if policy.canonical_sha256 != checksum:
            raise ValidationError("Coverage policy identity exists with different rules.")
        return policy
    return CoveragePolicy.objects.create(
        canonical_sha256=checksum,
        **canonical,
    )


def _compile_canonical(compile_version):
    obligations = []
    for obligation in compile_version.obligations.order_by("stable_id"):
        obligations.append(
            {
                "stable_id": obligation.stable_id,
                "kind": obligation.kind,
                "normalized_statement": obligation.normalized_statement,
                "canonical_sha256": obligation.canonical_sha256,
                "compiler_status": obligation.compiler_status,
                "decision": obligation.decision,
                "is_core": obligation.is_core,
                "jurisdiction": obligation.jurisdiction,
                "scope_items": sorted(obligation.scope_items.values_list("stable_id", flat=True)),
                "evidence": sorted(
                    [
                        [
                            evidence.authority.stable_id,
                            evidence.authority.source_version,
                            evidence.role,
                            evidence.locator,
                            evidence.proposition_sha256,
                            evidence.supports,
                        ]
                        for evidence in obligation.authority_evidence.select_related("authority")
                    ]
                ),
            }
        )
    relationships = sorted(
        [
            [edge.source.stable_id, edge.kind, edge.target.stable_id, edge.ordering]
            for edge in ObligationRelationship.objects.filter(
                source__compile_version=compile_version
            ).select_related("source", "target")
        ]
    )
    return {
        "scope_sha256": compile_version.official_scope_version.normalized_sha256,
        "compiler_schema_version": compile_version.compiler_schema_version,
        "policy_sha256": compile_version.coverage_policy.canonical_sha256,
        "source_class": compile_version.source_class,
        "obligations": obligations,
        "relationships": relationships,
    }


def _would_cycle(source, target):
    pending = [target.pk]
    visited = set()
    while pending:
        current = pending.pop()
        if current == source.pk:
            return True
        if current in visited:
            continue
        visited.add(current)
        pending.extend(
            ObligationRelationship.objects.filter(source_id=current).values_list(
                "target_id", flat=True
            )
        )
    return False


@transaction.atomic
def compile_manifest(payload, *, authority_contents=None):
    if payload.get("schema") not in (
        "BARCLIMB_RULE_COMPILER_V1",
        "BARCLIMB_RULE_COMPILER_V2",
    ):
        raise ValidationError("Unsupported Rule Obligation compiler schema.")
    authority_contents = authority_contents or {}
    input_checksum = canonical_sha256(payload)
    definition = payload["compile"]
    existing = CurriculumCompileVersion.objects.filter(
        version_identifier=definition["version_identifier"]
    ).first()
    if existing:
        if existing.input_sha256 != input_checksum:
            raise ValidationError("Compile identity exists with different deterministic input.")
        return existing, False
    scope = OfficialScopeVersion.objects.get(
        version_identifier=definition["official_scope_version"]
    )
    if scope.status not in (
        OfficialScopeVersion.Status.ACTIVE,
        OfficialScopeVersion.Status.SUPERSEDED,
    ):
        raise ValidationError("Compiler requires immutable active or superseded official scope.")
    supersedes = None
    if definition.get("supersedes"):
        supersedes = CurriculumCompileVersion.objects.get(
            version_identifier=definition["supersedes"]
        )
    source_class = definition.get("source_class", "TEST_FIXTURE")
    policy = _register_policy(payload["coverage_policy"], source_class)
    compile_version = CurriculumCompileVersion.objects.create(
        version_identifier=definition["version_identifier"],
        official_scope_version=scope,
        coverage_policy=policy,
        compiler_schema_version=definition["compiler_schema_version"],
        input_sha256=input_checksum,
        source_class=source_class,
        coverage_class=policy.coverage_class,
        national_complete=False,
        supersedes=supersedes,
    )
    authority_map = {}
    for entry in payload.get("authorities", []):
        if "content_base64" in entry:
            try:
                content = base64.b64decode(entry["content_base64"], validate=True)
            except Exception as error:
                raise ValidationError("Authority content_base64 is invalid.") from error
        else:
            content = authority_contents.get(entry["stable_id"])
            if content is None:
                raise ValidationError(
                    f"Operator-controlled bytes are required for {entry['stable_id']}."
                )
            if sha256_bytes(content) != entry.get("expected_sha256"):
                raise ValidationError(
                    f"Authority bytes do not match expected_sha256 for {entry['stable_id']}."
                )
        authority, _ = register_authority(
            content=content,
            stable_id=entry["stable_id"],
            source_version=entry["source_version"],
            authority_class=entry["authority_class"],
            authority_type=entry["authority_type"],
            title=entry["title"],
            canonical_citation=entry["canonical_citation"],
            source_uri=entry.get("source_uri", ""),
            source_class=entry.get("source_class", source_class),
            is_national=entry.get("is_national", True),
            jurisdiction=entry.get("jurisdiction", ""),
            issuing_authority=entry.get("issuing_authority", ""),
            publication_date=entry.get("publication_date"),
            effective_date=entry.get("effective_date"),
            retrieved_at=entry.get("retrieved_at"),
            media_type=entry.get("media_type", ""),
            storage_disposition=entry.get("storage_disposition", ""),
            rights_basis=entry.get("rights_basis", ""),
        )
        if authority.source_class != source_class:
            raise ValidationError("Authority and compile source classifications must match.")
        authority_map[entry["stable_id"]] = authority

    scope_items = {
        item.stable_id: item
        for item in scope.items.filter(is_leaf=True).select_related("scope_version")
    }
    obligations = {}
    normalized_seen = {}
    conflict_groups = defaultdict(list)
    duplicate_count = 0
    for candidate in payload.get("obligations", []):
        stable_id = candidate.get("stable_id", "")
        statement = candidate.get("statement", "")
        normalized = normalize_statement(statement)
        if (
            not stable_id
            or not normalized
            or candidate.get("kind") not in RuleObligation.Kind.values
        ):
            _issue(
                compile_version,
                f"structure:{stable_id or 'missing'}",
                "INVALID_STRUCTURE",
                "BLOCKING",
                "Candidate is missing stable identity, statement, or canonical kind.",
            )
            continue
        canonical = canonical_sha256({"kind": candidate["kind"], "statement": normalized})
        if canonical in normalized_seen:
            duplicate_count += 1
            _issue(
                compile_version,
                f"duplicate:{stable_id}",
                "DUPLICATE",
                "WARNING",
                f"Duplicates canonical candidate {normalized_seen[canonical]}.",
            )
            continue
        normalized_seen[canonical] = stable_id
        requested_mappings = candidate.get("scope_item_ids", [])
        mapped = [scope_items[item_id] for item_id in requested_mappings if item_id in scope_items]
        missing_mappings = sorted(set(requested_mappings) - set(scope_items))
        outside_pilot = []
        if policy.coverage_class == CoveragePolicy.CoverageClass.PILOT_ONLY:
            outside_pilot = sorted(set(requested_mappings) - set(policy.target_scope_item_ids))
        jurisdiction = candidate.get("jurisdiction", "")
        excess = candidate.get("classification") == "EXCESS" or not mapped
        blocked = bool(jurisdiction) or bool(missing_mappings) or bool(outside_pilot)
        ambiguous = candidate.get("ambiguous", False)
        decision = "AUTO_APPROVABLE"
        if blocked:
            decision = "BLOCKED"
        elif ambiguous or candidate.get("review_required", False) or policy.requires_human_review:
            decision = "REVIEW_REQUIRED"
        status = "BLOCKED" if blocked else ("EXCESS" if excess else "INCLUDED")
        obligation = RuleObligation.objects.create(
            compile_version=compile_version,
            stable_id=stable_id,
            kind=candidate["kind"],
            normalized_statement=normalized,
            statement=statement.strip(),
            canonical_sha256=canonical,
            compiler_status=status,
            decision=decision,
            inclusion_rationale=candidate.get("inclusion_rationale", "TEST_FIXTURE compiler input"),
            is_core=not excess and not blocked,
            jurisdiction=jurisdiction,
        )
        obligations[stable_id] = obligation
        for item in mapped:
            ObligationScopeMapping.objects.create(
                obligation=obligation,
                scope_item=item,
                mapping_rationale=candidate.get(
                    "mapping_rationale", "TEST_FIXTURE exact official-leaf mapping"
                ),
            )
        primary_count = 0
        for evidence in candidate.get("evidence", []):
            authority = authority_map.get(evidence["authority_id"])
            if authority is None:
                continue
            role = evidence.get("role", "SUBSTANTIVE_SUPPORT")
            if authority.authority_class == "SUBSTANTIVE_PRIMARY" and role == "SUBSTANTIVE_SUPPORT":
                primary_count += 1
            AuthorityEvidence.objects.create(
                obligation=obligation,
                authority=authority,
                role=role,
                locator=evidence["locator"],
                proposition_sha256=canonical_sha256(evidence.get("proposition", statement)),
                supports=evidence.get("supports", True),
            )
        if blocked:
            category = "UNSUPPORTED_JURISDICTION" if jurisdiction else "EXCESS"
            _issue(
                compile_version,
                f"blocked:{stable_id}",
                category,
                "BLOCKING",
                (
                    "Candidate cannot enter national NEXTGEN_CORE."
                    if jurisdiction
                    else "Candidate mapping falls outside the bounded PILOT_ONLY policy."
                ),
                obligation=obligation,
            )
        elif excess:
            _issue(
                compile_version,
                f"excess:{stable_id}",
                "EXCESS",
                "WARNING",
                "Candidate has no justified active official-perimeter mapping.",
                obligation=obligation,
            )
        if ambiguous:
            _issue(
                compile_version,
                f"ambiguity:{stable_id}",
                "AMBIGUITY",
                "BLOCKING",
                "Candidate mapping or normalization requires review.",
                obligation=obligation,
            )
        if policy.requires_primary_authority and primary_count == 0 and status == "INCLUDED":
            obligation.decision = "REVIEW_REQUIRED"
            obligation.save(update_fields=("decision",))
            _issue(
                compile_version,
                f"provenance:{stable_id}",
                "UNSUPPORTED_PROVENANCE",
                "BLOCKING",
                "Included candidate lacks structured substantive primary authority.",
                obligation=obligation,
            )
        group = candidate.get("conflict_group")
        if group:
            conflict_groups[group].append(obligation)

    for group, members in conflict_groups.items():
        if len({member.normalized_statement for member in members}) > 1:
            _issue(
                compile_version,
                f"conflict:{group}",
                "CONFLICT",
                "BLOCKING",
                "Candidate obligations materially disagree and require human reconciliation.",
                obligation=members[0],
            )
            for member in members:
                member.decision = "REVIEW_REQUIRED"
                member.reconciliation_status = "CONFLICT"
                member.save(update_fields=("decision", "reconciliation_status"))

    for edge in payload.get("relationships", []):
        source = obligations.get(edge.get("source_id"))
        target = obligations.get(edge.get("target_id"))
        kind = edge.get("kind")
        valid = (
            source
            and target
            and source != target
            and kind in RELATIONSHIP_TARGET_KIND
            and target.kind == RELATIONSHIP_TARGET_KIND[kind]
            and not _would_cycle(source, target)
        )
        if not valid:
            _issue(
                compile_version,
                f"relationship:{edge.get('source_id')}:{kind}:{edge.get('target_id')}",
                "INVALID_STRUCTURE",
                "BLOCKING",
                "Relationship is missing, circular, or semantically invalid.",
            )
            continue
        ObligationRelationship.objects.create(
            source=source,
            target=target,
            kind=kind,
            ordering=edge.get("ordering", 0),
        )

    compile_version.canonical_sha256 = canonical_sha256(_compile_canonical(compile_version))
    compile_version.compile_report = {
        "valid": not compile_version.issues.filter(severity="BLOCKING").exists(),
        "candidate_count": len(payload.get("obligations", [])),
        "obligation_count": compile_version.obligations.count(),
        "duplicate_count": duplicate_count,
        "issue_count": compile_version.issues.count(),
    }
    compile_version.status = CurriculumCompileVersion.Status.COMPILED
    compile_version.compiled_at = timezone.now()
    compile_version.save()
    return compile_version, True


@transaction.atomic
def reconcile_curriculum(compile_id):
    compile_version = CurriculumCompileVersion.objects.select_for_update().get(pk=compile_id)
    if compile_version.status not in (
        CurriculumCompileVersion.Status.COMPILED,
        CurriculumCompileVersion.Status.RECONCILED,
    ):
        raise ValidationError("Only compiled curriculum may be reconciled.")
    policy = compile_version.coverage_policy
    leaves_query = compile_version.official_scope_version.items.filter(
        is_leaf=True, perimeter="TESTABLE"
    )
    if policy.coverage_class == CoveragePolicy.CoverageClass.PILOT_ONLY:
        leaves_query = leaves_query.filter(stable_id__in=policy.target_scope_item_ids)
        found = set(leaves_query.values_list("stable_id", flat=True))
        missing = sorted(set(policy.target_scope_item_ids) - found)
        if missing:
            raise ValidationError({"unknown_pilot_scope_items": missing})
    leaves = list(leaves_query.order_by("stable_id"))
    covered = 0
    sufficient = 0
    leaf_results = []
    for leaf in leaves:
        obligations = list(
            RuleObligation.objects.filter(
                compile_version=compile_version,
                scope_items=leaf,
                compiler_status="INCLUDED",
                is_core=True,
            ).distinct()
        )
        qualifying = [
            obligation
            for obligation in obligations
            if obligation.kind in policy.allowed_obligation_kinds
            and (
                not policy.requires_primary_authority
                or obligation.authority_evidence.filter(
                    authority__authority_class="SUBSTANTIVE_PRIMARY",
                    role="SUBSTANTIVE_SUPPORT",
                    supports=True,
                ).exists()
            )
        ]
        if obligations:
            covered += 1
        meets = len(qualifying) >= policy.minimum_obligations_per_leaf
        if meets:
            sufficient += 1
        else:
            _issue(
                compile_version,
                f"omission:{leaf.stable_id}",
                "OMISSION",
                "BLOCKING",
                "Official testable leaf does not meet the fixture coverage policy.",
                scope_item=leaf,
            )
        leaf_results.append(
            {
                "scope_item_id": leaf.stable_id,
                "mapped_count": len(obligations),
                "qualifying_count": len(qualifying),
                "sufficient": meets,
            }
        )
    open_issues = compile_version.issues.filter(status="OPEN")
    counts = Counter(open_issues.values_list("category", flat=True))
    report = {
        "coverage_class": policy.coverage_class,
        "national_complete": False,
        "target_scope_item_ids": sorted(policy.target_scope_item_ids),
        "total_official_leaves": len(leaves),
        "total_active_scope_leaves": compile_version.official_scope_version.items.filter(
            is_leaf=True, perimeter="TESTABLE"
        ).count(),
        "leaves_with_obligations": covered,
        "leaves_sufficiently_covered": sufficient,
        "blocking_omission_count": counts["OMISSION"],
        "excess_count": counts["EXCESS"],
        "unresolved_conflict_count": counts["CONFLICT"],
        "unresolved_ambiguity_count": counts["AMBIGUITY"],
        "provenance_deficient_count": counts["UNSUPPORTED_PROVENANCE"],
        "blocking_issue_count": open_issues.filter(severity="BLOCKING").count(),
        "warning_issue_count": open_issues.filter(severity="WARNING").count(),
        "informational_issue_count": open_issues.filter(severity="INFO").count(),
        "leaf_results": leaf_results,
    }
    compile_version.reconciliation_report = report
    compile_version.status = CurriculumCompileVersion.Status.RECONCILED
    compile_version.reconciled_at = timezone.now()
    compile_version.save()
    return compile_version, report


@transaction.atomic
def resolve_issue(issue_id, *, reviewer, resolution, rationale, changes_canonical_truth=False):
    if not reviewer.is_staff:
        raise PermissionDenied("Curriculum review requires staff authority.")
    issue = ReconciliationIssue.objects.select_for_update().get(pk=issue_id)
    if issue.compile_version.status in (
        CurriculumCompileVersion.Status.CERTIFIED,
        CurriculumCompileVersion.Status.SUPERSEDED,
    ):
        raise ValidationError("Certified historical issues cannot be changed.")
    if issue.status == ReconciliationIssue.Status.RESOLVED:
        return issue.review_resolution
    review = ReviewResolution.objects.create(
        issue=issue,
        reviewer=reviewer,
        resolution=resolution,
        rationale=rationale,
        changes_canonical_truth=changes_canonical_truth,
    )
    if resolution in (ReviewResolution.Resolution.ACCEPT, ReviewResolution.Resolution.REJECT):
        issue.status = ReconciliationIssue.Status.RESOLVED
        issue.save(update_fields=("status",))
    return review


@transaction.atomic
def record_obligation_review(obligation_id, *, reviewer, resolution, rationale, authority_reviewed):
    if not reviewer.is_staff:
        raise PermissionDenied("Production obligation review requires staff authority.")
    obligation = RuleObligation.objects.select_for_update().get(pk=obligation_id)
    if obligation.compile_version.status in (
        CurriculumCompileVersion.Status.CERTIFIED,
        CurriculumCompileVersion.Status.SUPERSEDED,
    ):
        raise ValidationError("Certified historical obligations cannot be reviewed again.")
    existing = ObligationHumanReview.objects.filter(obligation=obligation).first()
    if existing:
        return existing, False
    review = ObligationHumanReview.objects.create(
        obligation=obligation,
        reviewer=reviewer,
        resolution=resolution,
        rationale=rationale,
        authority_reviewed=authority_reviewed,
    )
    return review, True


@transaction.atomic
def certify_curriculum(compile_id, *, allow_test_fixture=False):
    compile_version = CurriculumCompileVersion.objects.select_for_update().get(pk=compile_id)
    if (
        compile_version.source_class == AuthoritySource.SourceClass.TEST_FIXTURE
        and not allow_test_fixture
    ):
        raise ValidationError("TEST_FIXTURE curriculum cannot certify as production truth.")
    if compile_version.status != CurriculumCompileVersion.Status.RECONCILED:
        raise ValidationError("Curriculum must be explicitly reconciled before certification.")
    expected_checksum = canonical_sha256(_compile_canonical(compile_version))
    if expected_checksum != compile_version.canonical_sha256:
        raise ValidationError("Canonical curriculum changed after compilation.")
    blocking = compile_version.issues.filter(severity="BLOCKING", status="OPEN")
    if blocking.exists():
        raise ValidationError(
            {"blocking_issues": list(blocking.values_list("stable_id", flat=True))}
        )
    now = timezone.now()
    coverage = compile_version.reconciliation_report
    if coverage.get("blocking_issue_count") != 0:
        raise ValidationError("Reconcile again after review resolutions before certification.")
    if compile_version.coverage_policy.requires_human_review:
        missing_reviews = []
        rejected_reviews = []
        for obligation in compile_version.obligations.filter(compiler_status="INCLUDED"):
            review = getattr(obligation, "human_review", None)
            if review is None or not review.authority_reviewed:
                missing_reviews.append(obligation.stable_id)
            elif review.resolution != ObligationHumanReview.Resolution.APPROVE:
                rejected_reviews.append(obligation.stable_id)
        if missing_reviews or rejected_reviews:
            raise ValidationError(
                {
                    "human_review_required": sorted(missing_reviews),
                    "human_review_rejected": sorted(rejected_reviews),
                }
            )
    review_evidence = []
    for issue in compile_version.issues.select_related("review_resolution").order_by("stable_id"):
        review = issue.review_resolution if hasattr(issue, "review_resolution") else None
        review_evidence.append(
            {
                "issue": issue.stable_id,
                "category": issue.category,
                "status": issue.status,
                "resolution": review.resolution if review else None,
                "rationale": review.rationale if review else None,
                "changes_canonical_truth": review.changes_canonical_truth if review else None,
            }
        )
    snapshot_payload = {
        "compile_sha256": compile_version.canonical_sha256,
        "scope_sha256": compile_version.official_scope_version.normalized_sha256,
        "policy_sha256": compile_version.coverage_policy.canonical_sha256,
        "compiler_schema_version": compile_version.compiler_schema_version,
        "source_class": compile_version.source_class,
        "coverage": coverage,
        "review_evidence": review_evidence,
        "coverage_class": compile_version.coverage_class,
        "national_complete": False,
        "obligation_reviews": sorted(
            [
                {
                    "obligation": review.obligation.stable_id,
                    "reviewer": str(review.reviewer_id),
                    "resolution": review.resolution,
                    "authority_reviewed": review.authority_reviewed,
                    "rationale": review.rationale,
                }
                for review in ObligationHumanReview.objects.filter(
                    obligation__compile_version=compile_version
                ).select_related("obligation")
            ],
            key=lambda value: value["obligation"],
        ),
    }
    authority_provenance_sha256 = canonical_sha256(
        sorted(
            [
                [authority.stable_id, authority.source_version, authority.content_sha256]
                for authority in AuthoritySource.objects.filter(
                    authorityevidence__obligation__compile_version=compile_version
                ).distinct()
            ]
        )
    )
    snapshot = CoverageReleaseSnapshot.objects.create(
        compile_version=compile_version,
        official_scope_version=compile_version.official_scope_version,
        compiler_schema_version=compile_version.compiler_schema_version,
        source_class=compile_version.source_class,
        coverage_class=compile_version.coverage_class,
        national_complete=False,
        authority_provenance_sha256=authority_provenance_sha256,
        human_review_status=(
            "APPROVED" if compile_version.coverage_policy.requires_human_review else "NOT_REQUIRED"
        ),
        obligation_count=compile_version.obligations.filter(compiler_status="INCLUDED").count(),
        leaf_count=coverage["total_official_leaves"],
        covered_leaf_count=coverage["leaves_sufficiently_covered"],
        blocking_issue_count=coverage["blocking_issue_count"],
        warning_issue_count=coverage["warning_issue_count"],
        coverage_results=coverage,
        certification_sha256=canonical_sha256(snapshot_payload),
        certified_at=now,
    )
    previous = compile_version.supersedes
    if previous:
        if previous.status != CurriculumCompileVersion.Status.CERTIFIED:
            raise ValidationError("Superseded curriculum must be a certified historical version.")
        previous.status = CurriculumCompileVersion.Status.SUPERSEDED
        previous.save(update_fields=("status",))
    compile_version.status = CurriculumCompileVersion.Status.CERTIFIED
    compile_version.certified_at = now
    compile_version.save()
    return snapshot


def compare_scope_drift(old_scope, new_scope, *, old_compile=None):
    def keyed(scope):
        return {
            item.stable_id: canonical_sha256(
                {
                    "label": item.official_label,
                    "text": item.official_text,
                    "perimeter": item.perimeter,
                    "is_leaf": item.is_leaf,
                }
            )
            for item in scope.items.filter(is_leaf=True)
        }

    old = keyed(old_scope)
    new = keyed(new_scope)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(key for key in set(old) & set(new) if old[key] != new[key])
    impacted_ids = set(removed) | set(changed)
    impacted = []
    unaffected = []
    if old_compile:
        for obligation in old_compile.obligations.order_by("stable_id"):
            mapped = set(obligation.scope_items.values_list("stable_id", flat=True))
            (impacted if mapped & impacted_ids else unaffected).append(obligation.stable_id)
    return {
        "old_scope": old_scope.version_identifier,
        "new_scope": new_scope.version_identifier,
        "added_leaves": added,
        "removed_leaves": removed,
        "changed_leaves": changed,
        "potentially_impacted_obligations": impacted,
        "unaffected_obligations": unaffected,
        "requires_re_evaluation": bool(added or removed or changed),
    }


def compile_result(compile_version):
    issues = compile_version.issues.filter(status="OPEN")
    counts = Counter(issues.values_list("category", flat=True))
    return {
        "scope_version": compile_version.official_scope_version.version_identifier,
        "compiler_version": compile_version.compiler_schema_version,
        "curriculum_version": compile_version.version_identifier,
        "status": compile_version.status,
        "obligation_count": compile_version.obligations.count(),
        "omission_count": counts["OMISSION"],
        "excess_count": counts["EXCESS"],
        "conflict_count": counts["CONFLICT"],
        "ambiguity_count": counts["AMBIGUITY"],
        "certification_eligible": not issues.filter(severity="BLOCKING").exists(),
        "canonical_sha256": compile_version.canonical_sha256,
    }
