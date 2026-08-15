export type NativeEnvironment = "local" | "staging" | "production";

type Input = Readonly<{
  environment?: string;
  apiBaseUrl?: string;
  webBaseUrl?: string;
}>;

function validatedOrigin(value: string, label: string) {
  const parsed = new URL(value);
  if (!["http:", "https:"].includes(parsed.protocol) || !parsed.hostname) {
    throw new Error(`${label} must be an HTTP(S) origin`);
  }
  return parsed.origin;
}

export function resolveNativeEnvironment(input: Input) {
  const environment = (input.environment ?? "local") as NativeEnvironment;
  if (!["local", "staging", "production"].includes(environment)) {
    throw new Error(
      "EXPO_PUBLIC_APP_ENV must be local, staging, or production",
    );
  }
  const apiBaseUrl = validatedOrigin(
    input.apiBaseUrl ?? "http://localhost:8000",
    "API base URL",
  );
  const webBaseUrl = validatedOrigin(
    input.webBaseUrl ?? "http://localhost:5173",
    "Web base URL",
  );
  if (environment !== "local" && (!input.apiBaseUrl || !input.webBaseUrl)) {
    throw new Error(
      `${environment} native builds require explicit API and Web origins`,
    );
  }
  if (
    environment !== "local" &&
    (!apiBaseUrl.startsWith("https://") || !webBaseUrl.startsWith("https://"))
  ) {
    throw new Error(`${environment} native builds require HTTPS origins`);
  }
  return { environment, apiBaseUrl, webBaseUrl } as const;
}

export const nativeEnvironment = resolveNativeEnvironment({
  environment: process.env.EXPO_PUBLIC_APP_ENV,
  apiBaseUrl: process.env.EXPO_PUBLIC_API_BASE_URL,
  webBaseUrl: process.env.EXPO_PUBLIC_WEB_BASE_URL,
});
