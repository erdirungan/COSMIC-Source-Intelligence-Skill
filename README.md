# COSMIC Source Intelligence — AI Coder Skill

A portable Agent Skill for extracting **source-grounded architecture, technical entities, candidate business concepts and functional flows** for COSMIC Measurement Workbench (CWB). The skill deliberately **does not calculate CFP or classify COSMIC data movements**.

## Import into AI Coder

1. Push this repository to an accessible Git repository (private if source/tooling context requires it).
2. In AI Coder choose **Import skills from Git**, paste the repository URL, select its branch or pinned tag/commit, and choose **Discover**.
3. Select **cosmic-source-intelligence** and click **Import selected**.
4. Ask: `Use cosmic-source-intelligence, operation EXTRACT_ENTITIES, repo mar-backend, module CommonBackend, package etiya/commerce/backend/common/entity/address. First establish an authoritative file manifest and inspect a batch of five files. Return schemaVersion 1.0 JSON with checkpoint. Do not claim completeness without checkout evidence.`

An imported skill may be **manually invoked in AI Coder**, but is not automatically callable through the existing AI Coder MCP. Unattended CWB execution requires an accessible skill job API/tool or a separate CWB-side worker. The existing MCP can still supply the source evidence directly.

## Structure

- `SKILL.md`: operating instructions and triggers.
- `references/`: operation guides, COSMIC restrictions, evidence contract and JSON schema.
- `scripts/validate_inventory.py`: consistency/coverage checks; optionally JSON Schema validation with `pip install jsonschema`.
- `scripts/reconcile_manifest.py`: reconciles multiple batches with one manifest.
- `examples/`: synthetic samples; **not source-code verification**.

## Test locally

```bash
python scripts/validate_inventory.py examples/partial-address-batch.json
python scripts/validate_inventory.py examples/invalid-completion.json   # expected failure
python scripts/reconcile_manifest.py examples/partial-address-batch.json examples/partial-address-batch.json
```

`VALID` means internal record/coverage consistency only. It does **not** confirm that a declared manifest, code annotation or line reference matches a repository checkout.

## CWB ownership

CWB remains owner of the canonical evidence registry, approved measurement contexts, human decisions and COSMIC calculations. Source evidence is versioned and independently auditable; the skill produces proposals, not approvals.
