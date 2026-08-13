import { describe, expect, it } from "vitest";
import { colors } from "@barclimb/design-tokens";

describe("web foundation", () => {
  it("resolves shared design tokens", () =>
    expect(colors.accent).toBe("#3157d5"));
});
