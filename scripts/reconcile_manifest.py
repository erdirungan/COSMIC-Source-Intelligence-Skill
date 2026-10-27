#!/usr/bin/env python3
"""Compare a source manifest JSON with entity batch record JSONs.

Usage: python scripts/reconcile_manifest.py manifest.json batch1.json batch2.json
manifest.json: {"repository": "...", "sourceRevision": "...",
                "manifest": [{"path":"...","classification":"ENTITY",...}]}
Does not establish manifest truth; use a checkout-derived manifest.
"""
import argparse
import json
from collections import Counter
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest_file', type=Path)
    p.add_argument('batches', type=Path, nargs='+')
    a = p.parse_args()
    baseline = json.loads(a.manifest_file.read_text(encoding='utf-8'))
    manifest = baseline['manifest']
    expected = {r['path'] for r in manifest if r['classification'] == 'ENTITY'}
    all_records = []
    mismatches = []
    for fn in a.batches:
        batch = json.loads(fn.read_text(encoding='utf-8'))
        if batch['repository'] != baseline['repository'] or batch['sourceRevision'] != baseline['sourceRevision']:
            mismatches.append(str(fn))
        all_records.extend(r for r in batch['records'] if r.get('kind') == 'technicalEntity')
    ids = [r['id'] for r in all_records]
    seen = Counter(ids)
    actual_paths = {r.get('sourcePath') for r in all_records}
    result = {
        'manifestFiles': len(manifest),
        'expectedEntityFiles': len(expected),
        'technicalEntityRecords': len(all_records),
        'duplicateStableIds': [x for x, n in sorted(seen.items()) if n > 1],
        'entityFilesWithNoRecord': sorted(expected - actual_paths),
        'recordsOutsideManifestEntityFiles': sorted((actual_paths - expected) - {None}),
        'revisionMismatchedBatches': mismatches,
        'note': 'One file may declare multiple entities; compare IDs and manifest rather than equating records with files.'
    }
    print(json.dumps(result, indent=2))
    return int(bool(result['duplicateStableIds'] or result['entityFilesWithNoRecord'] or
                    result['recordsOutsideManifestEntityFiles'] or mismatches))


if __name__ == '__main__':
    raise SystemExit(main())
