import { describe, expect, it, vi } from "vitest";
import { createNativeSessionStore, NATIVE_SESSION_KEY } from "./authSession";

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
});
