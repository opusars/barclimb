// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });

describe("web shell", () => {
  afterEach(() => {
    document.body.replaceChildren();
  });

  it("mounts through ReactDOM with one compatible React runtime", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ authenticated: false, user: null }),
      }),
    );
    const container = document.createElement("div");
    document.body.append(container);
    const root = createRoot(container);

    await act(async () => {
      root.render(<App />);
    });

    expect(container.textContent).toContain("BarClimb");
    expect(container.textContent).toContain("Secure account");
    expect(container.textContent).toContain("Create account");

    await act(async () => {
      root.unmount();
    });
    vi.unstubAllGlobals();
  });
});
