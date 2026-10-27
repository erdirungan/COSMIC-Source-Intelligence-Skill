# CWB evidence contract (v1)

The JSON Schema is `cwb-evidence-schema.json`. The schema is intended as an interchange contract; downstream CWB must also enforce source-aware validation, approvals, and per-claim semantic checks.

Required envelope:
- `schemaVersion`: `1.0`; `operation`: supported operation name; `batchId`: stable unique ID for one emitted batch.
- `repository`, `sourceRevision`, `scope`, `manifestAuthority`: `CHECKOUT`, `PARTIAL_INDEX`, or `UNKNOWN`.
- `manifest[]`: file records with `path`, classification and inspection status (may be empty when operation not entity extraction).
- `records[]`: typed evidence records; `kind` one of `technicalEntity`, `businessConcept`, `component`, `interface`, `dependency`, `functionalFlow`, `interaction`, `attributeLineage`, `revisionDelta`.
- `coverage`: counts and four distinct completion booleans. Counts may use null if not provable; never fabricate a zero.
- `checkpoint`: `nextPaths[]`, `completedPaths[]`, `remainingPaths[]`, `resumeInstructions`.
- `unresolvedQuestions[]`: string questions with optional explicit links to records, NEVER silently dropped.

For each `technicalEntity` record, `attributes[]` and `relationships[]` are typed. Evidence uses `repository`, `path`, `startLine`, `endLine`, `sourceRevision`, and `verification`. If source lines are not inspectable, do not fabricate an evidence span; report unknown/partial.

An import merges by record ID + sourceRevision and batchId, not by simple class name. A later correction should name the affected stable ID and use `supersedes` to identify a batch/version, rather than silently overwriting approved canonical data. Store raw imports and validation results separately from published records.
