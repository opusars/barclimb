/** Event names are introduced with implemented product behavior, not guessed in M1.1. */
export type AnalyticsEventEnvelope = Readonly<{
  name: string;
  client: "web" | "ios" | "android";
}>;
