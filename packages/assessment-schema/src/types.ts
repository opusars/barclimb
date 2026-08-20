export const presentationSchemaVersion = "assessment_ui.v1" as const;
export const workspaceSchemaVersion = "assessment_workspace.v1" as const;
export const portableTextSchemaVersion = "barclimb_text.v1" as const;

export const assessmentFamilies = [
  "STANDALONE_MCQ",
  "IQS",
  "PT_STANDARD",
  "PT_LEGAL_RESEARCH",
] as const;
export type AssessmentFamily = (typeof assessmentFamilies)[number];

export const responseTypes = [
  "MCQ_SINGLE",
  "MCQ_MULTI",
  "SHORT_CONSTRUCTED",
  "MEDIUM_CONSTRUCTED",
  "LONG_CONSTRUCTED",
  "DRAFT",
  "EDIT",
  "COUNSEL",
] as const;
export type ResponseType = (typeof responseTypes)[number];

export const resourceTypes = [
  "TEXT",
  "EMAIL",
  "CASE",
  "STATUTE",
  "CONTRACT",
  "PLEADING",
  "POLICE_REPORT",
  "TRANSCRIPT",
  "MEMO",
  "TABLE",
  "IMAGE",
  "ATTACHMENT",
] as const;
export type ResourceType = (typeof resourceTypes)[number];

export const layoutModes = [
  "FOCUSED",
  "INTEGRATED",
  "WORKSPACE",
  "RESEARCH_WORKSPACE",
] as const;
export type LayoutMode = (typeof layoutModes)[number];

export const navigationModes = ["FREE", "LINEAR", "PROGRESSIVE"] as const;
export type NavigationMode = (typeof navigationModes)[number];

export const rendererComponentTypes = [
  "SINGLE_SELECT_QUESTION",
  "LONG_RESPONSE_EDITOR",
] as const;
export type RendererComponentType = (typeof rendererComponentTypes)[number];

export const toolCapabilities = [
  "QUESTION_NAVIGATOR",
  "MARK_FOR_REVIEW",
  "COPY_PASTE",
  "BASIC_FORMATTING",
  "RESOURCE_TABS",
] as const;
export type ToolCapability = (typeof toolCapabilities)[number];

export type AssessmentResource = Readonly<{
  id: string;
  type: ResourceType;
  title: string;
  content: string;
  accessibilityLabel: string;
}>;

export type AnswerChoice = Readonly<{
  id: string;
  label: string;
  text: string;
}>;

export type SingleSelectUnit = Readonly<{
  id: string;
  component: "SINGLE_SELECT_QUESTION";
  responseType: "MCQ_SINGLE";
  prompt: string;
  accessibilityLabel: string;
  choices: readonly AnswerChoice[];
  resourceIds: readonly string[];
}>;

export type LongResponseUnit = Readonly<{
  id: string;
  component: "LONG_RESPONSE_EDITOR";
  responseType:
    | "SHORT_CONSTRUCTED"
    | "MEDIUM_CONSTRUCTED"
    | "LONG_CONSTRUCTED"
    | "DRAFT"
    | "EDIT"
    | "COUNSEL";
  prompt: string;
  accessibilityLabel: string;
  resourceIds: readonly string[];
}>;

export type AssessmentUnit = SingleSelectUnit | LongResponseUnit;

export type AssessmentPresentation = Readonly<{
  presentationSchemaVersion: typeof presentationSchemaVersion;
  assessmentId: string;
  assessmentVersionId: string;
  title: string;
  family: AssessmentFamily;
  layout: LayoutMode;
  navigationMode: NavigationMode;
  capabilities: readonly ToolCapability[];
  resources: readonly AssessmentResource[];
  units: readonly AssessmentUnit[];
  presentationMetadata: Readonly<
    | {
        contentClassification: "TEST_FIXTURE";
        fixtureUse: "DEVELOPMENT_ONLY";
        syntheticContent: true;
        publicationEligibility: "INELIGIBLE";
        rendererContract: "REGISTERED_COMPONENTS_ONLY";
        recommendedViewport: "PHONE_TO_DESKTOP";
      }
    | {
        contentClassification: "ASSESSMENT_VERSION";
        fixtureUse: null;
        syntheticContent: boolean;
        publicationEligibility: "CONTROLLED_BY_SERVER";
        rendererContract: "REGISTERED_COMPONENTS_ONLY";
        recommendedViewport: "PHONE_TO_DESKTOP";
      }
  >;
}>;

export const formattingMarks = ["BOLD", "ITALIC", "UNDERLINE"] as const;
export type FormattingMark = (typeof formattingMarks)[number];
export const blockStyles = [
  "PARAGRAPH",
  "BULLETED_LIST",
  "NUMBERED_LIST",
] as const;
export type BlockStyle = (typeof blockStyles)[number];

export type PortableTextMark = Readonly<{
  type: FormattingMark;
  start: number;
  end: number;
}>;

export type PortableTextDocument = Readonly<{
  schemaVersion: typeof portableTextSchemaVersion;
  text: string;
  marks: readonly PortableTextMark[];
  blockStyle: BlockStyle;
  indentLevel: number;
}>;

export type ChoiceResponse = Readonly<{
  type: "CHOICE";
  selectedChoiceIds: readonly string[];
}>;

export type TextResponse = Readonly<{
  type: "TEXT";
  document: PortableTextDocument;
}>;

export type WorkspaceResponse = ChoiceResponse | TextResponse;

export const saveStatuses = [
  "UNSAVED_LOCAL",
  "SAVE_PENDING",
  "SAVED",
  "RECOVERABLE_FAILURE",
  "RESTORED",
] as const;
export type SaveStatus = (typeof saveStatuses)[number];

export type WorkspaceState = Readonly<{
  schemaVersion: typeof workspaceSchemaVersion;
  assessmentVersionId: string;
  currentUnitId: string;
  currentResourceId: string | null;
  currentView: "QUESTION" | "RESOURCES" | "RESPONSE";
  responses: Readonly<Record<string, WorkspaceResponse>>;
  markedForReviewUnitIds: readonly string[];
  persistence: Readonly<{
    status: SaveStatus;
    localRevision: number;
    savedRevision: number;
    lastSavedAt: string | null;
    failureCode: "INTERRUPTED_WRITE" | null;
  }>;
}>;

export type SchemaIssueCode =
  | "INVALID_SHAPE"
  | "INVALID_ENUM"
  | "DUPLICATE_ID"
  | "MISSING_REFERENCE"
  | "UNSUPPORTED_COMPONENT"
  | "INVALID_COMPONENT_RESPONSE"
  | "INVALID_FIXTURE_CLASSIFICATION";

export type SchemaIssue = Readonly<{
  code: SchemaIssueCode;
  path: string;
  message: string;
}>;

export type ValidationResult<T> =
  | Readonly<{ ok: true; value: T }>
  | Readonly<{ ok: false; issues: readonly SchemaIssue[] }>;

export type UnsupportedComponentError = Readonly<{
  code: "UNSUPPORTED_COMPONENT";
  component: string;
  message: string;
}>;
