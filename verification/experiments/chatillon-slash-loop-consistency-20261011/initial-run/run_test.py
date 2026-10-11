#!/usr/bin/env python3
"""Finite path enumeration for the pinned slash-loop consistency diagnostic.

No search for plaintext or key values: each edge consumes the next reference
substring under the inherited constraints. Only the two declared IDs are bound.
Without --output this recomputes read-only and prints JSON. --output creates a
new file exclusively, so it never silently overwrites a saved result.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import sys

HERE = Path(__file__).resolve().parent
PROTOCOL_SHA = "9f0c55212ada57055295dec79406f3476899191298fd5f29bf93d15d373fb6d1"
INPUT_SHA = "b130ebb024676a41749532a473e5918078f64f572be83ed20f76a56f2b48b872"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def enumerate_paths(tokens, reference, fixed, pair, targets, n2_shape="N2", n2_max=1):
    """Explicit DFS; unresolved occurrences are independent, including same shapes.

    Yield every complete token path that fits a reference prefix. Fixed mappings
    consume their literal lengths (the inherited policy). A masked token never
    inherits a literal. N2 overrides any literal with lengths 1..n2_max.
    """
    ids = [t["id"] for t in tokens]
    require(len(ids) == len(set(ids)), "Duplicate token ID")
    require(all(x in ids for x in list(pair) + list(targets)), "Missing observed token")
    require(len(pair) == 2 and pair[0] != pair[1], "Pair must contain two distinct IDs")
    choices = []
    for token in tokens:
        literal = None if token["mapping_masked"] else fixed.get(token["shape"])
        if token["shape"] == n2_shape:
            literal, widths = None, list(range(1, n2_max + 1))
        else:
            widths = [len(literal)] if literal is not None else token["widths"]
        require(widths and all(type(w) is int and w > 0 for w in widths), "Nonpositive width")
        require(len(widths) == len(set(widths)), "Duplicate width")
        choices.append((literal, widths))
    observed = set(pair) | set(targets)
    stack = [(0, 0, {})]
    while stack:
        index, start, values = stack.pop()
        if index == len(tokens):
            yield start, values
            continue
        token = tokens[index]
        literal, widths = choices[index]
        for width in reversed(widths):
            end = start + width
            if end > len(reference):
                continue
            emitted = reference[start:end]
            if literal is not None and emitted != literal:
                continue
            next_values = values
            if token["id"] in observed:
                next_values = dict(values)
                next_values[token["id"]] = emitted
            stack.append((index + 1, end, next_values))


def measure(tokens, reference, fixed, pair, targets, n2_shape="N2", n2_max=1):
    baseline_count = equality_count = 0
    projections = [Counter() for _ in targets]
    surviving_projections = [Counter() for _ in targets]
    ends, surviving_ends, joint, surviving_joint = Counter(), Counter(), Counter(), Counter()
    for end, values in enumerate_paths(tokens, reference, fixed, pair, targets, n2_shape, n2_max):
        baseline_count += 1
        ends[str(end)] += 1
        for projection, identifier in zip(projections, targets):
            projection[values[identifier]] += 1
        emitted_pair = tuple(values[identifier] for identifier in pair)
        joint[emitted_pair] += 1
        if emitted_pair[0] == emitted_pair[1]:
            equality_count += 1
            surviving_ends[str(end)] += 1
            surviving_joint[emitted_pair] += 1
            for projection, identifier in zip(surviving_projections, targets):
                projection[values[identifier]] += 1

    def hist(counter):
        return [{"first": a, "second": b, "count": count}
                for (a, b), count in sorted(counter.items())]

    return {
        "baseline": {"count": baseline_count, "projections": [dict(sorted(p.items())) for p in projections],
                     "end_positions": dict(sorted(ends.items()))},
        "joint_slash_outputs": hist(joint),
        "equality": {"count": equality_count, "joint_slash_outputs": hist(surviving_joint),
                     "projections": [dict(sorted(p.items())) for p in surviving_projections],
                     "end_positions": dict(sorted(surviving_ends.items()))},
    }


def load_pinned():
    protocol_path = HERE / "PROTOCOL.json"
    require(sha(protocol_path) == PROTOCOL_SHA, "Protocol hash mismatch")
    protocol = json.loads(protocol_path.read_text())
    config_path = (HERE / protocol["input"]["path"]).resolve()
    require(sha(config_path) == INPUT_SHA == protocol["input"]["sha256"], "Input hash mismatch")
    config = json.loads(config_path.read_text())
    require(protocol["n2_max_widths"] == [1, 8], "Unexpected width family")
    require(len(config["scenarios"]) == 12, "Expected 12 declared scenarios")
    require(len(config["expected_width_results"]) == 24, "Expected 24 archived baselines")
    fixed = {k: v for k, v in config["active_mapping"].items() if k != config["n2_shape"]}
    require(len(fixed) == 8, "Expected eight retained mappings")
    for scenario in config["scenarios"]:
        by_id = {t["id"]: t for t in scenario["tokens"]}
        require(all(by_id[p]["shape"] == protocol["required_pair_shape"] for p in protocol["binding_pair"]),
                "Unexpected binding-pair shape")
    return protocol, config, fixed


def run():
    require(sys.version_info >= (3, 10), "Python 3.10+ required")
    protocol, config, fixed = load_pinned()
    archived = {(r["reference_id"], r["grouping_id"], r["width"]): r
                for r in config["expected_width_results"]}
    require(len(archived) == 24, "Duplicate archived scenario/bound")
    records, effective = [], {}
    for scenario in config["scenarios"]:
        # Deduplicate only references identical over every reachable prefix,
        # with identical token/mapping constraints; suffix differences cannot
        # constitute independent trials in this prefix test.
        max_end = sum(8 if t["shape"] == config["n2_shape"] else
                      len(fixed[t["shape"]]) if not t["mapping_masked"] and t["shape"] in fixed else
                      max(t["widths"]) for t in scenario["tokens"])
        fingerprint = hashlib.sha256(json.dumps({"tokens": scenario["tokens"],
            "prefix": scenario["reference"][:max_end]}, sort_keys=True).encode()).hexdigest()
        effective_id = effective.setdefault(fingerprint, "effective_%02d" % (len(effective) + 1))
        targets = config["targets"] + [t["id"] for t in scenario["tokens"] if t["shape"] == config["n2_shape"]]
        for width in protocol["n2_max_widths"]:
            result = measure(scenario["tokens"], scenario["reference"], fixed,
                             protocol["binding_pair"], targets, config["n2_shape"], width)
            old = archived[(scenario["reference_id"], scenario["grouping_id"], width)]
            require(result["baseline"] == {k: old[k] for k in ("count", "projections", "end_positions")},
                    "Archived baseline mismatch: %s/%s/%s" % (scenario["reference_id"], scenario["grouping_id"], width))
            records.append({"reference_id": scenario["reference_id"], "grouping_id": scenario["grouping_id"],
                            "n2_max_width": width, "effective_case": effective_id,
                            "projection_ids": targets, "baseline_matches_archive": True, **result})
    require(len(effective) == 6, "Expected six effective prefix cases")
    summary = {"named_scenarios": 12, "effective_prefix_cases": 6, "scenario_bound_records": 24,
               "effective_case_bound_records": 12,
               "baseline_nonempty_records": sum(r["baseline"]["count"] > 0 for r in records),
               "equality_nonempty_records": sum(r["equality"]["count"] > 0 for r in records),
               "all_archived_baselines_match": True}
    return {"schema_version": 1, "status": "calculation_completed", "method": "explicit finite path enumeration",
            "date_utc": protocol["date_utc"], "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "hashes": {"input_sha256": INPUT_SHA, "protocol_sha256": PROTOCOL_SHA,
                       "code_sha256": {name: sha(HERE / name) for name in
                                       ("run_test.py", "independent_check.py", "tests.py")}},
            "commands": ["python3 tests.py", "python3 run_test.py --output RESULTS.json",
                         "python3 independent_check.py RESULTS.json"],
            "constraints": {"binding_pair": protocol["binding_pair"], "pair_shape": protocol["required_pair_shape"],
                            "n2_max_widths": protocol["n2_max_widths"], "retained_fixed_mapping": fixed,
                            "unknown_occurrences": "independent except declared pair equality",
                            "endpoint_policy": "all token paths fitting a reference prefix",
                            "mapping_masked": "retained verbatim; no fixed literal when masked",
                            "target_projections": "in declared projection_ids order; includes N2 after crossed targets"},
            "limitations": protocol["limitations"], "bounds": protocol["bounds"],
            "ai_assistance": protocol["ai_assistance"], "summary": summary, "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="create a new result file exclusively")
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(encoded)
        print(json.dumps({"output": str(args.output), "sha256": sha(args.output), "summary": result["summary"]}))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
