import { useCallback, useEffect, useMemo, useState } from "react";
import {
  AppState,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import {
  adjustIndent,
  applyFormattingMark,
  beginWorkspaceSave,
  completeWorkspaceSave,
  createWorkspaceState,
  deserializeWorkspaceState,
  failWorkspaceSave,
  m15AssessmentFixtures,
  MemoryWorkspacePersistence,
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
import { colors, spacing } from "@barclimb/design-tokens";
import { describeNativeRenderer } from "./assessmentRenderer";

const developmentPersistence = new MemoryWorkspacePersistence();

const statusLabel: Record<WorkspaceState["persistence"]["status"], string> = {
  UNSAVED_LOCAL: "Unsaved local edit",
  SAVE_PENDING: "Save pending",
  SAVED: "Saved",
  RECOVERABLE_FAILURE: "Recoverable save failure",
  RESTORED: "Restored local state",
};

export function AssessmentProofScreen({
  persistence = developmentPersistence,
  autosaveDelayMs = 450,
}: {
  persistence?: WorkspacePersistence;
  autosaveDelayMs?: number;
}) {
  const dimensions = useWindowDimensions();
  const wide = dimensions.width >= 768;
  const [presentation, setPresentation] = useState(m15AssessmentFixtures[0]!);
  const [state, setState] = useState(() =>
    createWorkspaceState(m15AssessmentFixtures[0]!),
  );
  const [selection, setSelection] = useState({ start: 0, end: 0 });
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
    const timer = setTimeout(() => void save(state), autosaveDelayMs);
    return () => clearTimeout(timer);
  }, [autosaveDelayMs, save, state]);

  useEffect(() => {
    const subscription = AppState.addEventListener("change", (next) => {
      if (next !== "active" && state.persistence.status === "UNSAVED_LOCAL")
        void save(state);
    });
    return () => subscription.remove();
  }, [save, state]);

  const renderer = useMemo(
    () => (unit ? describeNativeRenderer(unit) : null),
    [unit],
  );

  if (!unit || !renderer?.ok)
    return (
      <SafeAreaView style={styles.safeArea}>
        <View accessibilityRole="alert" style={styles.errorPanel}>
          <Text style={styles.errorText}>
            {renderer && !renderer.ok
              ? renderer.error.message
              : "The assessment unit is unavailable. No content was omitted."}
          </Text>
        </View>
      </SafeAreaView>
    );

  const unitId = unit.id;
  const response = state.responses[unitId];
  const marked = state.markedForReviewUnitIds.includes(unitId);

  function switchFixture(next: AssessmentPresentation) {
    setPresentation(next);
    setState(createWorkspaceState(next));
  }

  function applyMark(type: FormattingMark) {
    setState((current) =>
      applyFormattingMark(
        current,
        unitId,
        type,
        selection.start,
        selection.end,
      ),
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        contentContainerStyle={styles.screen}
        keyboardShouldPersistTaps="handled"
      >
        <View accessibilityRole="summary" style={styles.warning}>
          <Text style={styles.warningText}>
            TEST_FIXTURE · DEVELOPMENT_ONLY · synthetic content · never graded
          </Text>
        </View>
        <Text style={styles.eyebrow}>M1.5 portable renderer proof</Text>
        <Text accessibilityRole="header" style={styles.title}>
          {presentation.title}
        </Text>
        <Text style={styles.meta}>
          {presentation.family} · {presentation.layout} · {renderer.renderer}
        </Text>
        <Text accessibilityLiveRegion="polite" style={styles.status}>
          {statusLabel[state.persistence.status]}
        </Text>

        <ScrollView
          horizontal
          contentContainerStyle={styles.controls}
          accessibilityLabel="Synthetic fixture family"
        >
          {m15AssessmentFixtures.map((fixture) => (
            <ProofButton
              key={fixture.assessmentVersionId}
              label={fixture.family}
              selected={
                fixture.assessmentVersionId === presentation.assessmentVersionId
              }
              onPress={() => switchFixture(fixture)}
            />
          ))}
        </ScrollView>

        {presentation.resources.length > 0 && (
          <View style={styles.controls} accessibilityLabel="Workspace view">
            {(["QUESTION", "RESOURCES", "RESPONSE"] as const).map((view) => (
              <ProofButton
                key={view}
                label={view}
                selected={state.currentView === view}
                onPress={() =>
                  setState((current) => selectWorkspaceView(current, view))
                }
              />
            ))}
          </View>
        )}

        <View style={[styles.workspace, wide && styles.workspaceWide]}>
          {presentation.resources.length > 0 && (
            <View style={styles.panel} accessibilityLabel="Provided resources">
              <ScrollView horizontal contentContainerStyle={styles.controls}>
                {presentation.resources.map((resource) => (
                  <ProofButton
                    key={resource.id}
                    label={resource.title}
                    selected={resource.id === state.currentResourceId}
                    onPress={() =>
                      setState((current) =>
                        selectResource(current, resource.id),
                      )
                    }
                  />
                ))}
              </ScrollView>
              {activeResource && (
                <View
                  style={styles.resource}
                  accessibilityLabel={activeResource.accessibilityLabel}
                >
                  <Text style={styles.resourceType}>{activeResource.type}</Text>
                  <Text accessibilityRole="header" style={styles.panelTitle}>
                    {activeResource.title}
                  </Text>
                  <Text selectable style={styles.body}>
                    {activeResource.content}
                  </Text>
                </View>
              )}
            </View>
          )}

          <View style={styles.panel}>
            <ProofButton
              label={marked ? "Marked for review" : "Mark for review"}
              selected={marked}
              onPress={() =>
                setState((current) => toggleMarkedForReview(current, unit.id))
              }
            />
            <Text style={styles.prompt}>{unit.prompt}</Text>
            {unit.component === "SINGLE_SELECT_QUESTION" &&
              response?.type === "CHOICE" &&
              unit.choices.map((choice) => {
                const selected = response.selectedChoiceIds.includes(choice.id);
                return (
                  <Pressable
                    key={choice.id}
                    accessibilityRole="radio"
                    accessibilityLabel={`${choice.label}. ${choice.text}`}
                    accessibilityState={{ selected }}
                    style={[styles.choice, selected && styles.choiceSelected]}
                    onPress={() =>
                      setState((current) =>
                        selectChoice(current, unit.id, choice.id),
                      )
                    }
                  >
                    <Text style={styles.choiceLabel}>{choice.label}</Text>
                    <Text style={styles.choiceText}>{choice.text}</Text>
                  </Pressable>
                );
              })}
            {unit.component === "LONG_RESPONSE_EDITOR" &&
              response?.type === "TEXT" && (
                <View>
                  <View
                    style={styles.controls}
                    accessibilityLabel="Basic formatting"
                  >
                    {(["BOLD", "ITALIC", "UNDERLINE"] as const).map((mark) => (
                      <ProofButton
                        key={mark}
                        label={mark}
                        selected={false}
                        onPress={() => applyMark(mark)}
                      />
                    ))}
                    <ProofButton
                      label="BULLETS"
                      selected={
                        response.document.blockStyle === "BULLETED_LIST"
                      }
                      onPress={() =>
                        setState((current) =>
                          setBlockStyle(current, unitId, "BULLETED_LIST"),
                        )
                      }
                    />
                    <ProofButton
                      label="NUMBERING"
                      selected={
                        response.document.blockStyle === "NUMBERED_LIST"
                      }
                      onPress={() =>
                        setState((current) =>
                          setBlockStyle(current, unitId, "NUMBERED_LIST"),
                        )
                      }
                    />
                    <ProofButton
                      label="INDENT"
                      selected={false}
                      onPress={() =>
                        setState((current) => adjustIndent(current, unitId, 1))
                      }
                    />
                    <ProofButton
                      label="OUTDENT"
                      selected={false}
                      onPress={() =>
                        setState((current) => adjustIndent(current, unitId, -1))
                      }
                    />
                  </View>
                  <TextInput
                    accessibilityLabel={unit.accessibilityLabel}
                    multiline
                    textAlignVertical="top"
                    style={styles.editor}
                    value={response.document.text}
                    onChangeText={(text) =>
                      setState((current) => updateDraft(current, unit.id, text))
                    }
                    onSelectionChange={(event) =>
                      setSelection(event.nativeEvent.selection)
                    }
                  />
                  <Text style={styles.meta}>
                    Portable formatting ranges: {response.document.marks.length}{" "}
                    · {response.document.blockStyle} · indent{" "}
                    {response.document.indentLevel}
                  </Text>
                </View>
              )}
            <View style={styles.controls}>
              <ProofButton
                label="Save now"
                selected={false}
                onPress={() => void save(state)}
              />
              <ProofButton
                label="Simulate interrupted save"
                selected={false}
                onPress={() =>
                  setState((current) =>
                    failWorkspaceSave(beginWorkspaceSave(current)),
                  )
                }
              />
            </View>
          </View>
        </View>
        <Text style={styles.boundary}>
          Component-remount recovery is proven by this replaceable local
          adapter. Physical-device process-kill and durable encrypted-store
          behavior remain a Native GA test obligation.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

function ProofButton({
  label,
  selected,
  onPress,
}: {
  label: string;
  selected: boolean;
  onPress: () => void;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ selected }}
      style={[styles.control, selected && styles.controlSelected]}
      onPress={onPress}
    >
      <Text
        style={[styles.controlText, selected && styles.controlTextSelected]}
      >
        {label}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  screen: { padding: spacing[4], gap: spacing[3] },
  warning: {
    borderWidth: 2,
    borderColor: "#785c10",
    borderRadius: 10,
    backgroundColor: "#fff8d8",
    padding: spacing[3],
  },
  warningText: { color: "#503c00", fontWeight: "800", lineHeight: 20 },
  eyebrow: {
    color: colors.accent,
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 1.3,
    textTransform: "uppercase",
  },
  title: { color: colors.text, fontSize: 30, fontWeight: "800" },
  meta: { color: colors.muted, fontSize: 12, lineHeight: 18 },
  status: {
    alignSelf: "flex-start",
    color: colors.text,
    backgroundColor: "#e9f5ef",
    borderRadius: 99,
    paddingHorizontal: spacing[3],
    paddingVertical: spacing[2],
    fontWeight: "700",
  },
  controls: { flexDirection: "row", flexWrap: "wrap", gap: spacing[2] },
  control: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 9,
    backgroundColor: "white",
    paddingHorizontal: spacing[3],
    paddingVertical: spacing[2],
    minHeight: 44,
    justifyContent: "center",
  },
  controlSelected: { borderColor: colors.accent, backgroundColor: "#eaf0ff" },
  controlText: { color: colors.accent, fontWeight: "700", fontSize: 12 },
  controlTextSelected: { color: colors.text },
  workspace: { gap: spacing[3] },
  workspaceWide: { flexDirection: "row", alignItems: "flex-start" },
  panel: {
    flex: 1,
    minWidth: 0,
    gap: spacing[3],
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 14,
    backgroundColor: "white",
    padding: spacing[4],
  },
  resource: {
    backgroundColor: colors.background,
    borderRadius: 10,
    padding: spacing[4],
    gap: spacing[2],
  },
  resourceType: {
    color: colors.muted,
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 1,
  },
  panelTitle: { color: colors.text, fontSize: 19, fontWeight: "800" },
  body: { color: colors.text, lineHeight: 23, fontSize: 16 },
  prompt: { color: colors.text, lineHeight: 24, fontSize: 17 },
  choice: {
    minHeight: 52,
    flexDirection: "row",
    alignItems: "center",
    gap: spacing[3],
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 11,
    padding: spacing[3],
  },
  choiceSelected: { borderColor: colors.accent, backgroundColor: "#eaf0ff" },
  choiceLabel: {
    width: 30,
    height: 30,
    borderWidth: 2,
    borderColor: colors.accent,
    borderRadius: 15,
    textAlign: "center",
    lineHeight: 26,
    color: colors.text,
    fontWeight: "800",
  },
  choiceText: { flex: 1, color: colors.text, lineHeight: 21 },
  editor: {
    minHeight: 260,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 11,
    padding: spacing[3],
    color: colors.text,
    backgroundColor: "white",
    fontSize: 16,
    lineHeight: 23,
  },
  boundary: { color: colors.muted, fontSize: 12, lineHeight: 18 },
  errorPanel: {
    margin: spacing[6],
    borderWidth: 2,
    borderColor: "#9f3030",
    padding: spacing[4],
  },
  errorText: { color: "#762020", lineHeight: 22 },
});
