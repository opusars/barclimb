import { describe, expect, it, vi } from "vitest";
import {
  createNativeSessionStore,
  NativeCredentialRejected,
  NATIVE_SESSION_KEY,
  persistNativeSession,
  revokeAndClearNativeSession,
  restoreNativeSession,
} from "./authSession";

describe("native secure session store", () => {
  it("restores, writes, and removes only the opaque session credential", async () => {
    const storage = {
      getItemAsync: vi.fn().mockResolvedValue("opaque-token"),
      setItemAsync: vi.fn().mockResolvedValue(undefined),
      deleteItemAsync: vi.fn().mockResolvedValue(undefined),
    };
    const store = createNativeSessionStore(storage);
    await expect(store.restore()).resolves.toBe("opaque-token");
    await store.save("next-token");
    await store.clear();
    expect(storage.setItemAsync).toHaveBeenCalledWith(
      NATIVE_SESSION_KEY,
      "next-token",
      undefined,
    );
    expect(storage.deleteItemAsync).toHaveBeenCalledWith(
      NATIVE_SESSION_KEY,
      undefined,
    );
  });

  it("restores a valid credential", async () => {
    const storage = {
      getItemAsync: vi.fn().mockResolvedValue("opaque-token"),
      setItemAsync: vi.fn(),
      deleteItemAsync: vi.fn(),
    };
    const result = await restoreNativeSession(
      createNativeSessionStore(storage),
      vi.fn().mockResolvedValue({ username: "climber" }),
    );
    expect(result).toEqual({
      status: "valid",
      token: "opaque-token",
      user: { username: "climber" },
    });
  });

  it.each(["offline", "server 5xx"])(
    "preserves a credential after a transient %s validation failure",
    async (failure) => {
      const storage = {
        getItemAsync: vi.fn().mockResolvedValue("opaque-token"),
        setItemAsync: vi.fn(),
        deleteItemAsync: vi.fn(),
      };
      const result = await restoreNativeSession(
        createNativeSessionStore(storage),
        vi.fn().mockRejectedValue(new Error(failure)),
      );
      expect(result).toEqual({ status: "transient", token: "opaque-token" });
      expect(storage.deleteItemAsync).not.toHaveBeenCalled();
    },
  );

  it("removes only an authoritatively rejected credential", async () => {
    const storage = {
      getItemAsync: vi.fn().mockResolvedValue("opaque-token"),
      setItemAsync: vi.fn(),
      deleteItemAsync: vi.fn().mockResolvedValue(undefined),
    };
    const result = await restoreNativeSession(
      createNativeSessionStore(storage),
      vi.fn().mockRejectedValue(new NativeCredentialRejected("expired")),
    );
    expect(result).toEqual({ status: "invalid" });
    expect(storage.deleteItemAsync).toHaveBeenCalledOnce();
  });

  it.each([
    ["read", "storage_read_failed"],
    ["delete", "invalid_clear_failed"],
  ])(
    "terminates cleanly after a SecureStore %s rejection",
    async (failure, status) => {
      const storage = {
        getItemAsync:
          failure === "read"
            ? vi.fn().mockRejectedValue(new Error("storage unavailable"))
            : vi.fn().mockResolvedValue("opaque-token"),
        setItemAsync: vi.fn(),
        deleteItemAsync: vi
          .fn()
          .mockRejectedValue(new Error("storage unavailable")),
      };
      const result = await restoreNativeSession(
        createNativeSessionStore(storage),
        vi.fn().mockRejectedValue(new NativeCredentialRejected("expired")),
      );
      expect(result.status).toBe(status);
    },
  );

  it.each([
    [true, "save_failed_revoked"],
    [false, "save_failed_revoke_unavailable"],
  ])(
    "distinguishes a SecureStore write failure when revocation is %s",
    async (revoked, status) => {
      const storage = {
        getItemAsync: vi.fn(),
        setItemAsync: vi
          .fn()
          .mockRejectedValue(new Error("storage unavailable")),
        deleteItemAsync: vi.fn(),
      };
      const revoke = vi.fn().mockResolvedValue(revoked);
      const result = await persistNativeSession(
        createNativeSessionStore(storage),
        "new-token",
        revoke,
      );
      expect(result.status).toBe(status);
      expect(revoke).toHaveBeenCalledWith("new-token");
    },
  );

  it("reports successful server revocation and local deletion", async () => {
    const storage = {
      getItemAsync: vi.fn(),
      setItemAsync: vi.fn(),
      deleteItemAsync: vi.fn().mockResolvedValue(undefined),
    };
    const result = await revokeAndClearNativeSession(
      createNativeSessionStore(storage),
      "opaque-token",
      vi.fn().mockResolvedValue(true),
    );
    expect(result).toEqual({ status: "signed_out" });
    expect(storage.deleteItemAsync).toHaveBeenCalledOnce();
  });

  it("preserves local state when server revocation is unavailable", async () => {
    const storage = {
      getItemAsync: vi.fn(),
      setItemAsync: vi.fn(),
      deleteItemAsync: vi.fn(),
    };
    const result = await revokeAndClearNativeSession(
      createNativeSessionStore(storage),
      "opaque-token",
      vi.fn().mockRejectedValue(new Error("offline")),
    );
    expect(result).toEqual({ status: "revocation_unavailable" });
    expect(storage.deleteItemAsync).not.toHaveBeenCalled();
  });

  it("reports local deletion failure after confirmed server revocation", async () => {
    const storage = {
      getItemAsync: vi.fn(),
      setItemAsync: vi.fn(),
      deleteItemAsync: vi
        .fn()
        .mockRejectedValue(new Error("storage unavailable")),
    };
    const result = await revokeAndClearNativeSession(
      createNativeSessionStore(storage),
      "opaque-token",
      vi.fn().mockResolvedValue(true),
    );
    expect(result).toEqual({
      status: "local_clear_failed_after_revocation",
    });
  });
});
