#!/usr/bin/env python3
"""Read-only metadata/hash audit; optional exact-source PNG replay in memory.

This verifies recorded consistency, not named glyph binding or cipher semantics.
The default requires only Python's standard library and never opens image files.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re

HEX = re.compile(r"[0-9a-f]{64}\Z")
LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
ALLOWED_FILES = {
    'README.md', 'FROZEN_PROTOCOL.json', 'LOCALIZATION_INPUT.json',
    'LOCALIZER_REPORT.txt', 'LOCALIZER_CAPTURE_SUPPLEMENT.txt',
    'SOURCE_GATE_REVIEW.txt', 'PRE_OBSERVER_SCOPE.json',
    'COORDINATOR_REGISTRY.json', 'PACKET_SPEC.json', 'PACKET_MANIFEST.json',
    'SOURCE_IMAGE.json', 'CAPTURE_IMAGE.json', 'CAPTURE_IMAGE_02.json',
    'BLINDED_OBSERVER_PROMPT.txt', 'BLINDED_OBSERVER_RAW.txt', 'RESULTS.json',
    'PUBLICATION_TRANSFORMS.json', 'build_packet.py', 'verify_audit.py',
    'SHA256SUMS.txt', 'RUNTIME_AND_CHECKS.json',
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def no_duplicate_keys(entries: list[tuple[str, object]]) -> dict:
    value = {}
    for key, entry in entries:
        require(key not in value, f'duplicate JSON key: {key}')
        value[key] = entry
    return value


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicate_keys)
    require(isinstance(value, dict), f'{path.name}: expected JSON object')
    return value


def relative_path(value: str) -> str:
    require(isinstance(value, str), 'path must be a string')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.parts and all(part not in {'.', '..'} for part in path.parts), f'unsafe relative path: {value!r}')
    require('\\' not in value and path.as_posix() == value, f'noncanonical relative path: {value!r}')
    return value


def check_sums(package: Path) -> dict[str, str]:
    require(package.is_dir(), 'package directory is missing')
    actual_files = set()
    for path in package.iterdir():
        require(path.name in ALLOWED_FILES, f'unexpected package entry: {path.name}')
        require(path.is_file() and not path.is_symlink(), f'package entry must be a regular file: {path.name}')
        actual_files.add(path.name)
    require(actual_files == ALLOWED_FILES, 'complete audit inventory is required; missing: ' + ', '.join(sorted(ALLOWED_FILES - actual_files)))
    sums = {}
    for line in (package / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        require(match is not None, 'malformed SHA256SUMS.txt line')
        digest, name = match.groups()
        relative_path(name)
        require(name in ALLOWED_FILES and name != 'SHA256SUMS.txt', f'unsupported checksum entry: {name}')
        require(name not in sums, f'duplicate checksum entry: {name}')
        sums[name] = digest
    require(set(sums) == actual_files - {'SHA256SUMS.txt'}, 'checksum inventory does not exactly cover package files')
    for name, digest in sums.items():
        require(sha((package / name).read_bytes()) == digest, f'publication checksum mismatch: {name}')
    print(f'PASS: {len(sums)} published file checksums (SHA256SUMS.txt excludes itself)')
    return sums


def check_transforms(package: Path, sums: dict[str, str]) -> dict[str, str]:
    transforms = read_json(package / 'PUBLICATION_TRANSFORMS.json')
    records = transforms['files']
    require(isinstance(records, list) and records, 'publication transform records missing')
    originals = {}
    transformed_count = 0
    for record in records:
        name = relative_path(record['file'])
        require(name in sums and name not in originals, f'unknown or duplicate transformed file: {name}')
        require(HEX.fullmatch(record['original_sha256']) is not None, f'invalid original hash: {name}')
        require(record['publication_sha256'] == sums[name], f'transform publication hash mismatch: {name}')
        require(record['publication_bytes'] == (package / name).stat().st_size, f'transform publication byte mismatch: {name}')
        require(type(record['original_bytes']) is int and record['original_bytes'] > 0, f'invalid original byte count: {name}')
        kind = record['transformation']['type']
        if kind == 'verbatim':
            require(record['original_sha256'] == sums[name], f'verbatim original hash mismatch: {name}')
            require(record['original_bytes'] == record['publication_bytes'], f'verbatim byte count mismatch: {name}')
        elif kind == 'remove_local_filesystem_fields':
            published = read_json(package / name)
            require(all(key not in published for key in record['transformation']['removed_top_level_keys']), f'removed filesystem key remains: {name}')
            transformed_count += 1
        elif kind == 'replace_exact_workspace_prefix':
            change = record['transformation']
            require(HEX.fullmatch(change['source_prefix_sha256']) is not None, f'invalid redaction prefix digest: {name}')
            require(change['replacement'] == '<LOCAL_WORKSPACE>', f'unexpected path replacement: {name}')
            require(type(change['replacement_count']) is int and change['replacement_count'] > 0, f'invalid replacement count: {name}')
            require((package / name).read_text(encoding='utf-8').count(change['replacement']) == change['replacement_count'], f'replacement count mismatch: {name}')
            transformed_count += 1
        else:
            raise ValueError(f'unknown publication transform: {kind}')
        originals[name] = record['original_sha256']
    print(f'PASS: publication hashes and original-hash provenance records checked separately ({transformed_count} transformed files; original transformed bytes withheld)')
    return originals


def check_recorded_references(value: object, originals: dict[str, str], sums: dict[str, str]) -> int:
    count = 0
    if isinstance(value, dict):
        for key, child in value.items():
            if isinstance(key, str) and key.endswith('_sha256'):
                require(isinstance(child, str) and HEX.fullmatch(child) is not None, f'invalid recorded SHA256: {key}')
                name = key[:-len('_sha256')]
                if name in originals or name in sums:
                    expected = originals.get(name, sums.get(name))
                    require(child == expected, f'original-byte reference mismatch: {key}')
                    count += 1
            count += check_recorded_references(child, originals, sums)
    elif isinstance(value, list):
        count += sum(check_recorded_references(child, originals, sums) for child in value)
    return count


def index_entries(pairs: list[dict], location: str) -> dict[tuple[str, str], dict]:
    require(isinstance(pairs, list) and pairs, f'{location}: missing pairs')
    indexed = {}
    pair_labels = set()
    for pair in pairs:
        label = pair['label']
        require(isinstance(label, str) and LABEL.fullmatch(label) is not None, f'{location}: unsafe pair label')
        require(label.casefold() not in pair_labels, f'{location}: duplicate pair label')
        pair_labels.add(label.casefold())
        item_labels = set()
        require(isinstance(pair['items'], list) and pair['items'], f'{location}: missing items')
        for item in pair['items']:
            item_label = item['label']
            require(isinstance(item_label, str) and LABEL.fullmatch(item_label) is not None, f'{location}: unsafe item label')
            require(item_label.casefold() not in item_labels, f'{location}: duplicate item label')
            item_labels.add(item_label.casefold())
            indexed[(label, item_label)] = item
    return indexed


def checked_box(box: list, size: list, location: str) -> None:
    require(isinstance(box, list) and len(box) == 4 and all(type(n) is int for n in box), f'{location}: malformed box')
    x, y, width, height = box
    require(x >= 0 and y >= 0 and width > 0 and height > 0, f'{location}: negative or empty box')
    require(x + width <= size[0] and y + height <= size[1], f'{location}: out-of-bounds box')


def check_metadata(package: Path, originals: dict[str, str], sums: dict[str, str]) -> dict:
    documents = {name: read_json(package / name) for name in sums if name.endswith('.json') and name != 'PUBLICATION_TRANSFORMS.json'}
    reference_count = sum(check_recorded_references(value, originals, sums) for value in documents.values())
    protocol = documents['FROZEN_PROTOCOL.json']
    scope = documents['PRE_OBSERVER_SCOPE.json']
    registry = documents['COORDINATOR_REGISTRY.json']
    manifest = documents['PACKET_MANIFEST.json']
    source = documents['SOURCE_IMAGE.json']
    capture = documents['CAPTURE_IMAGE_02.json']
    first_capture = documents['CAPTURE_IMAGE.json']
    localization = documents['LOCALIZATION_INPUT.json']
    require(scope['named_pair_source_gate'] == 'unresolved', 'frozen named-pair source gate must remain unresolved')
    require(scope['frozen_protocol_changed'] is False and scope['before_blinded_observer_ratings'] is True, 'pre-observer scope changed')
    require(scope['named_pair_final_decision'] == 'unresolved regardless of any ancillary crop-rating outcome', 'ancillary scope promoted to named-pair conclusion')
    require(registry['protocol_sha256'] == originals['FROZEN_PROTOCOL.json'], 'registry original protocol reference mismatch')
    require(registry['packet_spec_sha256'] == originals['PACKET_SPEC.json'], 'registry original packet-spec reference mismatch')
    runtime = documents['RUNTIME_AND_CHECKS.json']
    require(runtime['packet_builder_sha256'] == originals['build_packet.py'], 'runtime original packet-builder hash mismatch')
    require(runtime['source_pixels_published'] is False and runtime['historical_computations_reexecuted'] is False, 'runtime scope flags changed')
    require(localization['image_sha256'] == source['sha256'], 'localization source-image reference mismatch')
    require(localization['targets'] == protocol['coordinator_targets'], 'localization target references differ from protocol')
    require(source['view_url'] == protocol['source']['url'], 'source viewer URL reference mismatch')
    require(first_capture['source_url'] == capture['source_url'], 'capture source viewer URLs disagree')
    for metadata in [source, first_capture, capture, manifest['source']]:
        require(HEX.fullmatch(metadata['sha256']) is not None, 'invalid source image hash')
        require(type(metadata['bytes']) is int and metadata['bytes'] > 0, 'invalid source image bytes')
        require(isinstance(metadata['dimensions'], list) and len(metadata['dimensions']) == 2 and all(type(n) is int and n > 0 for n in metadata['dimensions']), 'invalid source dimensions')
    require(registry['source_sha256'] == capture['sha256'] == manifest['source']['sha256'], 'packet source hash association mismatch')
    require(capture['dimensions'] == manifest['source']['dimensions'] and capture['bytes'] == manifest['source']['bytes'], 'packet source dimensions/bytes mismatch')
    for filename, digest in [('LOCALIZER_REPORT.txt', source['sha256']), ('LOCALIZER_CAPTURE_SUPPLEMENT.txt', first_capture['sha256']), ('LOCALIZER_CAPTURE_SUPPLEMENT.txt', capture['sha256'])]:
        require(digest in (package / filename).read_text(encoding='utf-8'), f'{filename}: recorded source hash absent')
    specs = index_entries(documents['PACKET_SPEC.json']['pairs'], 'spec')
    registered = index_entries(registry['pairs'], 'registry')
    emitted = index_entries(manifest['pairs'], 'manifest')
    require(set(specs) == set(registered) == set(emitted), 'packet pair/item labels do not agree')
    paths = set()
    for labels, spec in specs.items():
        item = emitted[labels]
        require(set(item) == {'label', 'crop', 'context', 'crop_3x', 'context_3x'}, f'{labels}: unexpected packet variants')
        for kind, key in [('crop', 'box'), ('context', 'context_box')]:
            box = spec[key]
            checked_box(box, capture['dimensions'], f'{labels}/{kind}')
            require(registered[labels][key] == box == item[kind]['box'], f'{labels}/{kind}: box reference mismatch')
            for variant, factor in [(kind, 1), (kind + '_3x', 3)]:
                record = item[variant]
                require(record['dimensions'] == [box[2] * factor, box[3] * factor], f'{labels}/{variant}: dimensions mismatch')
                require(record['mode'] == manifest['source']['mode'], f'{labels}/{variant}: mode mismatch')
                require(type(record['bytes']) is int and record['bytes'] > 0 and HEX.fullmatch(record['sha256']) is not None, f'{labels}/{variant}: invalid bytes/hash')
                name = relative_path(record['path'])
                require(name == f'{labels[0]}/{labels[1]}/{variant}.png' and name not in paths, f'{labels}/{variant}: path mismatch')
                paths.add(name)
    # Duplicate-control identity is a byte claim. Negative topology truth is not
    # independently checkable without pixels and is not inferred from hashes.
    for pair in registry['pairs']:
        if pair['expected_control_decision'] == 'same':
            first, *others = [emitted[(pair['label'], item['label'])] for item in pair['items']]
            for other in others:
                for variant in ['crop', 'context', 'crop_3x', 'context_3x']:
                    require(first[variant]['sha256'] == other[variant]['sha256'], f'{pair["label"]}: duplicate-control hash mismatch')
    print(f'PASS: {reference_count} original-file hash references, source associations, frozen unresolved scope, {len(paths)} PNG records and native/3x dimensions')
    check_results(package, documents['RESULTS.json'], registry, originals, scope)
    return manifest


def check_results(package: Path, results: dict, registry: dict, originals: dict[str, str], scope: dict) -> None:
    aliases = {
        'raw_observer_sha256': 'BLINDED_OBSERVER_RAW.txt',
        'prompt_original_sha256': 'BLINDED_OBSERVER_PROMPT.txt',
        'protocol_original_sha256': 'FROZEN_PROTOCOL.json',
        'registry_original_sha256': 'COORDINATOR_REGISTRY.json',
        'packet_manifest_sha256': 'PACKET_MANIFEST.json',
    }
    for key, filename in aliases.items():
        require(results[key] == originals[filename], f'RESULTS original-byte reference mismatch: {key}')
    require(results['named_pair_source_gate'] == scope['named_pair_source_gate'] == 'unresolved', 'RESULTS promotes unresolved source gate')
    require(results['named_pair_final_decision'] == 'unresolved', 'named-pair final decision must remain unresolved')
    raw = (package / 'BLINDED_OBSERVER_RAW.txt').read_text(encoding='utf-8')
    headings = list(re.finditer(r'^P[0-9]+\s*$', raw, re.MULTILINE))
    raw_decisions = {}
    for index, heading in enumerate(headings):
        label = heading.group().strip()
        require(label not in raw_decisions, f'duplicate raw observer pair: {label}')
        end = headings[index + 1].start() if index + 1 < len(headings) else len(raw)
        decisions = re.findall(r'^Decision: (\S+)\s*$', raw[heading.end():end], re.MULTILINE)
        require(len(decisions) == 1, f'{label}: expected one raw observer decision')
        raw_decisions[label] = decisions[0]
    registered = {pair['label']: pair for pair in registry['pairs']}
    recorded = {pair['label']: pair for pair in results['pairs']}
    require(len(recorded) == len(results['pairs']) and set(recorded) == set(registered) == set(raw_decisions), 'RESULTS/raw/registry pair labels disagree')
    controls = []
    target_decisions = []
    decisions_map = {'same': 'same_physical_class', 'different': 'different_physical_class', None: None}
    for label, pair in recorded.items():
        source_pair = registered[label]
        require(pair['raw_decision'] in {'same_physical_class', 'different_physical_class', 'unresolved'} and pair['raw_decision'] == raw_decisions[label], f'{label}: raw decision changed')
        require(pair['role'] == source_pair['role'], f'{label}: role changed')
        require(pair['source_regions_by_side'] == {item['label']: item['source_region'] for item in source_pair['items']}, f'{label}: source-region references changed')
        expected = decisions_map[source_pair['expected_control_decision']]
        require(pair['expected_control_decision'] == expected, f'{label}: control criterion changed')
        if expected is None:
            require(pair['control_passed'] is None, f'{label}: target misclassified as control')
            target_decisions.append(pair['raw_decision'])
        else:
            passed = pair['raw_decision'] == expected
            require(type(pair['control_passed']) is bool and pair['control_passed'] == passed, f'{label}: control outcome changed')
            controls.append(passed)
    require(len(target_decisions) == 1 and results['ancillary_target_raw_decision'] == target_decisions[0], 'ancillary target raw-decision reference mismatch')
    require(type(results['controls_passed']) is int and results['controls_passed'] == sum(controls), 'control pass count mismatch')
    require(type(results['controls_total']) is int and results['controls_total'] == len(controls), 'control total mismatch')
    gate = 'passed' if all(controls) else 'failed'
    require(results['control_gate'] == gate, 'all-controls-pass gate not preserved')
    print(f"RECORDED SCIENTIFIC GATES: named source {results['named_pair_source_gate']}; controls {gate} ({sum(controls)}/{len(controls)} passed); named final {results['named_pair_final_decision']}; ancillary raw target {results['ancillary_target_raw_decision']}")


def replay_source(source: Path, manifest: dict) -> None:
    # Pillow is deliberately optional and imported only with explicit --source.
    from PIL import Image
    data = source.read_bytes()
    expected = manifest['source']
    require(sha(data) == expected['sha256'] and len(data) == expected['bytes'], 'supplied source does not match exact recorded capture bytes')
    count = 0
    with Image.open(io.BytesIO(data)) as image:
        require(list(image.size) == expected['dimensions'] and image.mode == expected['mode'] and image.format == expected['format'], 'supplied source dimensions/mode/format mismatch')
        require(getattr(image, 'n_frames', 1) == 1, 'supplied source must have one frame')
        image.load()
        for pair in manifest['pairs']:
            for item in pair['items']:
                for kind in ['crop', 'context']:
                    x, y, width, height = item[kind]['box']
                    native = image.crop((x, y, x + width, y + height))
                    for variant, rendered in [(kind, native), (kind + '_3x', native.resize((width * 3, height * 3), Image.Resampling.NEAREST))]:
                        memory = io.BytesIO()
                        rendered.save(memory, format='PNG')
                        encoded = memory.getvalue()
                        entry = item[variant]
                        require(sha(encoded) == entry['sha256'] and len(encoded) == entry['bytes'] and list(rendered.size) == entry['dimensions'], f'PNG replay mismatch: {entry["path"]}; check exact source and Pillow encoder version')
                        count += 1
    print(f'PASS: {count} PNGs recomputed in memory from the exact supplied capture; no output files written')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, help='optional manually supplied exact capture; requires Pillow; replay stays in memory')
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    try:
        sums = check_sums(package)
        originals = check_transforms(package, sums)
        manifest = check_metadata(package, originals, sums)
        if args.source is not None:
            replay_source(args.source, manifest)
    except (OSError, ValueError, KeyError, TypeError, ImportError, IndexError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print('Data-integrity verification completed; scientific gates retain their recorded outcomes. Named-ID binding is not independently certified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
