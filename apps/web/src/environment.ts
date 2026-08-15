export type WebClientEnvironment = "local" | "staging" | "production";

type WebEnvironmentInput = Readonly<{
  environment?: string;
  browserOrigin: string;
  localProxyTarget?: string;
}>;

function origin(value: string, label: string) {
  const parsed = new URL(value);
  if (!parsed.hostname || !["http:", "https:"].includes(parsed.protocol)) {
    throw new Error(`${label} must be an HTTP(S) origin`);
  }
  return parsed.origin;
}

export function resolveWebEnvironment(input: WebEnvironmentInput) {
  const environment = (input.environment ?? "local") as WebClientEnvironment;
  if (!["local", "staging", "production"].includes(environment)) {
    throw new Error("VITE_APP_ENV must be local, staging, or production");
  }
  const browserOrigin = origin(input.browserOrigin, "browser origin");
  if (environment !== "local" && !browserOrigin.startsWith("https://")) {
    throw new Error(`${environment} Web must use HTTPS`);
  }
  if (environment !== "local" && input.localProxyTarget) {
    throw new Error(
      "deployed Web must use the same-origin API, not a proxy target",
    );
  }
  return {
    environment,
    apiBaseUrl: "",
    browserOrigin,
    localProxyTarget:
      environment === "local" && input.localProxyTarget
        ? origin(input.localProxyTarget, "local proxy target")
        : undefined,
  } as const;
}
