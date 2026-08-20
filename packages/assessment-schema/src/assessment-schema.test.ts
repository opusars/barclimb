import { describe, expect, it } from "vitest";
import {
  adjustIndent,
  applyFormattingMark,
  beginWorkspaceSave,
  completeWorkspaceSave,
  createRendererRegistry,
  createWorkspaceState,
  deserializeWorkspaceState,
  failWorkspaceSave,
  m15AssessmentFixtures,
  m15FixtureByFamily,
  MemoryWorkspacePersistence,
  resolveRenderer,
  selectChoice,
  selectResource,
  setBlockStyle,
  serializeWorkspaceState,
  toggleMarkedForReview,
  updateDraft,
  validateAssessmentPresentation,
  workspacePersistenceKey,
} from "./index";

describe("portable assessment presentation contract", () => {
  it("runtime-validates every isolated M1.5 family fixture", () => {
    expect(m15AssessmentFixtures.map((fixture) => fixture.family)).toEqual([
      "STANDALONE_MCQ",
      "IQS",
      "PT_STANDARD",
      "PT_LEGAL_RESEARCH",
    ]);
    for (const fixture of m15AssessmentFixtures) {
      expect(validateAssessmentPresentation(fixture)).toEqual({
        ok: true,
        value: fixture,
      });
      expect(fixture.presentationMetadata).toMatchObject({
        contentClassification: "TEST_FIXTURE",
        fixtureUse: "DEVELOPMENT_ONLY",
        syntheticContent: true,
        publicationEligibility: "INELIGIBLE",
      });
    }
  });

  it("rejects invalid resource references and fixture classification", () => {
    const fixture = m15FixtureByFamily("IQS");
    const missingResource = structuredClone(fixture) as unknown as {
      units: { resourceIds: string[] }[];
    };
    missingResource.units[0]!.resourceIds = ["not-present"];
    const result = validateAssessmentPresentation(missingResource);
    expect(result.ok).toBe(false);
    if (!result.ok) expect(result.issues[0]?.code).toBe("MISSING_REFERENCE");

    const misclassified = structuredClone(fixture) as unknown as {
      presentationMetadata: { publicationEligibility: string };
    };
    misclassified.presentationMetadata.publicationEligibility =
      "CONTROLLED_BY_SERVER";
    const classification = validateAssessmentPresentation(misclassified);
    expect(classification.ok).toBe(false);
    if (!classification.ok)
      expect(classification.issues[0]?.code).toBe(
        "INVALID_FIXTURE_CLASSIFICATION",
      );
  });

  it("keeps the core contract open to future server-owned AssessmentVersions", () => {
    const serverOwned = structuredClone(
      m15FixtureByFamily("STANDALONE_MCQ"),
    ) as unknown as {
      presentationMetadata: Record<string, unknown>;
    };
    serverOwned.presentationMetadata = {
      contentClassification: "ASSESSMENT_VERSION",
      fixtureUse: null,
      syntheticContent: false,
      publicationEligibility: "CONTROLLED_BY_SERVER",
      rendererContract: "REGISTERED_COMPONENTS_ONLY",
      recommendedViewport: "PHONE_TO_DESKTOP",
    };
    expect(validateAssessmentPresentation(serverOwned).ok).toBe(true);
  });

  it("rejects unsupported components and renderer registries fail safely", () => {
    const fixture = structuredClone(
      m15FixtureByFamily("STANDALONE_MCQ"),
    ) as unknown as { units: { component: string }[] };
    fixture.units[0]!.component = "ARBITRARY_HTML";
    const validation = validateAssessmentPresentation(fixture);
    expect(validation.ok).toBe(false);
    if (!validation.ok)
      expect(validation.issues[0]?.code).toBe("UNSUPPORTED_COMPONENT");

    const registry = createRendererRegistry({
      SINGLE_SELECT_QUESTION: "web-radio",
      LONG_RESPONSE_EDITOR: "web-editor",
    });
    expect(resolveRenderer(registry, "ARBITRARY_HTML")).toEqual({
      ok: false,
      error: {
        code: "UNSUPPORTED_COMPONENT",
        component: "ARBITRARY_HTML",
        message:
          "This client cannot safely render assessment component ARBITRARY_HTML.",
      },
    });
  });
});

describe("portable workspace state", () => {
  it("preserves MCQ selection and review state through navigation", () => {
    const fixture = m15FixtureByFamily("STANDALONE_MCQ");
    const unit = fixture.units[0]!;
    let state = createWorkspaceState(fixture);
    state = selectChoice(state, unit.id, "mcq-a");
    state = selectChoice(state, unit.id, "mcq-b");
    state = toggleMarkedForReview(state, unit.id);
    expect(state.responses[unit.id]).toEqual({
      type: "CHOICE",
      selectedChoiceIds: ["mcq-b"],
    });
    expect(state.markedForReviewUnitIds).toEqual([unit.id]);
  });

  it("switches IQS resources without losing the selected answer", () => {
    const fixture = m15FixtureByFamily("IQS");
    const unit = fixture.units[0]!;
    let state = selectChoice(createWorkspaceState(fixture), unit.id, "iqs-c");
    state = selectResource(state, "iqs-email");
    state = selectResource(state, "iqs-authority");
    expect(state.currentResourceId).toBe("iqs-authority");
    expect(state.responses[unit.id]).toEqual({
      type: "CHOICE",
      selectedChoiceIds: ["iqs-c"],
    });
    expect(JSON.stringify(state)).not.toMatch(
      /\b(dom|window|screenX|screenY|pixelX|pixelY|widget)\b/i,
    );
  });

  it("models long-form drafting, portable formatting, and save recovery", () => {
    const fixture = m15FixtureByFamily("PT_LEGAL_RESEARCH");
    const unit = fixture.units[0]!;
    let state = updateDraft(
      createWorkspaceState(fixture),
      unit.id,
      "Synthetic research update",
    );
    state = applyFormattingMark(state, unit.id, "BOLD", 0, 9);
    state = setBlockStyle(state, unit.id, "BULLETED_LIST");
    state = adjustIndent(state, unit.id, 1);
    state = beginWorkspaceSave(state);
    expect(state.persistence.status).toBe("SAVE_PENDING");
    state = failWorkspaceSave(state);
    expect(state.persistence).toMatchObject({
      status: "RECOVERABLE_FAILURE",
      failureCode: "INTERRUPTED_WRITE",
    });
    state = completeWorkspaceSave(
      beginWorkspaceSave(state),
      "2026-08-20T20:00:00.000Z",
    );
    const restored = deserializeWorkspaceState(
      serializeWorkspaceState(state),
      fixture,
    );
    expect(restored.persistence.status).toBe("RESTORED");
    expect(restored.responses[unit.id]).toEqual(state.responses[unit.id]);
    expect(restored.responses[unit.id]).toMatchObject({
      type: "TEXT",
      document: { blockStyle: "BULLETED_LIST", indentLevel: 1 },
    });
  });

  it("persists the last complete snapshot across component remounts", async () => {
    const fixture = m15FixtureByFamily("PT_STANDARD");
    const unit = fixture.units[0]!;
    const persistence = new MemoryWorkspacePersistence();
    const key = workspacePersistenceKey(fixture.assessmentVersionId);
    const saved = completeWorkspaceSave(
      updateDraft(createWorkspaceState(fixture), unit.id, "Recovered draft"),
      "2026-08-20T20:00:00.000Z",
    );
    await persistence.write(key, serializeWorkspaceState(saved));
    persistence.failNextWrite();
    await expect(persistence.write(key, "interrupted")).rejects.toThrow(
      "Simulated interrupted write",
    );
    const stored = await persistence.read(key);
    expect(stored).not.toBeNull();
    const restored = deserializeWorkspaceState(stored!, fixture);
    expect(restored.responses[unit.id]).toMatchObject({
      type: "TEXT",
      document: { text: "Recovered draft" },
    });
  });
});
