import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { colors, spacing } from "@barclimb/design-tokens";
import "./styles.css";

function App() {
  return (
    <main style={{ padding: spacing[6] }}>
      <header>
        <strong>BarClimb</strong>
      </header>
      <section className="shell" style={{ borderColor: colors.accent }}>
        <p className="eyebrow">Foundation build</p>
        <h1>Multi-client shell is ready for Milestone 1 work.</h1>
        <p>No learner features are implemented in M1.1.</p>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
