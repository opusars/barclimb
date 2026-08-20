// @vitest-environment jsdom

import { act } from "react";
import { createRoot, type Root } from "react-dom/client";
import { afterEach, describe, expect, it } from "vitest";
import { MemoryWorkspacePersistence } from "@barclimb/assessment-schema";
import { AssessmentProof } from "./AssessmentProof";

Object.assign(globalThis, { IS_REACT_ACT_ENVIRONMENT: true });

let root: Root | null = null;

afterEach(async () => {
  if (root) await act(async () => root?.unmount());
  root = null;
  document.body.replaceChildren();
  window.localStorage.clear();
});

function button(container: HTMLElement, label: string) {
  const match = [...container.querySelectorAll("button")].find(
    (candidate) => candidate.textContent?.trim() === label,
  );
  if (!match) throw new Error(`Missing button ${label}.`);
  return match;
}

async function click(target: Element) {
  await act(async () => {
    target.dispatchEvent(new MouseEvent("click", { bubbles: true }));
  });
}

async function renderProof() {
  const container = document.createElement("div");
  document.body.append(container);
  root = createRoot(container);
  await act(async () => {
    root?.render(
      <AssessmentProof
        persistence={new MemoryWorkspacePersistence()}
        autosaveDelayMs={60_000}
      />,
    );
  });
  return container;
}

describe("Web assessment presentation proof", () => {
  it("changes MCQ selection and exposes persistent review state", async () => {
    const container = await renderProof();
    const choices = container.querySelectorAll('[role="radio"]');
    expect(choices).toHaveLength(4);
    await click(choices[0]!);
    await click(choices[1]!);
    expect(choices[0]!.getAttribute("aria-checked")).toBe("false");
    expect(choices[1]!.getAttribute("aria-checked")).toBe("true");
    await click(button(container, "Mark for review"));
    expect(
      button(container, "Marked for review").getAttribute("aria-pressed"),
    ).toBe("true");
  });

  it("switches IQS resources without losing answer state", async () => {
    const container = await renderProof();
    await click(button(container, "IQS"));
    const choices = container.querySelectorAll('[role="radio"]');
    await click(choices[2]!);
    await click(button(container, "Office email"));
    expect(container.textContent).toContain(
      "The office clock was checked against the lobby clock",
    );
    await click(button(container, "Northlake Rule 7"));
    expect(choices[2]!.getAttribute("aria-checked")).toBe("true");
    expect(container.textContent).toContain("This is not real law");
  });

  it("shows a typed recoverable state after an interrupted long-form save", async () => {
    const container = await renderProof();
    await click(button(container, "PT_STANDARD"));
    expect(container.querySelector("textarea")).not.toBeNull();
    await click(button(container, "Simulate interrupted save"));
    expect(container.textContent).toContain("Recoverable save failure");
    expect(container.textContent).toContain("Portable formatting ranges: 0");
  });
});
