import { FormEvent, useEffect, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { authPaths } from "@barclimb/api-client";
import type { AuthenticatedUser } from "@barclimb/domain-types";
import { authModeForPath, type AuthRouteMode, webRoutes } from "./routes";

export function consumeActionTokenFromFragment(
  pathname = window.location.pathname,
) {
  const actionPaths: string[] = [
    webRoutes.passwordResetCompletion,
    webRoutes.verification,
  ];
  if (!actionPaths.includes(pathname)) return "";
  const token =
    new URLSearchParams(window.location.hash.replace(/^#/, "")).get("token") ??
    "";
  window.history.replaceState(window.history.state, "", pathname);
  return token;
}

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
  let data = null;
  if (response.status !== 204) {
    try {
      data = await response.json();
    } catch {
      data = null;
    }
  }
  if (!response.ok)
    throw new Error(data?.detail ?? "Please check the form and try again.");
  return data;
}

export function App() {
  const location = useLocation();
  const navigate = useNavigate();
  const mode = authModeForPath(location.pathname);
  const [actionToken, setActionToken] = useState(() =>
    consumeActionTokenFromFragment(location.pathname),
  );
  const [user, setUser] = useState<AuthenticatedUser | null>(null);
  const [sessionResolved, setSessionResolved] = useState(false);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    request(authPaths.session)
      .then((data) => setUser(data.user))
      .catch(() => setUser(null))
      .finally(() => setSessionResolved(true));
  }, []);

  if (location.pathname === webRoutes.root)
    return <Navigate replace to={webRoutes.login} />;
  if (!mode)
    return (
      <main>
        <h1>Page not found</h1>
      </main>
    );
  if (mode === "authenticated" && sessionResolved && !user)
    return <Navigate replace to={webRoutes.login} />;

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
          token: actionToken,
          new_password: String(values.password),
        });
        setMessage(data.detail);
        setActionToken("");
        navigate(webRoutes.login, { replace: true });
      } else if (mode === "verify") {
        const data = await request(authPaths.verificationConfirm, {
          token: actionToken,
        });
        setMessage(data.detail);
        setActionToken("");
        request(authPaths.me)
          .then(setUser)
          .catch(() => undefined);
      } else if (mode === "login" || mode === "signup") {
        const payload: Record<string, string> = {
          email: String(values.email),
          password: String(values.password),
        };
        if (mode === "signup") payload.username = String(values.username);
        setUser(
          await request(
            mode === "signup" ? authPaths.signup : authPaths.login,
            payload,
          ),
        );
        navigate(webRoutes.authenticatedProof);
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
    navigate(webRoutes.login, { replace: true });
  }

  return (
    <main>
      <header>
        <span className="mark">B</span>
        <strong>BarClimb</strong>
      </header>
      {mode === "authenticated" && user ? (
        <section className="account-card">
          <p className="eyebrow">My BarClimb</p>
          <h1>Welcome, {user.username}.</h1>
          <p className="private-email">
            {user.email} ·{" "}
            {user.is_email_verified ? "Verified" : "Verification pending"}
          </p>
          {!user.is_email_verified && (
            <p>Check your inbox to verify your private account email.</p>
          )}
          <p className="quiet">
            Learning surfaces are intentionally deferred beyond this milestone.
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
            <h2>{titleFor(mode)}</h2>
            {mode === "signup" && (
              <label>
                Username
                <input name="username" autoComplete="username" required />
              </label>
            )}
            {mode !== "reset" &&
              mode !== "verify" &&
              mode !== "authenticated" && (
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
            {mode !== "forgot" &&
              mode !== "verify" &&
              mode !== "authenticated" && (
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
            {mode !== "authenticated" && (
              <button disabled={busy}>
                {busy ? "Working…" : actionFor(mode)}
              </button>
            )}
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
                    onClick={() => navigate(webRoutes.passwordResetRequest)}
                  >
                    Forgot password?
                  </button>
                  <button
                    type="button"
                    className="text-button"
                    onClick={() => navigate(webRoutes.signup)}
                  >
                    Create account
                  </button>
                </>
              )}
              {mode !== "login" &&
                mode !== "verify" &&
                mode !== "authenticated" && (
                  <button
                    type="button"
                    className="text-button"
                    onClick={() => navigate(webRoutes.login)}
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

function titleFor(mode: AuthRouteMode) {
  return (
    {
      signup: "Create your account",
      forgot: "Reset your password",
      reset: "Choose a new password",
      verify: "Verify your email",
      login: "Welcome back",
      authenticated: "My BarClimb",
    } as const
  )[mode];
}

function actionFor(mode: AuthRouteMode) {
  return (
    {
      signup: "Create account",
      forgot: "Send reset link",
      reset: "Reset password",
      verify: "Verify email",
      login: "Log in",
      authenticated: "Continue",
    } as const
  )[mode];
}
