#!/usr/bin/env python3
"""Read-only independent augmented-state DP; never imports/runs run_test.py."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = "9f0c55212ada57055295dec79406f3476899191298fd5f29bf93d15d373fb6d1"
INPUT_SHA = "b130ebb024676a41749532a473e5918078f64f572be83ed20f76a56f2b48b872"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ensure(ok, message):
    if not ok:
        raise ValueError(message)


def dynamic_measure(tokens, text, mapping, binding_ids, output_ids, n2_shape="N2", maximum=1):
    """Count paths by (reference offset, tuple of captured emissions).

    At each token, multiply/merge incoming integer counts. Capture two pair
    emissions plus projections in state. This retains correlations rather than
    inferring equality from separate marginal projections. No paths are listed.
    """
    capture_ids = list(dict.fromkeys(list(binding_ids) + list(output_ids)))
    slots = {identifier: i for i, identifier in enumerate(capture_ids)}
    token_ids = [token["id"] for token in tokens]
    ensure(len(token_ids) == len(set(token_ids)), "Duplicate token ID")
    ensure(set(capture_ids) <= set(token_ids), "Missing capture ID")
    ensure(len(binding_ids) == 2 and len(set(binding_ids)) == 2, "Invalid pair")
    states = {(0, (None,) * len(capture_ids)): 1}
    for token in tokens:
        fixed = mapping.get(token["shape"]) if not token["mapping_masked"] else None
        if token["shape"] == n2_shape:
            lengths = range(1, maximum + 1)
            fixed = None
        elif fixed is not None:
            lengths = (len(fixed),)
        else:
            lengths = token["widths"]
        lengths = tuple(lengths)
        ensure(lengths and all(type(w) is int and w > 0 for w in lengths), "Invalid width")
        ensure(len(lengths) == len(set(lengths)), "Repeated width")
        next_states = defaultdict(int)
        for (offset, captured), multiplicity in states.items():
            for size in lengths:
                stop = offset + size
                if stop > len(text):
                    continue
                emission = text[offset:stop]
                if fixed is not None and emission != fixed:
                    continue
                updated = captured
                if token["id"] in slots:
                    updated = list(captured)
                    updated[slots[token["id"]]] = emission
                    updated = tuple(updated)
                next_states[(stop, updated)] += multiplicity
        states = dict(next_states)
    base_total = equal_total = 0
    base_end, equal_end, paired, equal_paired = (defaultdict(int) for _ in range(4))
    base_projection = [defaultdict(int) for _ in output_ids]
    equal_projection = [defaultdict(int) for _ in output_ids]
    for (stop, captured), ways in states.items():
        pair = (captured[slots[binding_ids[0]]], captured[slots[binding_ids[1]]])
        base_total += ways
        base_end[str(stop)] += ways
        paired[pair] += ways
        for index, identifier in enumerate(output_ids):
            base_projection[index][captured[slots[identifier]]] += ways
        if pair[0] == pair[1]:
            equal_total += ways
            equal_end[str(stop)] += ways
            equal_paired[pair] += ways
            for index, identifier in enumerate(output_ids):
                equal_projection[index][captured[slots[identifier]]] += ways

    def serialize_pairs(counts):
        return [{"first": pair[0], "second": pair[1], "count": counts[pair]} for pair in sorted(counts)]

    return {"baseline": {"count": base_total, "projections": [dict(sorted(p.items())) for p in base_projection],
                         "end_positions": dict(sorted(base_end.items()))},
            "joint_slash_outputs": serialize_pairs(paired),
            "equality": {"count": equal_total, "projections": [dict(sorted(p.items())) for p in equal_projection],
                         "end_positions": dict(sorted(equal_end.items())),
                         "joint_slash_outputs": serialize_pairs(equal_paired)}}


def check(saved_path):
    ensure(sys.version_info >= (3, 10), "Python 3.10+ required")
    ensure(digest(HERE / "PROTOCOL.json") == PROTOCOL_SHA, "Protocol hash mismatch")
    protocol = json.loads((HERE / "PROTOCOL.json").read_text())
    source_path = HERE / protocol["input"]["path"]
    ensure(digest(source_path) == INPUT_SHA == protocol["input"]["sha256"], "Input hash mismatch")
    config = json.loads(source_path.read_text())
    saved = json.loads(Path(saved_path).read_text())
    ensure(saved["hashes"]["input_sha256"] == INPUT_SHA, "Saved input hash mismatch")
    ensure(saved["hashes"]["protocol_sha256"] == PROTOCOL_SHA, "Saved protocol hash mismatch")
    for name in ("run_test.py", "independent_check.py", "tests.py"):
        ensure(saved["hashes"]["code_sha256"][name] == digest(HERE / name), "Saved code hash mismatch: " + name)
    ensure(protocol["n2_max_widths"] == [1, 8], "Unexpected bounds")
    ensure(len(config["scenarios"]) == 12, "Unexpected scenario count")
    key = {name: value for name, value in config["active_mapping"].items() if name != config["n2_shape"]}
    ensure(len(key) == 8, "Expected eight fixed mappings")
    archived = {(r["reference_id"], r["grouping_id"], r["width"]): r for r in config["expected_width_results"]}
    saved_records = {(r["reference_id"], r["grouping_id"], r["n2_max_width"]): r for r in saved["records"]}
    ensure(len(archived) == len(saved_records) == len(saved["records"]) == 24, "Unexpected record count")
    observed_keys = set()
    for scenario in config["scenarios"]:
        outputs = config["targets"] + [t["id"] for t in scenario["tokens"] if t["shape"] == config["n2_shape"]]
        for bound in (1, 8):
            record_key = (scenario["reference_id"], scenario["grouping_id"], bound)
            observed_keys.add(record_key)
            computed = dynamic_measure(scenario["tokens"], scenario["reference"], key,
                                       protocol["binding_pair"], outputs, config["n2_shape"], bound)
            previous = archived[record_key]
            ensure(computed["baseline"] == {k: previous[k] for k in ("count", "projections", "end_positions")},
                   "DP archived baseline mismatch: " + str(record_key))
            record = saved_records[record_key]
            ensure(record["projection_ids"] == outputs, "Projection ID mismatch")
            ensure(all(record[k] == computed[k] for k in computed), "DP saved result mismatch: " + str(record_key))
    ensure(observed_keys == set(archived) == set(saved_records), "Unexpected scenario set")
    return {"status": "passed", "method": "independent augmented-state dynamic program",
            "records_checked": 24, "archived_baselines_checked": 24,
            "comparisons": "baseline and equality counts, all projections, endpoint and joint-output histograms",
            "input_sha256": INPUT_SHA, "protocol_sha256": PROTOCOL_SHA,
            "results_sha256": digest(saved_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.results), indent=2))
