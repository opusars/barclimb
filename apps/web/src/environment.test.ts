import { describe, expect, it } from "vitest";
import { resolveWebEnvironment } from "./environment";

describe("Web environment", () => {
  it("uses same-origin API calls in staging", () => {
    expect(
      resolveWebEnvironment({
        environment: "staging",
        browserOrigin: "https://staging.example.test",
      }).apiBaseUrl,
    ).toBe("");
  });

  it("rejects deployed HTTP and proxy configuration", () => {
    expect(() =>
      resolveWebEnvironment({
        environment: "staging",
        browserOrigin: "http://staging.example.test",
      }),
    ).toThrow(/HTTPS/);
    expect(() =>
      resolveWebEnvironment({
        environment: "production",
        browserOrigin: "https://barclimb.example.test",
        localProxyTarget: "https://api.example.test",
      }),
    ).toThrow(/same-origin/);
  });
});
