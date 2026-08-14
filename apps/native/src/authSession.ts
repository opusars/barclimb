export const NATIVE_SESSION_KEY = "barclimb.native-session.v1";

export type SecureStorage = {
  getItemAsync(key: string, options?: object): Promise<string | null>;
  setItemAsync(key: string, value: string, options?: object): Promise<void>;
  deleteItemAsync(key: string, options?: object): Promise<void>;
};

export function createNativeSessionStore(
  storage: SecureStorage,
  keychainAccessible?: number,
) {
  const options =
    keychainAccessible === undefined ? undefined : { keychainAccessible };
  return {
    restore: () => storage.getItemAsync(NATIVE_SESSION_KEY, options),
    save: (token: string) =>
      storage.setItemAsync(NATIVE_SESSION_KEY, token, options),
    clear: () => storage.deleteItemAsync(NATIVE_SESSION_KEY, options),
  };
}
