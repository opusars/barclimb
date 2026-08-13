export type ApiClientConfig = Readonly<{ baseUrl: string }>;
export const apiPath = (config: ApiClientConfig, path: string) =>
  new URL(
    path.replace(/^\//, ""),
    `${config.baseUrl.replace(/\/$/, "")}/`,
  ).toString();
