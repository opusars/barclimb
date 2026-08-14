/** Infrastructure-only marker. Product domain contracts arrive in their owning milestones. */
export type ClientPlatform = "web" | "ios" | "android";

/** Private account view returned only to the authenticated account. */
export type AuthenticatedUser = Readonly<{
  id: number;
  username: string;
  email: string;
  is_email_verified: boolean;
}>;
