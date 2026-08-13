export type ApiClientConfig = Readonly<{ baseUrl: string }>;
export const apiPath = (config: ApiClientConfig, path: string) =>
  `${config.baseUrl.replace(/\/$/, "")}/${path.replace(/^\//, "")}`;
