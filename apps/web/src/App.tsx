import { FormEvent, useEffect, useState } from "react";
import { authPaths } from "@barclimb/api-client";
import type { AuthenticatedUser } from "@barclimb/domain-types";

type Mode = "login" | "signup" | "forgot" | "reset" | "verify";

async function csrfToken() {
  const response = await fetch(authPaths.csrf, { credentials: "same-origin" });
  return ((await response.json()) as { csrf_token: string }).csrf_token;
}

async function request(path: string, body?: Record<string, string>) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (body) headers["X-CSRFToken"] = await csrfToken();
  const response = await fetch(path, {
    method: body ? "POST" : "GET",
    credentials: "same-origin",
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = response.status === 204 ? null : await response.json();
  if (!response.ok)
    throw new Error(data?.detail ?? "Please check the form and try again.");
  return data;
}

export function App() {
  const query = new URLSearchParams(window.location.search);
  const initialMode: Mode = window.location.pathname.includes("reset-password")
    ? "reset"
    : window.location.pathname.includes("verify-email")
      ? "verify"
      : "login";
  const [mode, setMode] = useState<Mode>(initialMode);
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    request(authPaths.session)
      .then((data) => setUser(data.user))
      .catch(() => setUser(null));
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setMessage("");
    const values = Object.fromEntries(new FormData(event.currentTarget));
    try {
      if (mode === "forgot") {
        const data = await request(authPaths.passwordResetRequest, {
          email: String(values.email),
        });
        setMessage(data.detail);
      } else if (mode === "reset") {
        const data = await request(authPaths.passwordResetConfirm, {
          token: query.get("token") ?? "",
          new_password: String(values.password),
        });
        setMessage(data.detail);
        setMode("login");
      } else if (mode === "verify") {
        const data = await request(authPaths.verificationConfirm, {
          token: query.get("token") ?? "",
        });
        setMessage(data.detail);
        request(authPaths.me)
          .then(setUser)
          .catch(() => undefined);
      } else {
        const path = mode === "signup" ? authPaths.signup : authPaths.login;
        const payload: Record<string, string> = {
          email: String(values.email),
          password: String(values.password),
        };
        if (mode === "signup") payload.username = String(values.username);
        setUser(await request(path, payload));
      }
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Something went wrong.",
      );
    } finally {
      setBusy(false);
    }
  }

  async function signOut() {
    await request(authPaths.logout, {});
    setUser(null);
    setMode("login");
  }

  return (
    <main>
      <header>
        <span className="mark">B</span>
        <strong>BarClimb</strong>
      </header>
      {user ? (
        <section className="account-card">
          <p className="eyebrow">Identity foundation</p>
          <h1>Welcome, {user.username}.</h1>
          <p className="private-email">
            {user.email} ·{" "}
            {user.is_email_verified ? "Verified" : "Verification pending"}
          </p>
          {!user.is_email_verified && (
            <p>Check your inbox to verify your private account email.</p>
          )}
          <p className="quiet">
            The learning experience begins in a later milestone.
          </p>
          <button onClick={signOut}>Sign out</button>
        </section>
      ) : (
        <section className="auth-layout">
          <div className="promise">
            <p className="eyebrow">Build your way up</p>
            <h1>
              Your bar preparation should feel clear, personal, and achievable.
            </h1>
            <p>
              One secure BarClimb identity follows you across Web, iOS, and
              Android.
            </p>
          </div>
          <form className="auth-card" onSubmit={submit}>
            <p className="eyebrow">Secure account</p>
            <h2>
              {mode === "signup"
                ? "Create your account"
                : mode === "forgot"
                  ? "Reset your password"
                  : mode === "reset"
                    ? "Choose a new password"
                    : mode === "verify"
                      ? "Verify your email"
                      : "Welcome back"}
            </h2>
            {mode === "signup" && (
              <label>
                Username
                <input name="username" autoComplete="username" required />
              </label>
            )}
            {mode !== "reset" && mode !== "verify" && (
              <label>
                Email
                <input
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                />
              </label>
            )}
            {mode !== "forgot" && mode !== "verify" && (
              <label>
                Password
                <input
                  name="password"
                  type="password"
                  autoComplete={
                    mode === "signup" ? "new-password" : "current-password"
                  }
                  required
                />
              </label>
            )}
            <button disabled={busy}>
              {busy
                ? "Working…"
                : mode === "signup"
                  ? "Create account"
                  : mode === "forgot"
                    ? "Send reset link"
                    : mode === "reset"
                      ? "Reset password"
                      : mode === "verify"
                        ? "Verify email"
                        : "Log in"}
            </button>
            {message && (
              <p role="status" className="message">
                {message}
              </p>
            )}
            <nav>
              {mode === "login" && (
                <>
                  <button
                    type="button"
                    className="text-button"
                    onClick={() => setMode("forgot")}
                  >
                    Forgot password?
                  </button>
                  <button
                    type="button"
                    className="text-button"
                    onClick={() => setMode("signup")}
                  >
                    Create account
                  </button>
                </>
              )}
              {mode !== "login" && mode !== "verify" && (
                <button
                  type="button"
                  className="text-button"
                  onClick={() => setMode("login")}
                >
                  Back to login
                </button>
              )}
            </nav>
          </form>
        </section>
      )}
    </main>
  );
}
