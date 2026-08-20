import {
  createRendererRegistry,
  resolveRenderer,
  type AssessmentUnit,
} from "@barclimb/assessment-schema";

export const nativeAssessmentRendererRegistry = createRendererRegistry({
  SINGLE_SELECT_QUESTION: "NATIVE_ACCESSIBLE_RADIO_LIST",
  LONG_RESPONSE_EDITOR: "NATIVE_MULTILINE_TEXT_WORKSPACE",
} as const);

export function describeNativeRenderer(
  unit: Pick<AssessmentUnit, "component">,
) {
  return resolveRenderer(nativeAssessmentRendererRegistry, unit.component);
}
