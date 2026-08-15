export const nativeAppPaths = [
  "/app",
  "/practice",
  "/simulate",
  "/progress",
  "/search",
  "/history",
  "/account",
  "/privacy",
] as const;
export const webOnlyCredentialPaths = [
  "/verify-email",
  "/reset-password",
] as const;

export type CanonicalLinkResolution =
  | { kind: "native"; path: (typeof nativeAppPaths)[number] }
  | { kind: "web_only_auth"; path: (typeof webOnlyCredentialPaths)[number] }
  | { kind: "web_fallback"; url: string };

export function resolveCanonicalLink(
  rawUrl: string,
  canonicalWebOrigin: string,
): CanonicalLinkResolution {
  const candidate = new URL(rawUrl);
  const origin = new URL(canonicalWebOrigin).origin;
  if (candidate.origin !== origin)
    throw new Error("link is outside the canonical Web origin");
  const cleanUrl = `${candidate.origin}${candidate.pathname}`;
  if (
    (webOnlyCredentialPaths as readonly string[]).includes(candidate.pathname)
  ) {
    return {
      kind: "web_only_auth",
      path: candidate.pathname as (typeof webOnlyCredentialPaths)[number],
    };
  }
  if ((nativeAppPaths as readonly string[]).includes(candidate.pathname)) {
    return {
      kind: "native",
      path: candidate.pathname as (typeof nativeAppPaths)[number],
    };
  }
  return { kind: "web_fallback", url: cleanUrl };
}
