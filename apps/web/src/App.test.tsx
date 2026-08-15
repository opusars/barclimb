// @vitest-environment jsdom

import { act } from "react";
import { createRoot } from "react-dom/client";
import { afterEach, describe, expect, it, vi } from "vitest";
import { BrowserRouter } from "react-router-dom";
import { App } from "./App";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });

describe("web shell", () => {
  afterEach(() => {
    document.body.replaceChildren();
    window.history.replaceState(null, "", "/");
    vi.unstubAllGlobals();
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
      root.render(
        <BrowserRouter>
          <App />
        </BrowserRouter>,
      );
    });

    expect(container.textContent).toContain("BarClimb");
    expect(container.textContent).toContain("Secure account");
    expect(container.textContent).toContain("Create account");

    await act(async () => {
      root.unmount();
    });
  });

  it.each([
    ["/reset-password", "Choose a new password"],
    ["/verify-email", "Verify your email"],
  ])(
    "consumes an action credential from the fragment and cleans %s",
    async (path, title) => {
      window.history.replaceState(null, "", `${path}#token=fragment-secret`);
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
        root.render(
          <BrowserRouter>
            <App />
          </BrowserRouter>,
        );
      });

      expect(container.textContent).toContain(title);
      expect(window.location.pathname).toBe(path);
      expect(window.location.hash).toBe("");
      expect(window.location.search).toBe("");

      await act(async () => root.unmount());
    },
  );

  it.each([
    ["/login", "Welcome back"],
    ["/signup", "Create your account"],
    ["/forgot-password", "Reset your password"],
  ])("renders a stable direct route at %s", async (path, title) => {
    window.history.replaceState(null, "", path);
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
    await act(async () =>
      root.render(
        <BrowserRouter>
          <App />
        </BrowserRouter>,
      ),
    );
    expect(container.textContent).toContain(title);
    expect(window.location.pathname).toBe(path);
    await act(async () => root.unmount());
  });
});
