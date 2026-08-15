import { useCallback, useEffect, useMemo, useState } from "react";
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import * as SecureStore from "expo-secure-store";
import * as Linking from "expo-linking";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { SafeAreaProvider, SafeAreaView } from "react-native-safe-area-context";
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
import { nativeEnvironment } from "./src/environment";

type AuthMode = "login" | "signup" | "forgot";
type AuthStackParams = {
  Login: undefined;
  Signup: undefined;
  ForgotPassword: undefined;
};
type AppTabParams = {
  Home: undefined;
  Practice: undefined;
  Simulate: undefined;
  Progress: undefined;
};
const AuthStack = createNativeStackNavigator<AuthStackParams>();
const AppTabs = createBottomTabNavigator<AppTabParams>();

type NativeAuthResponse = {
  detail?: string;
  token?: string;
  user?: AuthenticatedUser;
};

async function authenticatedUser(credential: string) {
  let response: Response;
  try {
    response = await fetch(`${nativeEnvironment.apiBaseUrl}${authPaths.me}`, {
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
    `${nativeEnvironment.apiBaseUrl}${authPaths.nativeSessionRevoke}`,
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
        if (restored.status === "invalid")
          setMessage("Your session has expired. Please log in again.");
        else if (restored.status === "invalid_clear_failed")
          setMessage(
            "Your session is no longer valid, but secure storage could not remove it. Try again.",
          );
        else if (restored.status === "storage_read_failed")
          setMessage(
            "Secure storage is unavailable. Restart the app and try again.",
          );
        else setMessage("");
      }
      setLoading(false);
    },
    [],
  );

  const retrySavedSession = useCallback(async () => {
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

  async function authenticated(nextToken: string, nextUser: AuthenticatedUser) {
    const persisted = await persistNativeSession(
      store,
      nextToken,
      revokeServerSession,
    );
    if (persisted.status !== "saved") {
      setMessage(
        persisted.status === "save_failed_revoked"
          ? "Secure storage could not save this session. The server session was revoked."
          : "Secure storage could not save this session, and server revocation is unavailable. Try again after reconnecting.",
      );
      return false;
    }
    setToken(nextToken);
    setUser(nextUser);
    setMessage("");
    return true;
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

  const linking = {
    prefixes: [Linking.createURL("/"), nativeEnvironment.webBaseUrl],
    config: {
      screens: {
        Home: "app",
        Practice: "practice",
        Simulate: "simulate",
        Progress: "progress",
      },
    },
  };

  if (loading)
    return (
      <SafeAreaProvider>
        <SafeAreaView style={styles.center}>
          <ActivityIndicator color={colors.accent} />
        </SafeAreaView>
      </SafeAreaProvider>
    );
  return (
    <SafeAreaProvider>
      <NavigationContainer linking={linking}>
        {user ? (
          <AppTabs.Navigator>
            <AppTabs.Screen name="Home">
              {() => (
                <HomeScreen user={user} message={message} logout={logout} />
              )}
            </AppTabs.Screen>
            <AppTabs.Screen name="Practice">
              {() => <DeferredScreen title="Practice" />}
            </AppTabs.Screen>
            <AppTabs.Screen name="Simulate">
              {() => <DeferredScreen title="Simulate" />}
            </AppTabs.Screen>
            <AppTabs.Screen name="Progress">
              {() => <DeferredScreen title="Progress" />}
            </AppTabs.Screen>
          </AppTabs.Navigator>
        ) : (
          <AuthStack.Navigator>
            <AuthStack.Screen name="Login">
              {({ navigation }) => (
                <AuthScreen
                  mode="login"
                  message={message}
                  savedToken={token}
                  onAuthenticated={authenticated}
                  onRetry={retrySavedSession}
                  onNavigate={(mode) =>
                    navigation.navigate(
                      mode === "signup" ? "Signup" : "ForgotPassword",
                    )
                  }
                />
              )}
            </AuthStack.Screen>
            <AuthStack.Screen name="Signup">
              {({ navigation }) => (
                <AuthScreen
                  mode="signup"
                  message={message}
                  savedToken={token}
                  onAuthenticated={authenticated}
                  onRetry={retrySavedSession}
                  onNavigate={() => navigation.navigate("Login")}
                />
              )}
            </AuthStack.Screen>
            <AuthStack.Screen name="ForgotPassword">
              {({ navigation }) => (
                <AuthScreen
                  mode="forgot"
                  message={message}
                  savedToken={token}
                  onAuthenticated={authenticated}
                  onRetry={retrySavedSession}
                  onNavigate={() => navigation.navigate("Login")}
                />
              )}
            </AuthStack.Screen>
          </AuthStack.Navigator>
        )}
      </NavigationContainer>
    </SafeAreaProvider>
  );
}

function AuthScreen(props: {
  mode: AuthMode;
  message: string;
  savedToken: string | null;
  onAuthenticated: (token: string, user: AuthenticatedUser) => Promise<boolean>;
  onRetry: () => Promise<void>;
  onNavigate: (mode: AuthMode) => void;
}) {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [localMessage, setLocalMessage] = useState("");

  async function submit() {
    setBusy(true);
    setLocalMessage("");
    try {
      const endpoint =
        props.mode === "signup"
          ? authPaths.nativeSignup
          : props.mode === "forgot"
            ? authPaths.nativePasswordResetRequest
            : authPaths.nativeSession;
      const payload =
        props.mode === "signup"
          ? { email, username, password }
          : props.mode === "forgot"
            ? { email }
            : { email, password };
      const response = await fetch(
        `${nativeEnvironment.apiBaseUrl}${endpoint}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        },
      );
      let data: NativeAuthResponse = {};
      try {
        data = await response.json();
      } catch {
        data = {};
      }
      if (!response.ok) throw new Error(data.detail ?? "Unable to continue.");
      if (props.mode === "forgot")
        setLocalMessage(
          data.detail ?? "If that account exists, a reset link is on its way.",
        );
      else {
        if (!data.token || !data.user)
          throw new Error("The authentication response was incomplete.");
        if (await props.onAuthenticated(data.token, data.user)) setPassword("");
      }
    } catch (error) {
      setLocalMessage(
        error instanceof Error ? error.message : "Unable to continue.",
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
      >
        <Brand />
        <View style={styles.card}>
          <Text style={styles.eyebrow}>Secure account</Text>
          <Text style={styles.title}>
            {props.mode === "signup"
              ? "Create your account"
              : props.mode === "forgot"
                ? "Reset your password"
                : "Welcome back"}
          </Text>
          <Text style={styles.body}>
            One BarClimb identity follows you across every device.
          </Text>
          {props.mode === "signup" && (
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
          )}
          <Text style={styles.label}>Email</Text>
          <TextInput
            autoCapitalize="none"
            autoComplete="email"
            keyboardType="email-address"
            onChangeText={setEmail}
            style={styles.input}
            value={email}
          />
          {props.mode !== "forgot" && (
            <>
              <Text style={styles.label}>Password</Text>
              <TextInput
                autoCapitalize="none"
                autoComplete={
                  props.mode === "signup" ? "password-new" : "current-password"
                }
                onChangeText={setPassword}
                secureTextEntry
                style={styles.input}
                value={password}
              />
            </>
          )}
          {(localMessage || props.message) && (
            <Text accessibilityRole="alert" style={styles.message}>
              {localMessage || props.message}
            </Text>
          )}
          {props.savedToken && (
            <Pressable style={styles.secondaryButton} onPress={props.onRetry}>
              <Text style={styles.modeLink}>Retry saved session</Text>
            </Pressable>
          )}
          <Pressable
            disabled={busy}
            accessibilityRole="button"
            style={styles.button}
            onPress={submit}
          >
            <Text style={styles.buttonText}>
              {busy
                ? "Working…"
                : props.mode === "signup"
                  ? "Create account"
                  : props.mode === "forgot"
                    ? "Send reset link"
                    : "Log in"}
            </Text>
          </Pressable>
          <View style={styles.modeRow}>
            {props.mode === "login" ? (
              <>
                <Pressable onPress={() => props.onNavigate("forgot")}>
                  <Text style={styles.modeLink}>Forgot password?</Text>
                </Pressable>
                <Pressable onPress={() => props.onNavigate("signup")}>
                  <Text style={styles.modeLink}>Create account</Text>
                </Pressable>
              </>
            ) : (
              <Pressable onPress={() => props.onNavigate("login")}>
                <Text style={styles.modeLink}>Back to login</Text>
              </Pressable>
            )}
          </View>
          <Text style={styles.footnote}>
            Credential-bearing verification and reset links complete securely on
            the canonical Web origin.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function HomeScreen({
  user,
  message,
  logout,
}: {
  user: AuthenticatedUser;
  message: string;
  logout: () => Promise<void>;
}) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.content}>
        <Brand />
        <View style={styles.card}>
          <Text style={styles.eyebrow}>My BarClimb</Text>
          <Text style={styles.title}>Welcome, {user.username}.</Text>
          <Text style={styles.muted}>{user.email}</Text>
          <Text style={styles.body}>
            {user.is_email_verified
              ? "Email verified"
              : "Check your inbox to verify your email."}
          </Text>
          <Text style={styles.muted}>
            Learning surfaces are intentionally deferred beyond this milestone.
          </Text>
          {message && (
            <Text accessibilityRole="alert" style={styles.message}>
              {message}
            </Text>
          )}
          <Pressable
            accessibilityRole="button"
            style={styles.button}
            onPress={logout}
          >
            <Text style={styles.buttonText}>Sign out</Text>
          </Pressable>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function DeferredScreen({ title }: { title: string }) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.content}>
        <Brand />
        <View style={styles.card}>
          <Text style={styles.eyebrow}>Navigation proof</Text>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.muted}>
            This destination is reserved; product behavior begins in a later
            milestone.
          </Text>
        </View>
      </View>
    </SafeAreaView>
  );
}

function Brand() {
  return (
    <View style={styles.brandRow}>
      <View style={styles.mark}>
        <Text style={styles.markText}>B</Text>
      </View>
      <Text style={styles.brand}>BarClimb</Text>
    </View>
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
