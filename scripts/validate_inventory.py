#!/usr/bin/env python3
"""Validate CWB source-intelligence JSON consistency (not source-code truth).

Usage: python scripts/validate_inventory.py examples/partial-address-batch.json
Exit 0 = valid internally, exit 1 = blocking violations. JSON Schema also checked
when `jsonschema` is installed; otherwise stdlib checks still run.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE.parent / 'references' / 'cwb-evidence-schema.json'
CLASSIFICATIONS = {'ENTITY', 'MAPPED_SUPERCLASS', 'EMBEDDABLE', 'DTO', 'ENUM', 'OTHER', 'UNCERTAIN'}
STATUSES = {'NOT_INSPECTED', 'PARTIAL', 'FULL'}


def validate(data):
    errors, warnings = [], []
    def err(s): errors.append(s)
    for name in ('schemaVersion', 'operation', 'batchId', 'repository', 'sourceRevision', 'scope',
                 'manifestAuthority', 'manifest', 'records', 'coverage', 'checkpoint', 'unresolvedQuestions'):
        if name not in data: err(f'missing required field: {name}')
    if errors: return errors, warnings
    if data['schemaVersion'] != '1.0': err('unsupported schemaVersion')
    if not isinstance(data['manifest'], list) or not isinstance(data['records'], list):
        return errors + ['manifest and records must be arrays'], warnings
    paths = [m.get('path') for m in data['manifest']]
    if len(paths) != len(set(paths)): err('duplicate manifest paths')
    for i, m in enumerate(data['manifest']):
        if m.get('classification') not in CLASSIFICATIONS: err(f'manifest[{i}] invalid classification')
        if m.get('inspectionStatus') not in STATUSES: err(f'manifest[{i}] invalid inspectionStatus')
    c = data['coverage']
    checks = {
        'filesDiscovered': len(paths),
        'filesInspectedFull': sum(m.get('inspectionStatus') == 'FULL' for m in data['manifest']),
        'filesInspectedPartial': sum(m.get('inspectionStatus') == 'PARTIAL' for m in data['manifest']),
        'filesUninspected': sum(m.get('inspectionStatus') == 'NOT_INSPECTED' for m in data['manifest']),
        # This is a minimum count; a file can hold multiple mapped classes.
        'entityRecordsExtracted': sum(r.get('kind') == 'technicalEntity' for r in data['records']),
    }
    for k, expected in checks.items():
        got = c.get(k)
        if got is not None and got != expected: err(f'{k}={got}, but batch arrays yield {expected}')
    if data['operation'] == 'EXTRACT_ENTITIES':
        entity_paths = {m['path'] for m in data['manifest'] if m.get('classification') == 'ENTITY'}
        if c.get('entityClassesDiscovered') is not None and c['entityClassesDiscovered'] < len(entity_paths):
            err('entityClassesDiscovered smaller than manifest ENTITY files')
    ids = [r.get('id') for r in data['records']]
    if len(ids) != len(set(ids)): err('duplicate record IDs')
    local_ids = set(ids)
    manifest_map = {m['path']: m for m in data['manifest']}
    for i, r in enumerate(data['records']):
        ident = r.get('id', f'<record {i}>')
        evidences = r.get('evidence', [])
        if not evidences: err(f'{ident}: no source evidence')
        if r.get('kind') == 'technicalEntity':
            fqcn = r.get('fullyQualifiedName')
            expected_id = f"repo:{data['repository']}|class:{fqcn}"
            if not fqcn or ident != expected_id: err(f'{ident}: inconsistent stable FQCN ID')
            src = r.get('sourcePath')
            if src not in manifest_map: err(f'{ident}: sourcePath not in batch manifest')
            elif r.get('inspectionStatus') == 'FULL' and manifest_map[src]['inspectionStatus'] != 'FULL':
                err(f'{ident}: record FULL but source manifest not FULL')
            for attr in r.get('attributes', []):
                if not attr.get('evidence'): err(f'{ident}: attribute {attr.get("name")} lacks evidence')
            for rel in r.get('relationships', []):
                status, target = rel.get('resolution'), rel.get('targetId')
                if status == 'RESOLVED' and not target: err(f'{ident}: RESOLVED relationship without targetId')
                if status == 'UNRESOLVED' and target and target in local_ids:
                    warnings.append(f'{ident}: local target {target} exists but relationship marked UNRESOLVED')
                if not rel.get('evidence'): err(f'{ident}: relationship missing evidence')
        for e in evidences + [e for a in r.get('attributes', []) for e in a.get('evidence', [])] + [e for rel in r.get('relationships', []) for e in rel.get('evidence', [])]:
            if e.get('repository') != data['repository']:
                warnings.append(f'{ident}: cross-repository evidence {e.get("repository")} (verify intentionally)')
            if e.get('sourceRevision') != data['sourceRevision'] and e.get('verification') == 'VERIFIED_SOURCE':
                err(f'{ident}: VERIFIED_SOURCE evidence on another revision')
            start, end = e.get('startLine'), e.get('endLine')
            if not isinstance(start, int) or not isinstance(end, int) or start < 1 or end < start:
                err(f'{ident}: invalid evidence line range')
    if data['manifestAuthority'] != 'CHECKOUT' and c.get('discoveryComplete'):
        err('discoveryComplete requires CHECKOUT manifest')
    if c.get('discoveryComplete') and any(m['classification'] == 'UNCERTAIN' for m in data['manifest']):
        err('discoveryComplete with UNCERTAIN file classifications')
    if c.get('extractionComplete'):
        if not c.get('discoveryComplete'): err('extractionComplete without discoveryComplete')
        if any(m['inspectionStatus'] != 'FULL' for m in data['manifest'] if m['classification'] in ('ENTITY', 'MAPPED_SUPERCLASS', 'EMBEDDABLE')):
            err('extractionComplete with incomplete mapped source files')
        entity_record_paths = {r.get('sourcePath') for r in data['records'] if r.get('kind') == 'technicalEntity' and r.get('inspectionStatus') == 'FULL'}
        missing = {m['path'] for m in data['manifest'] if m.get('classification') == 'ENTITY'} - entity_record_paths
        if missing: err(f'extractionComplete but no FULL technicalEntity record for: {sorted(missing)}')
        if data['checkpoint'].get('remainingPaths'):
            err('extractionComplete but checkpoint still has remainingPaths')
    if c.get('businessMappingReviewed'):
        err('AI-supplied businessMappingReviewed=true requires external human approval; leave false in AI output')
    if data['checkpoint'].get('completedPaths'):
        invalid = set(data['checkpoint']['completedPaths']) - set(paths)
        if invalid: err(f'checkpoint completedPaths outside manifest: {sorted(invalid)}')
    return errors, warnings


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('json_file', type=Path)
    args = p.parse_args()
    try:
        data = json.loads(args.json_file.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as ex:
        print(f'INVALID JSON: {ex}', file=sys.stderr)
        return 1
    errors, warnings = validate(data)
    try:
        import jsonschema
        schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
        for error in jsonschema.Draft202012Validator(schema).iter_errors(data):
            errors.append(f'schema: {error.json_path}: {error.message}')
    except ImportError:
        warnings.append('jsonschema is not installed; JSON Schema layer skipped')
    for s in warnings: print(f'WARNING: {s}')
    for s in errors: print(f'ERROR: {s}')
    print(f'{"INVALID" if errors else "VALID"}: {args.json_file} ({len(errors)} errors, {len(warnings)} warnings)')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
