import { describe, expect, it } from "vitest";
import { resolveCanonicalLink } from "./deepLinks";

describe("canonical link resolution", () => {
  it("routes supported app links natively", () => {
    expect(
      resolveCanonicalLink(
        "https://staging.barclimb.test/progress",
        "https://staging.barclimb.test",
      ),
    ).toEqual({ kind: "native", path: "/progress" });
    expect(
      resolveCanonicalLink(
        "https://staging.barclimb.test/search",
        "https://staging.barclimb.test",
      ),
    ).toEqual({ kind: "native", path: "/search" });
  });

  it("keeps fragment credentials in the Web completion boundary", () => {
    const resolved = resolveCanonicalLink(
      "https://staging.barclimb.test/reset-password#token=fragment-secret",
      "https://staging.barclimb.test",
    );
    expect(resolved).toEqual({
      kind: "web_only_auth",
      path: "/reset-password",
    });
    expect(JSON.stringify(resolved)).not.toContain("fragment-secret");
  });

  it("returns a clean Web fallback without query or fragment data", () => {
    expect(
      resolveCanonicalLink(
        "https://staging.barclimb.test/nextgen?q=private#token=secret",
        "https://staging.barclimb.test",
      ),
    ).toEqual({
      kind: "web_fallback",
      url: "https://staging.barclimb.test/nextgen",
    });
  });
});
