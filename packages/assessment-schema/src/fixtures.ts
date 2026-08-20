import {
  presentationSchemaVersion,
  type AssessmentPresentation,
} from "./types";
import { assertValidAssessmentPresentation } from "./validation";

const fixtureMetadata = {
  contentClassification: "TEST_FIXTURE",
  fixtureUse: "DEVELOPMENT_ONLY",
  syntheticContent: true,
  publicationEligibility: "INELIGIBLE",
  rendererContract: "REGISTERED_COMPONENTS_ONLY",
  recommendedViewport: "PHONE_TO_DESKTOP",
} as const;

const syntheticNotice =
  "Synthetic M1.5 exercise. All names, rules, authorities, and events are fictional.";

const rawFixtures = [
  {
    presentationSchemaVersion,
    assessmentId: "fixture-mcq",
    assessmentVersionId: "fixture-mcq-v1",
    title: "Portable MCQ proof",
    family: "STANDALONE_MCQ",
    layout: "FOCUSED",
    navigationMode: "FREE",
    capabilities: ["QUESTION_NAVIGATOR", "MARK_FOR_REVIEW"],
    resources: [],
    units: [
      {
        id: "mcq-unit-1",
        component: "SINGLE_SELECT_QUESTION",
        responseType: "MCQ_SINGLE",
        accessibilityLabel: "Synthetic multiple-choice question",
        prompt: `${syntheticNotice} Under fictional Northlake Rule 7, a filing is timely when delivered before the office clock reaches noon. A courier delivers it at 11:55 a.m. Which statement follows from the supplied fictional rule?`,
        resourceIds: [],
        choices: [
          { id: "mcq-a", label: "A", text: "The filing is timely." },
          { id: "mcq-b", label: "B", text: "The filing is late." },
          { id: "mcq-c", label: "C", text: "Timing cannot be evaluated." },
          { id: "mcq-d", label: "D", text: "The filing creates a new rule." },
        ],
      },
    ],
    presentationMetadata: fixtureMetadata,
  },
  {
    presentationSchemaVersion,
    assessmentId: "fixture-iqs",
    assessmentVersionId: "fixture-iqs-v1",
    title: "Portable IQS resource proof",
    family: "IQS",
    layout: "INTEGRATED",
    navigationMode: "FREE",
    capabilities: ["QUESTION_NAVIGATOR", "MARK_FOR_REVIEW", "RESOURCE_TABS"],
    resources: [
      {
        id: "iqs-document",
        type: "TEXT",
        title: "Intake note",
        accessibilityLabel: "Synthetic intake note resource",
        content: `${syntheticNotice} The package reached the Northlake office at 11:55 a.m.`,
      },
      {
        id: "iqs-email",
        type: "EMAIL",
        title: "Office email",
        accessibilityLabel: "Synthetic office email resource",
        content: `${syntheticNotice} The office clock was checked against the lobby clock that morning.`,
      },
      {
        id: "iqs-authority",
        type: "STATUTE",
        title: "Northlake Rule 7",
        accessibilityLabel: "Synthetic statute-style resource",
        content: `${syntheticNotice} A filing delivered before noon is timely. This is not real law.`,
      },
    ],
    units: [
      {
        id: "iqs-unit-1",
        component: "SINGLE_SELECT_QUESTION",
        responseType: "MCQ_SINGLE",
        accessibilityLabel: "Synthetic integrated question",
        prompt:
          "Which resource most directly states the fictional timing rule?",
        resourceIds: ["iqs-document", "iqs-email", "iqs-authority"],
        choices: [
          { id: "iqs-a", label: "A", text: "The intake note" },
          { id: "iqs-b", label: "B", text: "The office email" },
          { id: "iqs-c", label: "C", text: "Northlake Rule 7" },
          { id: "iqs-d", label: "D", text: "None of the resources" },
        ],
      },
    ],
    presentationMetadata: fixtureMetadata,
  },
  {
    presentationSchemaVersion,
    assessmentId: "fixture-pt",
    assessmentVersionId: "fixture-pt-v1",
    title: "Portable PT workspace proof",
    family: "PT_STANDARD",
    layout: "WORKSPACE",
    navigationMode: "FREE",
    capabilities: [
      "QUESTION_NAVIGATOR",
      "MARK_FOR_REVIEW",
      "COPY_PASTE",
      "BASIC_FORMATTING",
      "RESOURCE_TABS",
    ],
    resources: [
      {
        id: "pt-file",
        type: "MEMO",
        title: "Synthetic client file",
        accessibilityLabel: "Synthetic client file resource",
        content: `${syntheticNotice} Prepare a short internal memo using only the supplied fictional record.`,
      },
      {
        id: "pt-library",
        type: "CASE",
        title: "Northlake v. Rowan",
        accessibilityLabel: "Synthetic case-style resource",
        content: `${syntheticNotice} Northlake v. Rowan is invented solely to test presentation and has no legal authority.`,
      },
    ],
    units: [
      {
        id: "pt-unit-1",
        component: "LONG_RESPONSE_EDITOR",
        responseType: "LONG_CONSTRUCTED",
        accessibilityLabel: "Synthetic long-form response editor",
        prompt:
          "Draft a short internal memo based only on the fictional resources.",
        resourceIds: ["pt-file", "pt-library"],
      },
    ],
    presentationMetadata: fixtureMetadata,
  },
  {
    presentationSchemaVersion,
    assessmentId: "fixture-lrpt",
    assessmentVersionId: "fixture-lrpt-v1",
    title: "Portable LRPT workspace proof",
    family: "PT_LEGAL_RESEARCH",
    layout: "RESEARCH_WORKSPACE",
    navigationMode: "FREE",
    capabilities: [
      "QUESTION_NAVIGATOR",
      "MARK_FOR_REVIEW",
      "COPY_PASTE",
      "BASIC_FORMATTING",
      "RESOURCE_TABS",
    ],
    resources: [
      {
        id: "lrpt-message",
        type: "EMAIL",
        title: "Research request",
        accessibilityLabel: "Synthetic research request resource",
        content: `${syntheticNotice} Identify which fictional source addresses delivery time.`,
      },
      {
        id: "lrpt-case",
        type: "CASE",
        title: "Rowan Delivery Opinion",
        accessibilityLabel: "Synthetic opinion resource",
        content: `${syntheticNotice} This invented opinion discusses a fictional delivery policy.`,
      },
      {
        id: "lrpt-statute",
        type: "STATUTE",
        title: "Northlake Filing Act",
        accessibilityLabel: "Synthetic statute resource",
        content: `${syntheticNotice} This invented act has no legal authority or instructional value.`,
      },
    ],
    units: [
      {
        id: "lrpt-unit-1",
        component: "LONG_RESPONSE_EDITOR",
        responseType: "COUNSEL",
        accessibilityLabel: "Synthetic legal research response editor",
        prompt:
          "Write a brief research update using only the fictional sources.",
        resourceIds: ["lrpt-message", "lrpt-case", "lrpt-statute"],
      },
    ],
    presentationMetadata: fixtureMetadata,
  },
] as const;

export const m15AssessmentFixtures: readonly AssessmentPresentation[] =
  rawFixtures.map((fixture) => assertValidAssessmentPresentation(fixture));

export function m15FixtureByFamily(family: AssessmentPresentation["family"]) {
  const fixture = m15AssessmentFixtures.find((item) => item.family === family);
  if (!fixture) throw new Error(`Missing M1.5 fixture for ${family}.`);
  return fixture;
}
