import type { ConfigContext, ExpoConfig } from "expo/config";
import base from "./app.json";

function deployedOrigin(
  value: string | undefined,
  label: string,
  deployed: boolean,
) {
  if (!value) {
    if (deployed)
      throw new Error(`${label} is required for deployed native builds`);
    return label === "EXPO_PUBLIC_API_BASE_URL"
      ? "http://localhost:8000"
      : "http://localhost:5173";
  }
  const parsed = new URL(value);
  if (deployed && parsed.protocol !== "https:")
    throw new Error(`${label} must use HTTPS for deployed native builds`);
  return parsed.origin;
}

export default ({ config }: ConfigContext): ExpoConfig => {
  const environment = process.env.EXPO_PUBLIC_APP_ENV ?? "local";
  if (!["local", "staging", "production"].includes(environment))
    throw new Error(
      "EXPO_PUBLIC_APP_ENV must be local, staging, or production",
    );
  const deployed = environment !== "local";
  deployedOrigin(
    process.env.EXPO_PUBLIC_API_BASE_URL,
    "EXPO_PUBLIC_API_BASE_URL",
    deployed,
  );
  const webBaseUrl = deployedOrigin(
    process.env.EXPO_PUBLIC_WEB_BASE_URL,
    "EXPO_PUBLIC_WEB_BASE_URL",
    deployed,
  );
  const suffix = environment === "production" ? "" : `.${environment}`;
  const supportedPaths = [
    "/app",
    "/practice",
    "/simulate",
    "/progress",
    "/search",
    "/history",
    "/account",
    "/privacy",
  ];
  return {
    ...config,
    ...base.expo,
    scheme:
      environment === "production" ? "barclimb" : `barclimb-${environment}`,
    ios: {
      ...base.expo.ios,
      bundleIdentifier: `com.barclimb.app${suffix}`,
      infoPlist: {
        ...config.ios?.infoPlist,
        ITSAppUsesNonExemptEncryption: false,
      },
      associatedDomains:
        environment === "local" ? [] : [`applinks:${new URL(webBaseUrl).host}`],
    },
    android: {
      ...base.expo.android,
      package: `com.barclimb.app${suffix}`,
      intentFilters:
        environment === "local"
          ? []
          : [
              {
                action: "VIEW",
                autoVerify: true,
                data: supportedPaths.map((pathPrefix) => ({
                  scheme: "https",
                  host: new URL(webBaseUrl).host,
                  pathPrefix,
                })),
                category: ["BROWSABLE", "DEFAULT"],
              },
            ],
    },
  };
};
