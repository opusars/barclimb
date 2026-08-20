import { describe, expect, it } from "vitest";
import { m15AssessmentFixtures } from "@barclimb/assessment-schema";
import {
  describeWebRenderer,
  webAssessmentRendererRegistry,
} from "./assessmentRenderer";

describe("web assessment renderer registry", () => {
  it("maps every M1.5 fixture unit to a DOM-appropriate renderer", () => {
    for (const fixture of m15AssessmentFixtures) {
      for (const unit of fixture.units)
        expect(describeWebRenderer(unit).ok).toBe(true);
    }
    expect(webAssessmentRendererRegistry).toEqual({
      SINGLE_SELECT_QUESTION: "WEB_SEMANTIC_RADIO_GROUP",
      LONG_RESPONSE_EDITOR: "WEB_TEXTAREA_WORKSPACE",
    });
  });

  it("returns a typed fail-safe instead of arbitrary HTML", () => {
    expect(
      describeWebRenderer({ component: "WEBVIEW" } as never),
    ).toMatchObject({
      ok: false,
      error: { code: "UNSUPPORTED_COMPONENT", component: "WEBVIEW" },
    });
  });
});
