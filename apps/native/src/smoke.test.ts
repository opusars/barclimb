import { describe, expect, it } from "vitest";
import { spacing } from "@barclimb/design-tokens";

describe("native foundation", () => {
  it("resolves shared platform-neutral tokens", () =>
    expect(spacing[4]).toBe(16));
});
