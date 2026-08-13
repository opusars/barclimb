// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it } from "vitest";
import { App } from "./App";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });

describe("web shell", () => {
  afterEach(() => {
    document.body.replaceChildren();
  });

  it("mounts through ReactDOM with one compatible React runtime", async () => {
    const container = document.createElement("div");
    document.body.append(container);
    const root = createRoot(container);

    await act(async () => {
      root.render(<App />);
    });

    expect(container.textContent).toContain("BarClimb");
    expect(container.textContent).toContain("No learner features");

    await act(async () => {
      root.unmount();
    });
  });
});
