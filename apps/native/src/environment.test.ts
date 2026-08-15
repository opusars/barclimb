import { describe, expect, it } from "vitest";
import { resolveNativeEnvironment } from "./environment";

describe("native environment", () => {
  it("requires explicit HTTPS deployed origins", () => {
    expect(() => resolveNativeEnvironment({ environment: "staging" })).toThrow(
      /explicit/,
    );
    expect(() =>
      resolveNativeEnvironment({
        environment: "staging",
        apiBaseUrl: "http://api.test",
        webBaseUrl: "https://web.test",
      }),
    ).toThrow(/HTTPS/);
  });

  it("allows isolated local defaults", () => {
    expect(resolveNativeEnvironment({}).environment).toBe("local");
  });
});
