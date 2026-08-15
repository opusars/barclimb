export const webRoutes = {
  root: "/",
  login: "/login",
  signup: "/signup",
  verification: "/verify-email",
  passwordResetRequest: "/forgot-password",
  passwordResetCompletion: "/reset-password",
  authenticatedProof: "/app",
} as const;

export type AuthRouteMode =
  | "login"
  | "signup"
  | "forgot"
  | "reset"
  | "verify"
  | "authenticated";

const modeByPath = new Map<string, AuthRouteMode>([
  [webRoutes.login, "login"],
  [webRoutes.signup, "signup"],
  [webRoutes.verification, "verify"],
  [webRoutes.passwordResetRequest, "forgot"],
  [webRoutes.passwordResetCompletion, "reset"],
  [webRoutes.authenticatedProof, "authenticated"],
]);

export function authModeForPath(pathname: string): AuthRouteMode | null {
  const normalized =
    pathname.length > 1 ? pathname.replace(/\/$/, "") : pathname;
  return modeByPath.get(normalized) ?? null;
}
