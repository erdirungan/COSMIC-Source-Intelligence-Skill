# EXTRACT_ENTITIES

## Inventory boundaries

Use an explicit repo, revision, module/package scope. Default batch size 5 files and an explicit file manifest. If checkout access exists, enumerate recursively from filesystem/git at the pinned commit; do NOT infer the file list from `grep_code`, `get_table`, `search_graph`, or wiki. If no checkout manifest is available, report `manifestAuthority=PARTIAL_INDEX` and `discoveryComplete=false`.

Record a `manifest[]` row for **every scoped source file** with `path`, `classification` (`ENTITY`, `MAPPED_SUPERCLASS`, `EMBEDDABLE`, `DTO`, `ENUM`, `OTHER`, `UNCERTAIN`), `classificationEvidence`, and `inspectionStatus` (`NOT_INSPECTED`, `PARTIAL`, `FULL`). In Java, inspect `@Entity`, inherited mapping patterns and XML mapping where relevant. File names ending in `Entity` do not prove persistence. The primary unit is file coverage, but a file may contain multiple mapped types; do not assume 1:1.

## MCP-first approach

- `get_table(table=...)` deterministically returns ORM/SQL table definitions, but `[name inferred]`, `FK?`, and `REFERENCED BY?` require confirmation. Query exact table names to avoid its limited multi-match definition output.
- `get_graph_schema` then `search_graph` discovers indexed class/type symbols. Paginate and note `total`; offset cap means it may not be exhaustive. `get_snippet` reads bounded symbol source and may truncate at ~16k chars; check entire file in checkout if needed.
- `grep_code` accepts literal terms (not regex) and only indexed chunks. Use for finding known tokens, not for completeness proof.
- `get_project_glossary` may find cross-repository names; reconcile semantics by evidence, not string similarity.

## Per technical record

`kind=technicalEntity`, `id=repo:<repository>|class:<FQCN>`, `sourcePath`, `fullyQualifiedName`, `technicalType`, `table` (if proven), `primaryKey` (if proven), `attributes[]` with name/type/column/mapping/nullable/PK flags and evidence, `relationships[]` with target stable ID or `resolution=UNRESOLVED/EXTERNAL`, association kind, cardinality, join details, and evidence, `inspectionStatus`, `evidence[]`.

Extract all persistence-relevant inherited properties and association metadata. If an entity extends a mapped superclass with incomplete details, keep `inspectionStatus=PARTIAL` or explicitly reference a separately inspected inherited mapping record. Null is not a guess.

Business concepts are **separate** `kind=businessConcept` records. Include candidate name/definition, evidence, mapped technical ID(s), identity candidates, `candidateOOI=UNCERTAIN` by default, and `reviewStatus=PROPOSED`. Lookup tables, localization rows and join tables remain technical structures unless meaningfully justified as separate business concepts.

## Reconciliation

- Match manifest paths to class FQCN; normalize duplicate `id` and duplicate file+FQCN separately.
- Entity count is derived from actual mapped classes, not filename total or narrative count.
- Record both per-batch and cumulative counts with explicit provenance. Cumulative counts may be `null` if previous batches are unavailable; never add speculative counts.
- Relationship targets in another repository/module can be marked `EXTERNAL` with grounded reference. A missing target in scope is `UNRESOLVED`.
- Do not set `extractionComplete=true` until authoritative manifest and full mapped-attribute/relation inspection are established and validators pass.

## Deterministic progression

Sort manifest paths lexicographically, process next 5 eligible files, emit full source evidence and checkpoint. On interruption emit all **complete records** and mark pending files partial/uninspected. Do not generate giant truncated JSON.
