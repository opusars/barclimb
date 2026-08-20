import {
  portableTextSchemaVersion,
  workspaceSchemaVersion,
  type AssessmentPresentation,
  type FormattingMark,
  type WorkspaceResponse,
  type WorkspaceState,
} from "./types";
import { validateWorkspaceState } from "./validation";

const emptyResponse = (
  component: "SINGLE_SELECT_QUESTION" | "LONG_RESPONSE_EDITOR",
): WorkspaceResponse =>
  component === "SINGLE_SELECT_QUESTION"
    ? { type: "CHOICE", selectedChoiceIds: [] }
    : {
        type: "TEXT",
        document: {
          schemaVersion: portableTextSchemaVersion,
          text: "",
          marks: [],
          blockStyle: "PARAGRAPH",
          indentLevel: 0,
        },
      };

export function createWorkspaceState(
  presentation: AssessmentPresentation,
): WorkspaceState {
  const firstUnit = presentation.units[0];
  if (!firstUnit) throw new Error("A presentation must contain a unit.");
  return {
    schemaVersion: workspaceSchemaVersion,
    assessmentVersionId: presentation.assessmentVersionId,
    currentUnitId: firstUnit.id,
    currentResourceId: presentation.resources[0]?.id ?? null,
    currentView: "QUESTION",
    responses: Object.fromEntries(
      presentation.units.map((unit) => [
        unit.id,
        emptyResponse(unit.component),
      ]),
    ),
    markedForReviewUnitIds: [],
    persistence: {
      status: "SAVED",
      localRevision: 0,
      savedRevision: 0,
      lastSavedAt: null,
      failureCode: null,
    },
  };
}

const edited = (state: WorkspaceState): WorkspaceState => ({
  ...state,
  persistence: {
    ...state.persistence,
    status: "UNSAVED_LOCAL",
    localRevision: state.persistence.localRevision + 1,
    failureCode: null,
  },
});

export function selectChoice(
  state: WorkspaceState,
  unitId: string,
  choiceId: string,
): WorkspaceState {
  const response = state.responses[unitId];
  if (!response || response.type !== "CHOICE")
    throw new Error(`Unit ${unitId} is not a choice response.`);
  return edited({
    ...state,
    responses: {
      ...state.responses,
      [unitId]: { type: "CHOICE", selectedChoiceIds: [choiceId] },
    },
  });
}

export function updateDraft(
  state: WorkspaceState,
  unitId: string,
  text: string,
): WorkspaceState {
  const response = state.responses[unitId];
  if (!response || response.type !== "TEXT")
    throw new Error(`Unit ${unitId} is not a text response.`);
  const marks = response.document.marks.filter(
    (mark) => mark.end <= text.length,
  );
  return edited({
    ...state,
    responses: {
      ...state.responses,
      [unitId]: {
        type: "TEXT",
        document: { ...response.document, text, marks },
      },
    },
  });
}

export function applyFormattingMark(
  state: WorkspaceState,
  unitId: string,
  type: FormattingMark,
  start: number,
  end: number,
): WorkspaceState {
  const response = state.responses[unitId];
  if (!response || response.type !== "TEXT")
    throw new Error(`Unit ${unitId} is not a text response.`);
  if (start < 0 || end <= start || end > response.document.text.length)
    return state;
  const duplicate = response.document.marks.some(
    (mark) => mark.type === type && mark.start === start && mark.end === end,
  );
  const marks = duplicate
    ? response.document.marks.filter(
        (mark) =>
          !(mark.type === type && mark.start === start && mark.end === end),
      )
    : [...response.document.marks, { type, start, end }];
  return edited({
    ...state,
    responses: {
      ...state.responses,
      [unitId]: {
        type: "TEXT",
        document: { ...response.document, marks },
      },
    },
  });
}

export function setBlockStyle(
  state: WorkspaceState,
  unitId: string,
  blockStyle: "PARAGRAPH" | "BULLETED_LIST" | "NUMBERED_LIST",
): WorkspaceState {
  const response = state.responses[unitId];
  if (!response || response.type !== "TEXT")
    throw new Error(`Unit ${unitId} is not a text response.`);
  return edited({
    ...state,
    responses: {
      ...state.responses,
      [unitId]: {
        type: "TEXT",
        document: { ...response.document, blockStyle },
      },
    },
  });
}

export function adjustIndent(
  state: WorkspaceState,
  unitId: string,
  delta: -1 | 1,
): WorkspaceState {
  const response = state.responses[unitId];
  if (!response || response.type !== "TEXT")
    throw new Error(`Unit ${unitId} is not a text response.`);
  const indentLevel = Math.max(
    0,
    Math.min(3, response.document.indentLevel + delta),
  );
  if (indentLevel === response.document.indentLevel) return state;
  return edited({
    ...state,
    responses: {
      ...state.responses,
      [unitId]: {
        type: "TEXT",
        document: { ...response.document, indentLevel },
      },
    },
  });
}

export function selectResource(
  state: WorkspaceState,
  resourceId: string,
): WorkspaceState {
  return edited({
    ...state,
    currentResourceId: resourceId,
    currentView: "RESOURCES",
  });
}

export function selectWorkspaceView(
  state: WorkspaceState,
  currentView: WorkspaceState["currentView"],
): WorkspaceState {
  return edited({ ...state, currentView });
}

export function toggleMarkedForReview(
  state: WorkspaceState,
  unitId: string,
): WorkspaceState {
  const marked = state.markedForReviewUnitIds.includes(unitId);
  return edited({
    ...state,
    markedForReviewUnitIds: marked
      ? state.markedForReviewUnitIds.filter((id) => id !== unitId)
      : [...state.markedForReviewUnitIds, unitId],
  });
}

export const beginWorkspaceSave = (state: WorkspaceState): WorkspaceState => ({
  ...state,
  persistence: {
    ...state.persistence,
    status: "SAVE_PENDING",
    failureCode: null,
  },
});

export const completeWorkspaceSave = (
  state: WorkspaceState,
  savedAt: string,
): WorkspaceState => ({
  ...state,
  persistence: {
    ...state.persistence,
    status: "SAVED",
    savedRevision: state.persistence.localRevision,
    lastSavedAt: savedAt,
    failureCode: null,
  },
});

export const failWorkspaceSave = (state: WorkspaceState): WorkspaceState => ({
  ...state,
  persistence: {
    ...state.persistence,
    status: "RECOVERABLE_FAILURE",
    failureCode: "INTERRUPTED_WRITE",
  },
});

export const serializeWorkspaceState = (state: WorkspaceState): string =>
  JSON.stringify(state);

export function deserializeWorkspaceState(
  serialized: string,
  presentation: AssessmentPresentation,
): WorkspaceState {
  let parsed: unknown;
  try {
    parsed = JSON.parse(serialized);
  } catch {
    throw new Error("Saved workspace is not valid JSON.");
  }
  const result = validateWorkspaceState(parsed, presentation);
  if (!result.ok)
    throw new Error(result.issues[0]?.message ?? "Invalid state.");
  return {
    ...result.value,
    persistence: {
      ...result.value.persistence,
      status: "RESTORED",
      failureCode: null,
    },
  };
}

export interface WorkspacePersistence {
  read(key: string): Promise<string | null>;
  write(key: string, value: string): Promise<void>;
}

export class MemoryWorkspacePersistence implements WorkspacePersistence {
  private readonly values = new Map<string, string>();
  private failNext = false;

  failNextWrite() {
    this.failNext = true;
  }

  async read(key: string) {
    return this.values.get(key) ?? null;
  }

  async write(key: string, value: string) {
    if (this.failNext) {
      this.failNext = false;
      throw new Error("Simulated interrupted write.");
    }
    this.values.set(key, value);
  }
}

export const workspacePersistenceKey = (assessmentVersionId: string) =>
  `barclimb:m1.5:${assessmentVersionId}`;
