import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import * as SecureStore from "expo-secure-store";
import { authPaths } from "@barclimb/api-client";
import type { AuthenticatedUser } from "@barclimb/domain-types";
import { colors, spacing } from "@barclimb/design-tokens";
import {
  createNativeSessionStore,
  NativeCredentialRejected,
  type NativeSessionRestoreResult,
  persistNativeSession,
  revokeAndClearNativeSession,
  restoreNativeSession,
} from "./src/authSession";

const API_BASE_URL = (
  process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://localhost:8000"
)
  .replace(/\/api\/v1\/?$/, "")
  .replace(/\/$/, "");
type Mode = "login" | "signup" | "forgot";

type NativeAuthResponse = {
  detail?: string;
  token?: string;
  user?: AuthenticatedUser;
};

async function authenticatedUser(credential: string) {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${authPaths.me}`, {
      headers: { Authorization: `Bearer ${credential}` },
    });
  } catch {
    throw new Error("session validation unavailable");
  }
  if (response.status === 401 || response.status === 403)
    throw new NativeCredentialRejected("invalid native credential");
  if (!response.ok) throw new Error("session validation unavailable");
  return (await response.json()) as AuthenticatedUser;
}

async function revokeServerSession(credential: string) {
  const response = await fetch(
    `${API_BASE_URL}${authPaths.nativeSessionRevoke}`,
    {
      method: "POST",
      headers: { Authorization: `Bearer ${credential}` },
    },
  );
  return response.ok || response.status === 401 || response.status === 403;
}

export default function App() {
  const store = useMemo(
    () =>
      createNativeSessionStore(
        SecureStore,
        SecureStore.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
      ),
    [],
  );
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const applyRestoredSession = useCallback(
    (restored: NativeSessionRestoreResult<AuthenticatedUser>) => {
      if (restored.status === "valid") {
        setUser(restored.user);
        setToken(restored.token);
        setMessage("");
      } else if (restored.status === "transient") {
        setUser(null);
        setToken(restored.token);
        setMessage("Your saved session is preserved. Reconnect and try again.");
      } else {
        setUser(null);
        setToken(null);
        if (restored.status === "invalid") {
          setMessage("Your session has expired. Please log in again.");
        } else if (restored.status === "invalid_clear_failed") {
          setMessage(
            "Your session is no longer valid, but secure storage could not remove it. Try again.",
          );
        } else if (restored.status === "storage_read_failed") {
          setMessage(
            "Secure storage is unavailable. Restart the app and try again.",
          );
        } else {
          setMessage("");
        }
      }
      setLoading(false);
    },
    [],
  );

  const restoreSession = useCallback(async () => {
    setLoading(true);
    applyRestoredSession(await restoreNativeSession(store, authenticatedUser));
  }, [applyRestoredSession, store]);

  useEffect(() => {
    let mounted = true;
    void restoreNativeSession(store, authenticatedUser).then((restored) => {
      if (mounted) applyRestoredSession(restored);
    });
    return () => {
      mounted = false;
    };
  }, [applyRestoredSession, store]);

  async function submit() {
    setLoading(true);
    setMessage("");
    try {
      const endpoint =
        mode === "signup"
          ? authPaths.nativeSignup
          : mode === "forgot"
            ? authPaths.nativePasswordResetRequest
            : authPaths.nativeSession;
      const payload =
        mode === "signup"
          ? { email, username, password }
          : mode === "forgot"
            ? { email }
            : { email, password };
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      let data: NativeAuthResponse = {};
      try {
        data = await response.json();
      } catch {
        data = {};
      }
      if (!response.ok) throw new Error(data.detail ?? "Unable to continue.");
      if (mode === "forgot") {
        setMessage(
          data.detail ?? "If that account exists, a reset link is on its way.",
        );
      } else {
        if (!data.token || !data.user)
          throw new Error("The authentication response was incomplete.");
        const persisted = await persistNativeSession(
          store,
          data.token,
          revokeServerSession,
        );
        if (persisted.status !== "saved") {
          setMessage(
            persisted.status === "save_failed_revoked"
              ? "Secure storage could not save this session. The server session was revoked."
              : "Secure storage could not save this session, and server revocation is unavailable. Try again after reconnecting.",
          );
          setToken(null);
          setUser(null);
          setPassword("");
          return;
        }
        setToken(data.token);
        setUser(data.user);
        setPassword("");
      }
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Unable to continue.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function logout() {
    const result = await revokeAndClearNativeSession(
      store,
      token,
      revokeServerSession,
    );
    if (result.status === "revocation_unavailable") {
      setMessage("Connect to the internet to sign out securely.");
      return;
    }
    setToken(null);
    setUser(null);
    setMessage(
      result.status === "local_clear_failed_after_revocation"
        ? "Signed out on the server, but secure storage could not remove the local credential. Try again."
        : "",
    );
  }

  if (loading)
    return (
      <SafeAreaView style={styles.center}>
        <ActivityIndicator color={colors.accent} />
      </SafeAreaView>
    );
  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.brandRow}>
          <View style={styles.mark}>
            <Text style={styles.markText}>B</Text>
          </View>
          <Text style={styles.brand}>BarClimb</Text>
        </View>
        {user ? (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>Identity foundation</Text>
            <Text style={styles.title}>Welcome, {user.username}.</Text>
            <Text style={styles.muted}>{user.email}</Text>
            <Text style={styles.body}>
              {user.is_email_verified
                ? "Email verified"
                : "Check your inbox to verify your email."}
            </Text>
            <Text style={styles.muted}>
              The learning experience begins in a later milestone.
            </Text>
            {message ? (
              <Text accessibilityRole="alert" style={styles.message}>
                {message}
              </Text>
            ) : null}
            <Pressable
              accessibilityRole="button"
              style={styles.button}
              onPress={logout}
            >
              <Text style={styles.buttonText}>Sign out</Text>
            </Pressable>
          </View>
        ) : (
          <View style={styles.card}>
            <Text style={styles.eyebrow}>Secure account</Text>
            <Text style={styles.title}>
              {mode === "signup"
                ? "Create your account"
                : mode === "forgot"
                  ? "Reset your password"
                  : "Welcome back"}
            </Text>
            <Text style={styles.body}>
              One BarClimb identity follows you across every device.
            </Text>
            {mode === "signup" ? (
              <>
                <Text style={styles.label}>Username</Text>
                <TextInput
                  autoCapitalize="none"
                  autoComplete="username-new"
                  onChangeText={setUsername}
                  style={styles.input}
                  value={username}
                />
              </>
            ) : null}
            <Text style={styles.label}>Email</Text>
            <TextInput
              autoCapitalize="none"
              autoComplete="email"
              keyboardType="email-address"
              onChangeText={setEmail}
              style={styles.input}
              value={email}
            />
            {mode !== "forgot" ? (
              <>
                <Text style={styles.label}>Password</Text>
                <TextInput
                  autoCapitalize="none"
                  autoComplete={
                    mode === "signup" ? "password-new" : "current-password"
                  }
                  onChangeText={setPassword}
                  secureTextEntry
                  style={styles.input}
                  value={password}
                />
              </>
            ) : null}
            {message ? (
              <Text accessibilityRole="alert" style={styles.message}>
                {message}
              </Text>
            ) : null}
            {token ? (
              <Pressable
                accessibilityRole="button"
                style={styles.secondaryButton}
                onPress={restoreSession}
              >
                <Text style={styles.modeLink}>Retry saved session</Text>
              </Pressable>
            ) : null}
            <Pressable
              accessibilityRole="button"
              style={styles.button}
              onPress={submit}
            >
              <Text style={styles.buttonText}>
                {mode === "signup"
                  ? "Create account"
                  : mode === "forgot"
                    ? "Send reset link"
                    : "Log in"}
              </Text>
            </Pressable>
            <View style={styles.modeRow}>
              {mode === "login" ? (
                <>
                  <Pressable onPress={() => setMode("forgot")}>
                    <Text style={styles.modeLink}>Forgot password?</Text>
                  </Pressable>
                  <Pressable onPress={() => setMode("signup")}>
                    <Text style={styles.modeLink}>Create account</Text>
                  </Pressable>
                </>
              ) : (
                <Pressable onPress={() => setMode("login")}>
                  <Text style={styles.modeLink}>Back to login</Text>
                </Pressable>
              )}
            </View>
            <Text style={styles.footnote}>
              Verification and reset links open securely on barclimb.com.
            </Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  center: {
    flex: 1,
    backgroundColor: colors.background,
    justifyContent: "center",
  },
  content: {
    flexGrow: 1,
    padding: spacing[6],
    justifyContent: "center",
    gap: spacing[8],
  },
  brandRow: { flexDirection: "row", alignItems: "center", gap: spacing[3] },
  mark: {
    width: 38,
    height: 38,
    borderRadius: 11,
    backgroundColor: colors.accent,
    alignItems: "center",
    justifyContent: "center",
  },
  markText: { color: "white", fontWeight: "800", fontSize: 18 },
  brand: { fontSize: 19, fontWeight: "800", color: colors.text },
  card: {
    backgroundColor: "white",
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 22,
    padding: spacing[6],
    gap: spacing[3],
  },
  eyebrow: {
    color: colors.accent,
    textTransform: "uppercase",
    letterSpacing: 1.5,
    fontWeight: "800",
    fontSize: 12,
  },
  title: {
    fontSize: 34,
    lineHeight: 40,
    fontWeight: "700",
    color: colors.text,
  },
  body: { color: colors.text, lineHeight: 22 },
  muted: { color: colors.muted, lineHeight: 22 },
  label: { color: colors.text, fontWeight: "700", marginTop: spacing[2] },
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 11,
    padding: spacing[3],
    fontSize: 16,
    color: colors.text,
  },
  button: {
    backgroundColor: colors.accent,
    borderRadius: 11,
    alignItems: "center",
    padding: spacing[4],
    marginTop: spacing[3],
  },
  buttonText: { color: "white", fontWeight: "800" },
  secondaryButton: { alignItems: "center", padding: spacing[3] },
  message: { color: "#8b2e2e", lineHeight: 20 },
  modeRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    gap: spacing[3],
  },
  modeLink: { color: colors.accent, fontWeight: "700" },
  footnote: {
    color: colors.muted,
    fontSize: 12,
    lineHeight: 18,
    textAlign: "center",
  },
});
