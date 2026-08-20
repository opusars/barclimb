import { describe, expect, it } from "vitest";
import { m15AssessmentFixtures } from "@barclimb/assessment-schema";
import {
  describeNativeRenderer,
  nativeAssessmentRendererRegistry,
} from "./assessmentRenderer";

describe("native assessment renderer registry", () => {
  it("maps every shared fixture unit to a React Native renderer", () => {
    for (const fixture of m15AssessmentFixtures) {
      for (const unit of fixture.units)
        expect(describeNativeRenderer(unit).ok).toBe(true);
    }
    expect(nativeAssessmentRendererRegistry).toEqual({
      SINGLE_SELECT_QUESTION: "NATIVE_ACCESSIBLE_RADIO_LIST",
      LONG_RESPONSE_EDITOR: "NATIVE_MULTILINE_TEXT_WORKSPACE",
    });
  });

  it("returns a typed fail-safe and never requests a WebView", () => {
    expect(
      describeNativeRenderer({ component: "ARBITRARY_HTML" } as never),
    ).toMatchObject({
      ok: false,
      error: {
        code: "UNSUPPORTED_COMPONENT",
        component: "ARBITRARY_HTML",
      },
    });
  });
});
