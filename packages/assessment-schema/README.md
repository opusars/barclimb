# Assessment schema boundary

M1.5 proves one JSON-serializable presentation and workspace-state contract for
React Web and React Native. It contains no React, DOM, React Native, grading,
curriculum, learner-evidence, or production-attempt dependency.

`m15AssessmentFixtures` are runtime-validated `TEST_FIXTURE` /
`DEVELOPMENT_ONLY` synthetic payloads. They are bundled only for the bounded
presentation spike and are not assessment inventory, publication data, learner
evidence, or readiness input.

The persistence interface intentionally defines only local snapshot read/write.
It proves unsaved, pending, saved, recoverable-failure, and restored states. It
does not define cross-device concurrency, authoritative server versions, or
conflict resolution; those remain production attempt-system work.
