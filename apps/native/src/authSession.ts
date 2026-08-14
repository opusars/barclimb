export const NATIVE_SESSION_KEY = "barclimb.native-session.v1";

export type SecureStorage = {
  getItemAsync(key: string, options?: object): Promise<string | null>;
  setItemAsync(key: string, value: string, options?: object): Promise<void>;
  deleteItemAsync(key: string, options?: object): Promise<void>;
};

export class NativeCredentialRejected extends Error {}

export type NativeSessionRestoreResult<User> =
  | { status: "empty" }
  | { status: "valid"; token: string; user: User }
  | { status: "transient"; token: string }
  | { status: "invalid" }
  | { status: "invalid_clear_failed" }
  | { status: "storage_read_failed" };

export type NativeSessionPersistResult =
  | { status: "saved" }
  | { status: "save_failed_revoked" }
  | { status: "save_failed_revoke_unavailable" };

export type NativeSessionLogoutResult =
  | { status: "signed_out" }
  | { status: "revocation_unavailable" }
  | { status: "local_clear_failed_after_revocation" };

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

export async function restoreNativeSession<User>(
  store: ReturnType<typeof createNativeSessionStore>,
  validate: (token: string) => Promise<User>,
): Promise<NativeSessionRestoreResult<User>> {
  let token: string | null;
  try {
    token = await store.restore();
  } catch {
    return { status: "storage_read_failed" };
  }
  if (!token) return { status: "empty" };
  try {
    return { status: "valid", token, user: await validate(token) };
  } catch (error) {
    if (!(error instanceof NativeCredentialRejected)) {
      return { status: "transient", token };
    }
    try {
      await store.clear();
      return { status: "invalid" };
    } catch {
      return { status: "invalid_clear_failed" };
    }
  }
}

export async function persistNativeSession(
  store: ReturnType<typeof createNativeSessionStore>,
  token: string,
  revoke: (token: string) => Promise<boolean>,
): Promise<NativeSessionPersistResult> {
  try {
    await store.save(token);
    return { status: "saved" };
  } catch {
    try {
      if (await revoke(token)) return { status: "save_failed_revoked" };
    } catch {
      // The caller must preserve the distinction from confirmed revocation.
    }
    return { status: "save_failed_revoke_unavailable" };
  }
}

export async function revokeAndClearNativeSession(
  store: ReturnType<typeof createNativeSessionStore>,
  token: string | null,
  revoke: (token: string) => Promise<boolean>,
): Promise<NativeSessionLogoutResult> {
  if (token) {
    try {
      if (!(await revoke(token))) return { status: "revocation_unavailable" };
    } catch {
      return { status: "revocation_unavailable" };
    }
  }
  try {
    await store.clear();
    return { status: "signed_out" };
  } catch {
    return { status: "local_clear_failed_after_revocation" };
  }
}
