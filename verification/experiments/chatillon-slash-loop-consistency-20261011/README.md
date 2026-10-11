# Slash-loop consistency diagnostic, 11 October 2026

This exploratory calculation asks whether the two recorded `S_slash_loop`
occurrences can emit the same string under the inherited prefix-alignment
constraints. It uses the existing [pinned input](../chatillon-1635/config.json),
without changing historical data or rerunning the earlier experiment scripts.
Read [REPORT.txt](REPORT.txt) for counts, full paired-output histograms and scope.

Eight baseline-nonempty named records retain equality-compatible paths, with
conditional slash outputs `i/i`, crossed outputs `s/f`, N2 output `r`, and
endpoint 39. The 24 records represent 12 named scenarios and six effective prefix
cases duplicated across reference alternatives; they are not independent trials.
No historical key assignment or full decipherment is established.

## Reproduce the current calculation

Use Python 3.10+ and the standard library. From this directory:

```sh
python3 tests.py
python3 run_test.py --output RECOMPUTED.json
python3 independent_check.py RECOMPUTED.json
python3 independent_check.py RESULTS.json
```

`run_test.py` without `--output` prints recomputed JSON and makes no file changes.
An explicit output is created exclusively and must not already exist. The
independent checker only reads files; it neither imports nor runs the enumerator.
It uses an augmented-state dynamic program to check all 24 saved baseline/equality
counts, paired-output histograms, projections and endpoints against the pinned
input, then checks summary consistency. It also verifies input/protocol/code hashes.

The saved run used CPython 3.13.9. `RESULTS.json` contains hashes, software version,
constraints, all 24 records, and the post-result protocol amendment. Fingerprints
establish file identity, not historical correctness.

## Original run and correction

The first calculation's outputs were already visible when protocol v2 corrected
one synthetic expected count. For `X,q,X` against `abqac` with widths 1..2, the
prefix model has two independent paths (endpoints 4 and 5), not one; neither has
equal X. The tests already asserted two paths, but this disagreed with protocol
v1's written criterion. The initial run is therefore not a valid conclusion under
v1. It must not be described as successful preregistered validation.

The correction changed no production input, hypothesis, width family, mappings,
algorithm or production criteria. Corrected production records and summary are
identical to the first run. [PROTOCOL.json](PROTOCOL.json) explicitly records the
post-result amendment. `initial-run/` preserves the exact five original files as
audit bytes; use the current top-level files for reproduction.

For audit, the original computation can be reconstructed in a temporary copied
tree, keeping its expected relative input layout. This runs only the archived
new diagnostic, not the older research experiments:

```python
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

here = Path.cwd()  # this experiment directory
with tempfile.TemporaryDirectory() as temporary:
    experiments = Path(temporary) / "verification" / "experiments"
    original = experiments / here.name
    original.mkdir(parents=True)
    for source in (here / "initial-run").iterdir():
        if source.is_file():
            shutil.copy2(source, original / source.name)
    inputs = experiments / "chatillon-1635"
    inputs.mkdir()
    shutil.copy2(here.parent / "chatillon-1635" / "config.json", inputs / "config.json")
    subprocess.run([sys.executable, "tests.py"], cwd=original, check=True)
    subprocess.run([sys.executable, "run_test.py", "--output", "REPLAY.json"], cwd=original, check=True)
    subprocess.run([sys.executable, "independent_check.py", "REPLAY.json"], cwd=original, check=True)
    archived = json.loads((original / "RESULTS.json").read_text())
    replay = json.loads((original / "REPLAY.json").read_text())
    assert archived["records"] == replay["records"]
```

This reconstructs arithmetic, including the correctly counted synthetic paths in
the old test code; it does not repair v1's inconsistent written criterion.

## Limits and next evidence

The protocol lists the exact limitations: exposed wording and assumptions,
uncertified source-glyph identity, remaining independent unknown slots,
structurally guaranteed zero full-reference fits, and incomplete access to private
prior work. Equality success concerns only this conditional model. Source view139
was accessible and inspected at general scale in the parent task; the specific
glyph pair still needs independent adjudication, and an independent same-key text
is needed for validation beyond the exposed reference. No source image is included.

`SHA256SUMS.txt` covers all saved files here except the manifest itself and Python
caches. The immutable input hash is pinned in the protocol and results rather
than copied into this directory. No old package files are added to this diagnostic.
