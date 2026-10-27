# VALIDATE_EVIDENCE — completion gates

Validation is deterministic wherever possible, and cannot be outsourced to model self-assessment.

1. **Schema:** JSON parses; envelope fields and supported enums; evidence coordinates are structurally valid.
2. **Revision:** record source revision per evidence claim; flag wiki/graph SHA vs checkout SHA; stale source evidence cannot establish current-checkout verification.
3. **Manifest:** full source manifest only when derived from authoritative checkout; unique normalized file paths and classifications with explicit inspection statuses.
4. **Counts:** derive from actual arrays; don't trust narrative or model totals. Detect missing, repeated and extra mapped classes independently of file count.
5. **Mappings:** `FULL` means end-to-end inspection of all declared and relevant inherited mappings, not just the snippet read. Include PK, table/column annotations, relation targets and unknowns.
6. **Relationships:** require stable target ID in imported records, or `UNRESOLVED` / `EXTERNAL`; no silent orphan resolution.
7. **Complete:** `discoveryComplete` requires `manifestAuthority=CHECKOUT` and fully classified scoped files; `extractionComplete` requires discovery complete, all mapped source records `FULL` and no unresolved required mapping questions. `relationshipResolutionComplete` can remain false for out-of-scope targets. `businessMappingReviewed` is exclusively a human approval field and must not be asserted by AI Coder.
8. **Conflicts:** treat duplicate IDs, package totals disagreement, shape mismatch and stale wiki data as blocking until reconciled. Keep correction records with `supersedes` or explicit diff.

A validation script is supplied at `scripts/validate_inventory.py`. Run it only if file-system execution is supported; otherwise CWB should run it downstream. Script validation checks consistency of supplied evidence, **not** the truth of inaccessible source files.
