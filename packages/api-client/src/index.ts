export type ApiClientConfig = Readonly<{ baseUrl: string }>;
export const apiPath = (config: ApiClientConfig, path: string) =>
  `${config.baseUrl.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;

export const authPaths = {
  csrf: "/api/v1/auth/csrf/",
  login: "/api/v1/auth/login/",
  logout: "/api/v1/auth/logout/",
  me: "/api/v1/auth/me/",
  nativeSession: "/api/v1/auth/native/session/",
  nativeSessionRevoke: "/api/v1/auth/native/session/revoke/",
  nativeSignup: "/api/v1/auth/native/signup/",
  nativePasswordResetRequest: "/api/v1/auth/native/password-reset/request/",
  passwordResetConfirm: "/api/v1/auth/password-reset/confirm/",
  passwordResetRequest: "/api/v1/auth/password-reset/request/",
  session: "/api/v1/auth/session/",
  signup: "/api/v1/auth/signup/",
  verificationConfirm: "/api/v1/auth/verification/confirm/",
  verificationRequest: "/api/v1/auth/verification/request/",
} as const;
