import { isNonEmptyString } from "@barclimb/validation";
import {
  assessmentFamilies,
  blockStyles,
  formattingMarks,
  layoutModes,
  navigationModes,
  portableTextSchemaVersion,
  presentationSchemaVersion,
  rendererComponentTypes,
  resourceTypes,
  responseTypes,
  saveStatuses,
  toolCapabilities,
  workspaceSchemaVersion,
  type AssessmentPresentation,
  type AssessmentUnit,
  type PortableTextDocument,
  type SchemaIssue,
  type ValidationResult,
  type WorkspaceResponse,
  type WorkspaceState,
} from "./types";

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const isEnumValue = <T extends string>(
  values: readonly T[],
  value: unknown,
): value is T => typeof value === "string" && values.includes(value as T);

const issue = (
  code: SchemaIssue["code"],
  path: string,
  message: string,
): SchemaIssue => ({ code, path, message });

function parseUnit(
  value: unknown,
  path: string,
  resourceIds: ReadonlySet<string>,
): ValidationResult<AssessmentUnit> {
  if (!isRecord(value))
    return {
      ok: false,
      issues: [issue("INVALID_SHAPE", path, "Unit must be an object.")],
    };
  if (!isNonEmptyString(value.id))
    return {
      ok: false,
      issues: [issue("INVALID_SHAPE", `${path}.id`, "Unit id is required.")],
    };
  if (!isEnumValue(rendererComponentTypes, value.component))
    return {
      ok: false,
      issues: [
        issue(
          "UNSUPPORTED_COMPONENT",
          `${path}.component`,
          `Unsupported assessment component: ${String(value.component)}.`,
        ),
      ],
    };
  if (!isEnumValue(responseTypes, value.responseType))
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_ENUM",
          `${path}.responseType`,
          "Response type is not registered.",
        ),
      ],
    };
  if (
    !isNonEmptyString(value.prompt) ||
    !isNonEmptyString(value.accessibilityLabel)
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_SHAPE",
          path,
          "Prompt and accessibility label are required.",
        ),
      ],
    };
  if (
    !Array.isArray(value.resourceIds) ||
    !value.resourceIds.every(isNonEmptyString)
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_SHAPE",
          `${path}.resourceIds`,
          "Resource references must be string ids.",
        ),
      ],
    };
  const missingResource = value.resourceIds.find((id) => !resourceIds.has(id));
  if (missingResource)
    return {
      ok: false,
      issues: [
        issue(
          "MISSING_REFERENCE",
          `${path}.resourceIds`,
          `Resource ${missingResource} does not exist.`,
        ),
      ],
    };
  if (value.component === "SINGLE_SELECT_QUESTION") {
    if (value.responseType !== "MCQ_SINGLE")
      return {
        ok: false,
        issues: [
          issue(
            "INVALID_COMPONENT_RESPONSE",
            `${path}.responseType`,
            "Single-select components require MCQ_SINGLE.",
          ),
        ],
      };
    if (!Array.isArray(value.choices) || value.choices.length !== 4)
      return {
        ok: false,
        issues: [
          issue(
            "INVALID_SHAPE",
            `${path}.choices`,
            "M1.5 MCQ_SINGLE fixtures require four choices.",
          ),
        ],
      };
    const choiceIds = new Set<string>();
    for (const [index, choice] of value.choices.entries()) {
      if (
        !isRecord(choice) ||
        !isNonEmptyString(choice.id) ||
        !isNonEmptyString(choice.label) ||
        !isNonEmptyString(choice.text)
      )
        return {
          ok: false,
          issues: [
            issue(
              "INVALID_SHAPE",
              `${path}.choices.${index}`,
              "Each choice requires id, label, and text.",
            ),
          ],
        };
      if (choiceIds.has(choice.id))
        return {
          ok: false,
          issues: [
            issue(
              "DUPLICATE_ID",
              `${path}.choices.${index}.id`,
              `Duplicate choice id ${choice.id}.`,
            ),
          ],
        };
      choiceIds.add(choice.id);
    }
    return { ok: true, value: value as unknown as AssessmentUnit };
  }
  if (value.responseType === "MCQ_SINGLE" || value.responseType === "MCQ_MULTI")
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_COMPONENT_RESPONSE",
          `${path}.responseType`,
          "Long-response components require a constructed response type.",
        ),
      ],
    };
  return { ok: true, value: value as unknown as AssessmentUnit };
}

export function validateAssessmentPresentation(
  value: unknown,
): ValidationResult<AssessmentPresentation> {
  if (!isRecord(value))
    return {
      ok: false,
      issues: [issue("INVALID_SHAPE", "$", "Presentation must be an object.")],
    };
  if (value.presentationSchemaVersion !== presentationSchemaVersion)
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_ENUM",
          "presentationSchemaVersion",
          "Unsupported presentation schema version.",
        ),
      ],
    };
  if (
    !isNonEmptyString(value.assessmentId) ||
    !isNonEmptyString(value.assessmentVersionId) ||
    !isNonEmptyString(value.title)
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_SHAPE",
          "$",
          "Assessment identity, version identity, and title are required.",
        ),
      ],
    };
  if (
    !isEnumValue(assessmentFamilies, value.family) ||
    !isEnumValue(layoutModes, value.layout) ||
    !isEnumValue(navigationModes, value.navigationMode)
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_ENUM",
          "$",
          "Family, layout, or navigation mode is not registered.",
        ),
      ],
    };
  if (
    !Array.isArray(value.capabilities) ||
    !value.capabilities.every((item) => isEnumValue(toolCapabilities, item))
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_ENUM",
          "capabilities",
          "Capabilities must all be registered.",
        ),
      ],
    };
  if (!Array.isArray(value.resources) || !Array.isArray(value.units))
    return {
      ok: false,
      issues: [
        issue("INVALID_SHAPE", "$", "Resources and units must be arrays."),
      ],
    };
  const resourceIds = new Set<string>();
  for (const [index, resource] of value.resources.entries()) {
    if (
      !isRecord(resource) ||
      !isNonEmptyString(resource.id) ||
      !isEnumValue(resourceTypes, resource.type) ||
      !isNonEmptyString(resource.title) ||
      !isNonEmptyString(resource.content) ||
      !isNonEmptyString(resource.accessibilityLabel)
    )
      return {
        ok: false,
        issues: [
          issue(
            "INVALID_SHAPE",
            `resources.${index}`,
            "Resource fields are incomplete or unsupported.",
          ),
        ],
      };
    if (resourceIds.has(resource.id))
      return {
        ok: false,
        issues: [
          issue(
            "DUPLICATE_ID",
            `resources.${index}.id`,
            `Duplicate resource id ${resource.id}.`,
          ),
        ],
      };
    resourceIds.add(resource.id);
  }
  const units: AssessmentUnit[] = [];
  const unitIds = new Set<string>();
  for (const [index, unit] of value.units.entries()) {
    const parsed = parseUnit(unit, `units.${index}`, resourceIds);
    if (!parsed.ok) return parsed;
    if (unitIds.has(parsed.value.id))
      return {
        ok: false,
        issues: [
          issue(
            "DUPLICATE_ID",
            `units.${index}.id`,
            `Duplicate unit id ${parsed.value.id}.`,
          ),
        ],
      };
    unitIds.add(parsed.value.id);
    units.push(parsed.value);
  }
  if (units.length === 0)
    return {
      ok: false,
      issues: [
        issue("INVALID_SHAPE", "units", "At least one unit is required."),
      ],
    };
  if (
    !isRecord(value.presentationMetadata) ||
    value.presentationMetadata.rendererContract !==
      "REGISTERED_COMPONENTS_ONLY" ||
    value.presentationMetadata.recommendedViewport !== "PHONE_TO_DESKTOP"
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_FIXTURE_CLASSIFICATION",
          "presentationMetadata",
          "Presentation metadata does not identify a registered renderer contract.",
        ),
      ],
    };
  const fixtureMetadataValid =
    value.presentationMetadata.contentClassification === "TEST_FIXTURE" &&
    value.presentationMetadata.fixtureUse === "DEVELOPMENT_ONLY" &&
    value.presentationMetadata.syntheticContent === true &&
    value.presentationMetadata.publicationEligibility === "INELIGIBLE";
  const serverMetadataValid =
    value.presentationMetadata.contentClassification === "ASSESSMENT_VERSION" &&
    value.presentationMetadata.fixtureUse === null &&
    typeof value.presentationMetadata.syntheticContent === "boolean" &&
    value.presentationMetadata.publicationEligibility ===
      "CONTROLLED_BY_SERVER";
  if (!fixtureMetadataValid && !serverMetadataValid)
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_FIXTURE_CLASSIFICATION",
          "presentationMetadata",
          "Content classification and publication eligibility are inconsistent.",
        ),
      ],
    };
  return {
    ok: true,
    value: { ...value, units } as unknown as AssessmentPresentation,
  };
}

export class AssessmentSchemaError extends Error {
  readonly issues: readonly SchemaIssue[];

  constructor(issues: readonly SchemaIssue[]) {
    super(issues.map((item) => `${item.path}: ${item.message}`).join("; "));
    this.name = "AssessmentSchemaError";
    this.issues = issues;
  }
}

export function assertValidAssessmentPresentation(
  value: unknown,
): AssessmentPresentation {
  const result = validateAssessmentPresentation(value);
  if (!result.ok) throw new AssessmentSchemaError(result.issues);
  return result.value;
}

function isPortableDocument(value: unknown): value is PortableTextDocument {
  if (
    !isRecord(value) ||
    value.schemaVersion !== portableTextSchemaVersion ||
    typeof value.text !== "string" ||
    !Array.isArray(value.marks) ||
    !isEnumValue(blockStyles, value.blockStyle) ||
    !Number.isInteger(value.indentLevel) ||
    Number(value.indentLevel) < 0 ||
    Number(value.indentLevel) > 3
  )
    return false;
  const textLength = value.text.length;
  return value.marks.every(
    (mark) =>
      isRecord(mark) &&
      isEnumValue(formattingMarks, mark.type) &&
      Number.isInteger(mark.start) &&
      Number.isInteger(mark.end) &&
      Number(mark.start) >= 0 &&
      Number(mark.end) > Number(mark.start) &&
      Number(mark.end) <= textLength,
  );
}

function isWorkspaceResponse(value: unknown): value is WorkspaceResponse {
  if (!isRecord(value)) return false;
  if (value.type === "CHOICE")
    return (
      Array.isArray(value.selectedChoiceIds) &&
      value.selectedChoiceIds.every(isNonEmptyString)
    );
  return value.type === "TEXT" && isPortableDocument(value.document);
}

export function validateWorkspaceState(
  value: unknown,
  presentation: AssessmentPresentation,
): ValidationResult<WorkspaceState> {
  if (
    !isRecord(value) ||
    value.schemaVersion !== workspaceSchemaVersion ||
    value.assessmentVersionId !== presentation.assessmentVersionId ||
    !isNonEmptyString(value.currentUnitId) ||
    !presentation.units.some((unit) => unit.id === value.currentUnitId) ||
    (value.currentResourceId !== null &&
      (!isNonEmptyString(value.currentResourceId) ||
        !presentation.resources.some(
          (resource) => resource.id === value.currentResourceId,
        ))) ||
    !["QUESTION", "RESOURCES", "RESPONSE"].includes(
      String(value.currentView),
    ) ||
    !isRecord(value.responses) ||
    !Object.values(value.responses).every(isWorkspaceResponse) ||
    !Array.isArray(value.markedForReviewUnitIds) ||
    !value.markedForReviewUnitIds.every((id) =>
      presentation.units.some((unit) => unit.id === id),
    ) ||
    !isRecord(value.persistence) ||
    !isEnumValue(saveStatuses, value.persistence.status) ||
    !Number.isInteger(value.persistence.localRevision) ||
    !Number.isInteger(value.persistence.savedRevision) ||
    (value.persistence.lastSavedAt !== null &&
      !isNonEmptyString(value.persistence.lastSavedAt)) ||
    (value.persistence.failureCode !== null &&
      value.persistence.failureCode !== "INTERRUPTED_WRITE")
  )
    return {
      ok: false,
      issues: [
        issue(
          "INVALID_SHAPE",
          "$",
          "Workspace state does not match the portable M1.5 contract.",
        ),
      ],
    };
  return { ok: true, value: value as unknown as WorkspaceState };
}
