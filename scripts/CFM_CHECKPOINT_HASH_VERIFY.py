#!/usr/bin/env python3
"""Read-only, streaming SHA-256 verification of 14 frozen P20 checkpoints.

USAGE
    python CFM_CHECKPOINT_HASH_VERIFY.py BUILDING_CFM_RESUME_LATEST.zip CFM_CODE_ONLY_PROVENANCE_EXPORT.zip

Reads only the 14 checkpoint byte streams listed in the archived P37F lock.
No checkpoint is executed, deserialized, imported, or extracted.
No raw data, test labels, training, inference or network operations are involved.
Neither input ZIP is modified. Reports are written to the current directory.
"""
import csv
import hashlib
import json
import sys
import zipfile
from pathlib import Path

LOCK_FILE = 'source_evidence/outputs/p37_oslo_single_locked_external_confirmation/P37F_PRE_CAL_IMPLEMENTATION_AND_MODEL_LOCK.json'
OUT = Path('CFM_CHECKPOINT_HASH_RESULTS.csv')
SUMMARY = Path('CFM_CHECKPOINT_HASH_SUMMARY.md')


def main():
    if len(sys.argv) != 3:
        raise SystemExit('USAGE: py CFM_CHECKPOINT_HASH_VERIFY.py MASTER.zip CODE_EXPORT.zip')
    master = Path(sys.argv[1]); export = Path(sys.argv[2])
    if not master.is_file() or not export.is_file():
        raise SystemExit('Input file not found. Check your ZIP paths; originals must stay unchanged.')
    with zipfile.ZipFile(export, 'r') as source:
        locked = json.loads(source.read(LOCK_FILE))
        models = locked['model_file_hashes']
    if len(models) != 14:
        raise SystemExit(f'Aborting: expected exactly 14 model paths, got {len(models)}.')
    result=[]
    with zipfile.ZipFile(master, 'r') as archive:
        existing=set(archive.namelist())
        for filename, expected in sorted(models.items()):
            status='MISSING'; observed=''; note=''
            if filename in existing:
                try:
                    h=hashlib.sha256()
                    with archive.open(filename, 'r') as reader:
                        while True:
                            block=reader.read(4 * 1024 * 1024)
                            if not block: break
                            h.update(block)
                    observed=h.hexdigest()
                    status='PASS' if observed.lower()==expected.lower() else 'MISMATCH'
                except (zipfile.BadZipFile, RuntimeError, OSError, EOFError) as exc:
                    status='READ_ERROR'; note=f'{type(exc).__name__}: {exc}'
            result.append({'checkpoint_path':filename, 'locked_expected_sha256':expected,
                           'current_master_sha256':observed,'status':status,'note':note})
            print(f'{status:11} {filename}',flush=True)
    with OUT.open('w', newline='', encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=list(result[0]))
        writer.writeheader();writer.writerows(result)
    statuses={s:sum(r['status']==s for r in result) for s in ('PASS','MISSING','MISMATCH','READ_ERROR')}
    SUMMARY.write_text(
        '# Read-only 14-checkpoint SHA-256 comparison\n\n'
        'This is a file-integrity check against the P37F archived model hash manifest, **not** model reproduction. '
        'No model weights were loaded into Python/torch, and no dataset or test labels were read.\n\n'
        f'- Input master: `{master.name}`\n- Archived lock: `{LOCK_FILE}`\n'
        f'- Counts: {statuses}\n- Results: `{OUT.name}`\n\n'
        'A PASS shows current bytes match the archived hash receipt; it does not prove end-to-end reproducibility '
        'or establish the original training environment.\n',encoding='utf-8')
    print(f'Wrote {OUT} and {SUMMARY}. Counts: {statuses}')
    return 0 if statuses['PASS']==14 else 2


if __name__=='__main__':
    sys.exit(main())
