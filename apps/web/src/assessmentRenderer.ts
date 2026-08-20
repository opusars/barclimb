import {
  createRendererRegistry,
  resolveRenderer,
  type AssessmentUnit,
} from "@barclimb/assessment-schema";

export const webAssessmentRendererRegistry = createRendererRegistry({
  SINGLE_SELECT_QUESTION: "WEB_SEMANTIC_RADIO_GROUP",
  LONG_RESPONSE_EDITOR: "WEB_TEXTAREA_WORKSPACE",
} as const);

export function describeWebRenderer(unit: Pick<AssessmentUnit, "component">) {
  return resolveRenderer(webAssessmentRendererRegistry, unit.component);
}
