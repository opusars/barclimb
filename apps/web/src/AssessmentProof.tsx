import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ChangeEvent,
} from "react";
import {
  adjustIndent,
  applyFormattingMark,
  beginWorkspaceSave,
  completeWorkspaceSave,
  createWorkspaceState,
  deserializeWorkspaceState,
  failWorkspaceSave,
  m15AssessmentFixtures,
  selectChoice,
  selectResource,
  selectWorkspaceView,
  serializeWorkspaceState,
  setBlockStyle,
  toggleMarkedForReview,
  updateDraft,
  workspacePersistenceKey,
  type AssessmentPresentation,
  type FormattingMark,
  type WorkspacePersistence,
  type WorkspaceState,
} from "@barclimb/assessment-schema";
import { describeWebRenderer } from "./assessmentRenderer";

const browserPersistence: WorkspacePersistence = {
  async read(key) {
    return window.localStorage.getItem(key);
  },
  async write(key, value) {
    window.localStorage.setItem(key, value);
  },
};

const saveStatusLabel: Record<WorkspaceState["persistence"]["status"], string> =
  {
    UNSAVED_LOCAL: "Unsaved local edit",
    SAVE_PENDING: "Save pending",
    SAVED: "Saved",
    RECOVERABLE_FAILURE: "Recoverable save failure",
    RESTORED: "Restored local state",
  };

export function AssessmentProof({
  persistence = browserPersistence,
  autosaveDelayMs = 450,
}: {
  persistence?: WorkspacePersistence;
  autosaveDelayMs?: number;
}) {
  const [presentation, setPresentation] = useState(m15AssessmentFixtures[0]!);
  const [state, setState] = useState(() =>
    createWorkspaceState(m15AssessmentFixtures[0]!),
  );
  const [selection, setSelection] = useState({ start: 0, end: 0 });
  const editorRef = useRef<HTMLTextAreaElement>(null);
  const unit = presentation.units.find(
    (candidate) => candidate.id === state.currentUnitId,
  );
  const activeResource = presentation.resources.find(
    (resource) => resource.id === state.currentResourceId,
  );

  useEffect(() => {
    let active = true;
    const fresh = createWorkspaceState(presentation);
    void persistence
      .read(workspacePersistenceKey(presentation.assessmentVersionId))
      .then((saved) => {
        if (!active || !saved) return;
        try {
          setState(deserializeWorkspaceState(saved, presentation));
        } catch {
          setState(fresh);
        }
      });
    return () => {
      active = false;
    };
  }, [persistence, presentation]);

  const save = useCallback(
    async (snapshot: WorkspaceState) => {
      const pending = beginWorkspaceSave(snapshot);
      setState((current) =>
        current.persistence.localRevision === snapshot.persistence.localRevision
          ? pending
          : current,
      );
      const saved = completeWorkspaceSave(pending, new Date().toISOString());
      try {
        await persistence.write(
          workspacePersistenceKey(presentation.assessmentVersionId),
          serializeWorkspaceState(saved),
        );
        setState((current) =>
          current.persistence.localRevision ===
          snapshot.persistence.localRevision
            ? saved
            : current,
        );
      } catch {
        setState((current) =>
          current.persistence.localRevision ===
          snapshot.persistence.localRevision
            ? failWorkspaceSave(current)
            : current,
        );
      }
    },
    [persistence, presentation.assessmentVersionId],
  );

  useEffect(() => {
    if (state.persistence.status !== "UNSAVED_LOCAL") return;
    const timer = window.setTimeout(() => void save(state), autosaveDelayMs);
    return () => window.clearTimeout(timer);
  }, [autosaveDelayMs, save, state]);

  useEffect(() => {
    const saveBeforeExit = () => {
      if (state.persistence.status === "UNSAVED_LOCAL") void save(state);
    };
    window.addEventListener("pagehide", saveBeforeExit);
    return () => window.removeEventListener("pagehide", saveBeforeExit);
  }, [save, state]);

  const renderer = useMemo(
    () => (unit ? describeWebRenderer(unit) : null),
    [unit],
  );

  if (!unit)
    return (
      <section className="assessment-error" role="alert">
        The assessment unit is unavailable. No content was omitted.
      </section>
    );
  if (!renderer?.ok)
    return (
      <section className="assessment-error" role="alert">
        {renderer?.error.message ?? "Unsupported assessment component."}
      </section>
    );

  const unitId = unit.id;
  const response = state.responses[unitId];
  const marked = state.markedForReviewUnitIds.includes(unitId);

  function switchFixture(next: AssessmentPresentation) {
    setPresentation(next);
    setState(createWorkspaceState(next));
  }

  function formatSelection(type: FormattingMark) {
    setState((current) =>
      applyFormattingMark(
        current,
        unitId,
        type,
        selection.start,
        selection.end,
      ),
    );
    editorRef.current?.focus();
  }

  function captureSelection(event: ChangeEvent<HTMLTextAreaElement>) {
    setSelection({
      start: event.currentTarget.selectionStart,
      end: event.currentTarget.selectionEnd,
    });
  }

  return (
    <section className="assessment-proof" aria-labelledby="proof-title">
      <div className="fixture-warning" role="note">
        TEST_FIXTURE · DEVELOPMENT_ONLY · synthetic content · never graded
      </div>
      <div className="assessment-proof-header">
        <div>
          <p className="eyebrow">M1.5 portable renderer proof</p>
          <h2 id="proof-title">{presentation.title}</h2>
          <p>
            {presentation.family} · {presentation.layout} · Web renderer:{" "}
            {renderer.renderer}
          </p>
        </div>
        <p className="save-status" role="status" aria-live="polite">
          {saveStatusLabel[state.persistence.status]}
        </p>
      </div>

      <nav className="fixture-switcher" aria-label="Synthetic fixture family">
        {m15AssessmentFixtures.map((fixture) => (
          <button
            key={fixture.assessmentVersionId}
            type="button"
            className={
              fixture.assessmentVersionId === presentation.assessmentVersionId
                ? "active-proof-control"
                : "secondary-proof-control"
            }
            aria-pressed={
              fixture.assessmentVersionId === presentation.assessmentVersionId
            }
            onClick={() => switchFixture(fixture)}
          >
            {fixture.family}
          </button>
        ))}
      </nav>

      {presentation.resources.length > 0 && (
        <nav className="workspace-view-switcher" aria-label="Workspace view">
          {(["QUESTION", "RESOURCES", "RESPONSE"] as const).map((view) => (
            <button
              key={view}
              type="button"
              aria-pressed={state.currentView === view}
              className="secondary-proof-control"
              onClick={() =>
                setState((current) => selectWorkspaceView(current, view))
              }
            >
              {view}
            </button>
          ))}
        </nav>
      )}

      <div
        className={`assessment-workspace ${presentation.resources.length ? "has-resources" : ""}`}
      >
        {presentation.resources.length > 0 && (
          <aside className="resource-panel" aria-label="Provided resources">
            <div className="resource-tabs" role="tablist">
              {presentation.resources.map((resource) => (
                <button
                  type="button"
                  role="tab"
                  aria-selected={resource.id === state.currentResourceId}
                  key={resource.id}
                  className="secondary-proof-control"
                  onClick={() =>
                    setState((current) => selectResource(current, resource.id))
                  }
                >
                  {resource.title}
                </button>
              ))}
            </div>
            {activeResource && (
              <article
                className="resource-content"
                aria-label={activeResource.accessibilityLabel}
              >
                <p className="resource-type">{activeResource.type}</p>
                <h3>{activeResource.title}</h3>
                <p>{activeResource.content}</p>
              </article>
            )}
          </aside>
        )}

        <div className="response-panel">
          <div className="unit-toolbar">
            <button
              type="button"
              className="secondary-proof-control"
              aria-pressed={marked}
              onClick={() =>
                setState((current) => toggleMarkedForReview(current, unit.id))
              }
            >
              {marked ? "Marked for review" : "Mark for review"}
            </button>
          </div>
          <p className="assessment-prompt">{unit.prompt}</p>
          {unit.component === "SINGLE_SELECT_QUESTION" &&
            response?.type === "CHOICE" && (
              <fieldset className="choice-list">
                <legend className="visually-hidden">
                  {unit.accessibilityLabel}
                </legend>
                {unit.choices.map((choice) => {
                  const selected = response.selectedChoiceIds.includes(
                    choice.id,
                  );
                  return (
                    <button
                      type="button"
                      role="radio"
                      aria-checked={selected}
                      key={choice.id}
                      className={`choice-row ${selected ? "selected-choice" : ""}`}
                      onClick={() =>
                        setState((current) =>
                          selectChoice(current, unit.id, choice.id),
                        )
                      }
                    >
                      <span>{choice.label}</span>
                      {choice.text}
                    </button>
                  );
                })}
              </fieldset>
            )}
          {unit.component === "LONG_RESPONSE_EDITOR" &&
            response?.type === "TEXT" && (
              <div className="editor-shell">
                <div className="format-toolbar" aria-label="Basic formatting">
                  {(["BOLD", "ITALIC", "UNDERLINE"] as const).map((mark) => (
                    <button
                      type="button"
                      className="secondary-proof-control"
                      key={mark}
                      onClick={() => formatSelection(mark)}
                    >
                      {mark}
                    </button>
                  ))}
                  <button
                    type="button"
                    className="secondary-proof-control"
                    onClick={() =>
                      setState((current) =>
                        setBlockStyle(current, unitId, "BULLETED_LIST"),
                      )
                    }
                  >
                    BULLETS
                  </button>
                  <button
                    type="button"
                    className="secondary-proof-control"
                    onClick={() =>
                      setState((current) =>
                        setBlockStyle(current, unitId, "NUMBERED_LIST"),
                      )
                    }
                  >
                    NUMBERING
                  </button>
                  <button
                    type="button"
                    className="secondary-proof-control"
                    onClick={() =>
                      setState((current) => adjustIndent(current, unitId, 1))
                    }
                  >
                    INDENT
                  </button>
                  <button
                    type="button"
                    className="secondary-proof-control"
                    onClick={() =>
                      setState((current) => adjustIndent(current, unitId, -1))
                    }
                  >
                    OUTDENT
                  </button>
                </div>
                <textarea
                  ref={editorRef}
                  aria-label={unit.accessibilityLabel}
                  value={response.document.text}
                  onChange={(event) =>
                    setState((current) =>
                      updateDraft(current, unit.id, event.target.value),
                    )
                  }
                  onSelect={captureSelection}
                  rows={12}
                  spellCheck
                />
                <p className="format-summary" aria-live="polite">
                  Portable formatting ranges: {response.document.marks.length} ·{" "}
                  {response.document.blockStyle} · indent{" "}
                  {response.document.indentLevel}
                </p>
              </div>
            )}
          <div className="save-actions">
            <button type="button" onClick={() => void save(state)}>
              Save now
            </button>
            <button
              type="button"
              className="secondary-proof-control"
              onClick={() =>
                setState((current) =>
                  failWorkspaceSave(beginWorkspaceSave(current)),
                )
              }
            >
              Simulate interrupted save
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
