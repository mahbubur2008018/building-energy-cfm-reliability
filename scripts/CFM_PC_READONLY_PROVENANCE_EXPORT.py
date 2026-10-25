#!/usr/bin/env python3
"""Read-only local ZIP provenance export for Building Energy CFM P40+ master.

Usage (Windows/macOS/Linux):
  python CFM_PC_READONLY_PROVENANCE_EXPORT.py "/path/to/BUILDING_CFM_RESUME_LATEST.zip"

The input master ZIP is opened in read-only mode. This script never executes
archived scripts, reads model checkpoints, test-label/prediction datasets, or
runs training/evaluation. Review export content before uploading or publishing.
"""
import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile

EXPECTED_HASHES = {
    'scripts/phase21_frozen_inference_worker.py':
        '98f7e86449ed85aa90ee7f43311b5eceb9dd235a1f16e24a594f402b3ec15ac4',
    'outputs/phase21_cofactor_frozen_confirmation/P21_FROZEN_INFERENCE_SETTINGS.json':
        '3070774cdac28679e91deadd07c7d88884fc4f6e1f811dcd1d503a06cf7b0a87',
}
SOURCE_EXTS = {'.py', '.sh', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.lock'}
SOURCE_HINTS = ('script', 'code', 'config', 'requirements', 'environment', 'freeze', 'pip', 'runtime', 'hash', 'sha', 'phase20', 'phase21', 'phase37', 'phase40', 'lock')
FORBIDDEN = ('prediction', 'test_cache', 'raw_data', 'raw-meter', 'raw_meter', 'meter_data', 'target_array', 'test_label', 'test_target', 'cal_label', 'cal_target', 'weights', 'checkpoint', 'state_dict', 'feature_array', 'prediction_array', 'credentials', 'secret', 'token', 'password')
MAX_FILE_BYTES = 400_000


def relative_name(name: str) -> str:
    s = name.replace('\\', '/').lstrip('/')
    if s.startswith('BUILDING_CFM_STATE/'):
        s = s[len('BUILDING_CFM_STATE/'):]
    return s


def safe_selected(name: str, size: int) -> bool:
    s = relative_name(name)
    low = s.lower()
    if not s or size <= 0 or size > MAX_FILE_BYTES or any(tag in low for tag in FORBIDDEN):
        return False
    if '..' in PurePosixPath(s).parts:
        return False
    ext = PurePosixPath(s).suffix.lower()
    if low.startswith('scripts/') and ext in SOURCE_EXTS:
        return True
    if low.startswith('outputs/'):
        if ext in ('.json', '.txt', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.lock') and any(h in low for h in SOURCE_HINTS):
            return True
    if ext in SOURCE_EXTS and any(h in low for h in SOURCE_HINTS):
        return True
    if ext in ('.json', '.txt') and any(h in low for h in ('requirements', 'environment', 'freeze', 'hash', 'sha256', 'manifest', 'role_allocation', 'pre_calibration', 'protocol')):
        return True
    return s in EXPECTED_HASHES


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('master_zip', help='Path to PC-saved completed Kaggle master ZIP')
    ap.add_argument('--output', help='Optional output ZIP filename')
    args = ap.parse_args()
    master = Path(args.master_zip).expanduser().resolve()
    if not master.is_file():
        raise SystemExit('ERROR: Input ZIP not found: ' + str(master))
    output = Path(args.output).expanduser().resolve() if args.output else master.with_name('CFM_CODE_ONLY_PROVENANCE_EXPORT.zip')
    if output == master:
        raise SystemExit('ERROR: Output path must be different from original master')
    inventory = []
    hashes = []
    found = set()
    with ZipFile(master, 'r') as zin, ZipFile(output, 'w', ZIP_DEFLATED, compresslevel=6) as zout:
        for i, info in enumerate(zin.infolist(), start=1):
            if info.is_dir():
                continue
            rel = relative_name(info.filename)
            inventory.append({'path': rel, 'uncompressed_bytes': info.file_size, 'compressed_bytes': info.compress_size,
                              'CRC32_header': f'{info.CRC:08x}', 'exported': safe_selected(info.filename, info.file_size)})
            if not safe_selected(info.filename, info.file_size):
                continue
            data = zin.read(info)  # reads only whitelisted, small source files
            sha = hashlib.sha256(data).hexdigest()
            expected = EXPECTED_HASHES.get(rel)
            status = 'MATCH' if expected == sha else ('MISMATCH' if expected else 'NOT_IN_TWO_ANCHOR_RECEIPTS')
            zout.writestr('source_evidence/' + rel, data)
            hashes.append({'path': rel, 'bytes': len(data), 'sha256': sha,
                           'pretest_expected_sha256': expected or '', 'pretest_anchor_status': status})
            found.add(rel)
        for path, digest in EXPECTED_HASHES.items():
            if path not in found:
                hashes.append({'path': path, 'bytes': '', 'sha256': '',
                               'pretest_expected_sha256': digest, 'pretest_anchor_status': 'NOT_FOUND'})
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=['path','bytes','sha256','pretest_expected_sha256','pretest_anchor_status'])
        writer.writeheader(); writer.writerows(hashes)
        zout.writestr('PROVENANCE_HASH_AUDIT.csv', buf.getvalue())
        zout.writestr('FULL_MASTER_FILENAMES_INVENTORY.json', json.dumps(inventory, indent=2, ensure_ascii=False))
        zout.writestr('READ_ME_FIRST.txt',
                     'Original master ZIP was NOT modified. Only small source and configuration files were read.\n'
                     'No checkpoint model weights, raw meter arrays, prediction arrays or test-label files were exported.\n'
                     'Hash checks on two anchor files are preliminary; full P32/P37 comparison remains open.\n'
                     'Inventory contains filenames and sizes of other files, NOT their contents.\n'
                     'Review output privately for sensitive code, internal filenames or credentials before sharing.\n')
    print('INPUT :', master, '| bytes:', master.stat().st_size)
    print('OUTPUT:', output, '| bytes:', output.stat().st_size)
    print('Files indexed:', len(inventory), '| source/config evidence exported:', len(found))
    for row in hashes:
        if row['pretest_anchor_status'] in ('MATCH', 'MISMATCH', 'NOT_FOUND'):
            print('Anchor:', row['pretest_anchor_status'], row['path'])
    print('Upload the smaller OUTPUT ZIP and latest saved .ipynb if available.')

if __name__ == '__main__':
    try:
        main()
    except (BadZipFile, OSError, RuntimeError) as exc:
        print('ERROR:', exc, file=sys.stderr)
        sys.exit(2)
