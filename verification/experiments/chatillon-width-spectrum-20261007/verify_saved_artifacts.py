#!/usr/bin/env python3
"""Verify saved bytes and record arithmetic. Never execute the cipher programs."""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "original"
ORIGINAL_NAMES = (
    "PROTOCOL.txt", "README.txt", "RESULTS.json", "SHA256SUMS.json",
    "config.json", "independent_check.py", "test_widths.py",
)
CONTROLS = ("original", "rotate", "reverse", "swap")
HISTORICAL_MANIFEST_SHA256 = "e8eb75ce618ece23bf02a5754cd990c831dd27fa102562b24fc89a964963c599"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aggregate(rows, field):
    values = Counter()
    for row in rows:
        values.update(row[field])
    return dict(sorted(values.items()))


def maximum_consumed_length(config, scenario, n2_width=8):
    key = {k: v for k, v in config["active_mapping"].items() if k != "N2"}
    total = 0
    for token in scenario["tokens"]:
        value = None if token["mapping_masked"] else key.get(token["shape"])
        total += len(value) if value is not None else (
            n2_width if token["shape"] == "N2" else max(token["widths"])
        )
    return total


def make_summary(config, rows):
    """Aggregate only saved result fields and static input bounds."""
    conditions = []
    for control in CONTROLS:
        group = [r for r in rows if r["control"] == control]
        conditions.append({
            "control": control,
            "record_count": len(group),
            "nonempty_record_count": sum(r["count"] > 0 for r in group),
            "saved_prefix_path_total_over_named_scenarios": sum(r["count"] for r in group),
            "saved_full_endpoint_total": sum(r["full_endpoint_count"] for r in group),
            "exact_widths": [{
                "width": width,
                "saved_prefix_path_total_over_named_scenarios": sum(
                    r["count"] for r in group if r["width"] == width),
                "closed_sign_outputs": sorted({
                    text for r in group if r["width"] == width for text in r["closed"]}),
                "n2_substrings": sorted({
                    text for r in group if r["width"] == width for text in r["n2"]}),
            } for width in range(1, 9)],
        })
    return {
        "historical_experiment_date": "2026-10-07",
        "packaging_validation_date_utc": "2026-10-11",
        "experiment_rerun_during_packaging": False,
        "summary_basis": "Read-only aggregation of preserved RESULTS.json and static config.json bounds",
        "record_count": len(rows),
        "scenario_count": len(config["scenarios"]),
        "reference_lengths": sorted({len(s["reference"]) for s in config["scenarios"]}),
        "saved_successful_endpoints": sorted({int(p) for r in rows for p in r["ends"]}),
        "maximum_consumed_length_at_n2_width_8_by_scenario": [{
            "reference_id": s["reference_id"], "grouping_id": s["grouping_id"],
            "reference_length": len(s["reference"]),
            "maximum_consumed_length": maximum_consumed_length(config, s),
        } for s in config["scenarios"]],
        "conditions": conditions,
        "limitations": [
            "Not a decipherment, full coherent key, blind test, or independent plaintext witness.",
            "Unknown occurrences remain independent and eight inherited non-N2 mappings are retained.",
            "Named scenarios are duplicated over the consumed prefix; path totals are not independent trials.",
            "All successful saved paths require conditional sous wording and conditional token grouping.",
            "Negative controls diagnose dependence on retained anchors, not calibrated statistical significance.",
            "Zero strict full-reference counts are structurally guaranteed by the token-span bounds.",
            "Static integrity and arithmetic checks do not independently regenerate alignment results.",
        ],
    }


def verify():
    package_manifest = ROOT / "SHA256SUMS.txt"
    package_files_checked = []
    for line in package_manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        target = ROOT / relative
        require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
                "Unsafe package checksum path")
        require(target.is_file() and not target.is_symlink(), "Missing/nonregular file: " + relative)
        require(digest(target) == expected, "Package digest mismatch: " + relative)
        package_files_checked.append(relative)
    require(len(package_files_checked) == len(set(package_files_checked)), "Duplicate checksum entry")
    expected_package_files = set("original/" + name for name in ORIGINAL_NAMES) | {
        "README.txt", "PROVENANCE.txt", "SAVED_RESULTS_SUMMARY.json", "verify_saved_artifacts.py"
    }
    require(set(package_files_checked) == expected_package_files, "Unexpected package checksum scope")
    require(set(p.name for p in ORIGINAL.iterdir()) == set(ORIGINAL_NAMES), "Original-file allowlist mismatch")
    require(digest(ORIGINAL / "SHA256SUMS.json") == HISTORICAL_MANIFEST_SHA256,
            "Historical manifest differs from preserved packaging baseline")
    historical = json.loads((ORIGINAL / "SHA256SUMS.json").read_text(encoding="utf-8"))
    historical_files_checked = []
    for name in ORIGINAL_NAMES:
        if name == "SHA256SUMS.json":
            continue
        require(digest(ORIGINAL / name) == historical[name], "Historical digest mismatch: " + name)
        historical_files_checked.append(name)
    for script in (ORIGINAL / "test_widths.py", ORIGINAL / "independent_check.py", Path(__file__)):
        ast.parse(script.read_text(encoding="utf-8"), filename=script.name)

    config = json.loads((ORIGINAL / "config.json").read_text(encoding="utf-8"))
    rows = json.loads((ORIGINAL / "RESULTS.json").read_text(encoding="utf-8"))
    scenarios = {(s["reference_id"], s["grouping_id"]): s for s in config["scenarios"]}
    require(len(scenarios) == len(config["scenarios"]) == 12, "Scenario coverage mismatch")
    expected = {(a, b, w, c) for a, b in scenarios for w in range(1, 9) for c in CONTROLS}
    actual = [(r["reference_id"], r["grouping_id"], r["width"], r["control"]) for r in rows]
    require(len(rows) == len(set(actual)) == 384 and set(actual) == expected, "Result coverage mismatch")
    for row in rows:
        require(type(row["count"]) is int and row["count"] >= 0, "Invalid path count")
        for field in ("closed", "n2", "ends"):
            histogram = row[field]
            require(isinstance(histogram, dict), "Invalid histogram")
            require(all(type(v) is int and v > 0 for v in histogram.values()), "Invalid histogram count")
            require(sum(histogram.values()) == row["count"], "Histogram total mismatch")
        scenario = scenarios[row["reference_id"], row["grouping_id"]]
        length = len(scenario["reference"])
        require(all(p.isdecimal() and 0 <= int(p) <= length for p in row["ends"]), "Endpoint out of bounds")
        require(type(row["full_endpoint_count"]) is int and row["full_endpoint_count"] >= 0,
                "Invalid full-endpoint count")
        require(row["full_endpoint_count"] == row["ends"].get(str(length), 0), "Full-endpoint mismatch")
        require(all(len(text) == row["width"] for text in row["n2"]), "N2 substring width mismatch")
        require(all(int(p) <= maximum_consumed_length(config, scenario, row["width"])
                    for p in row["ends"]), "Endpoint exceeds static token-span bound")

    inherited_checked = 0
    for older in config["expected_width_results"]:
        subset = [r for r in rows if r["reference_id"] == older["reference_id"]
                  and r["grouping_id"] == older["grouping_id"] and r["control"] == "original"
                  and r["width"] <= older["width"]]
        require(sum(r["count"] for r in subset) == older["count"], "Inherited maximum-width count mismatch")
        require(aggregate(subset, "closed") == older["projections"][1], "Inherited closed histogram mismatch")
        require(aggregate(subset, "n2") == older["projections"][2], "Inherited N2 histogram mismatch")
        require(aggregate(subset, "ends") == older["end_positions"], "Inherited endpoint histogram mismatch")
        inherited_checked += 1
    summary = json.loads((ROOT / "SAVED_RESULTS_SUMMARY.json").read_text(encoding="utf-8"))
    require(summary == make_summary(config, rows), "Saved-result summary mismatch")
    return {
        "status": "passed",
        "validation_type": "Read-only integrity, syntax, saved-record coverage, arithmetic, and static bounds",
        "experiment_programs_executed": False,
        "alignment_results_independently_regenerated": False,
        "historical_files_matching_original_manifest": len(historical_files_checked),
        "package_files_matching_checksums": len(package_files_checked),
        "unique_saved_result_records": len(rows),
        "inherited_maximum_width_summaries_checked": inherited_checked,
        "inherited_fields_checked": ["count", "closed projection", "N2 projection", "endpoint histogram"],
        "current_validation_python_version": sys.version.split()[0],
    }


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2))
    except (OSError, ValueError, KeyError, TypeError, SyntaxError) as exc:
        print("Verification failed: " + str(exc), file=sys.stderr)
        sys.exit(1)
