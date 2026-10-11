# Verify chatillon-1635

[Repository overview](../README.md) · [Read the result and check one example by hand](../READING_GUIDE.md)

## What this check does

The supported command first checks the published file fingerprints in `SHA256SUMS.txt`, then repeats this investigation’s saved calculation. A fingerprint (SHA-256) identifies exact file bytes; it is not a scientific correctness score.

The public replay enumerates the declared assumption family. It does not certify the comparator wording, recover a full key or rerun every earlier solver and transfer experiment.

It uses Python’s standard library, makes no network requests, and needs no downloaded scans or extra packages for this default check. It does not fit a new key or edit the research evidence.

## Download and open the folder

1. On [this repository’s main page](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635), choose **Code → Download ZIP**, following [GitHub’s download instructions](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives).
2. Extract the whole ZIP. Keep its folders and files together; do not download only `check_all.py`.
3. Open a terminal in the extracted top-level folder: it contains `README.md`, `SHA256SUMS.txt` and the `verification` folder. For example, after navigating to its parent directory:

```sh
cd chatillon-to-servien-cipher-letter-1635-main
```

If you already use Git, cloning the full repository is an alternative:

```sh
git clone https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635.git
cd chatillon-to-servien-cipher-letter-1635
```

## Run the supported check

Use **Python 3.10 or later**. On macOS/Linux, check the installed version and run:

```sh
python3 --version
python3 verification/check_all.py
```

On Windows, if the Python launcher is installed, use:

```powershell
py -3 --version
py -3 verification/check_all.py
```

If your Python command is `python` rather than `python3` or `py -3`, use that command after confirming it is Python 3.10+. If Python is absent, obtain it from [python.org](https://www.python.org/downloads/) or your operating system’s supported installation method.

Run ordinary Python, with no `-O`/`-OO` options and no `PYTHONOPTIMIZE` setting that enables optimization: the checker relies on assertions.

## What a successful run looks like

The command exits successfully and prints a JSON report with top-level `"status": "passed"`. It also reports how many fingerprinted files were checked. That file count can change when documentation is updated.

The following are the expected status/topic/replay fields; the actual report also includes `files_checked` and scope limits:

```json
{
  "status": "passed",
  "topic": "chatillon-1635",
  "replay": {
    "chatillon-1635": {
      "status": "passed",
      "ablation_conditions": 6144,
      "width_conditions": 24,
      "forcing_subsets": 240,
      "closed_values_by_n2_max_width": {
        "1": [
          "f"
        ],
        "8": [
          "e",
          "f",
          "n",
          "r"
        ]
      },
      "scope": "Conditional exposed-text alignment, not a recovered complete key"
    }
  }
}
```

In ordinary words: **6,144 dependent alignment conditions and 24 width conditions reproduce; the saved candidate sets are 1 → [f] and 8 → [e, f, n, r].**

## Separate package scopes

The root `check_all.py` runs only `experiments/verify.py`, covering the older 6,144 dependent alignment conditions and 24 width conditions. It does not run later packages. All three packages below are published on main; each command checks its stated scope.

**On main:** the [7 October width-spectrum package](experiments/chatillon-width-spectrum-20261007/README.txt), merged through PR4, has 384 saved records. From the root, with Python 3.8+ and the standard library:

```sh
python3 verification/experiments/chatillon-width-spectrum-20261007/verify_saved_artifacts.py
```

This checks integrity and stored arithmetic, not fresh path enumeration. Its full-reference zero counts follow from input-length limits and cannot independently refute the historical text.

**Equality diagnostic:** [package README](experiments/chatillon-slash-loop-consistency-20261011/README.md). With Python 3.10+, enter its package directory from the repository root:

```sh
cd verification/experiments/chatillon-slash-loop-consistency-20261011
python3 tests.py
python3 independent_check.py RESULTS.json
```

Expected: `records_checked=24`, `archived_baselines_checked=24`. The diagnostic is exploratory: its written protocol was corrected after production results. For fresh enumeration follow that README; `run_test.py` without `--output` prints JSON without changing the saved results.

**Source audit:** [package README](experiments/chatillon-source-glyph-audit-20261011/README.md). From the repository root:

```sh
python3 verification/experiments/chatillon-source-glyph-audit-20261011/verify_audit.py
```

The package records Python 3.13.9 and optional Pillow 11.3.0. Default verification checks metadata integrity without loading pixels. The named pair remains unresolved, 3/4 controls passed, and historical-ID binding is conditional. Pixel reproduction requires the exact withheld capture; a fresh Gallica screenshot is a different input.

PR4–6 were confirmed merged on 11 October 2026. Integration makes the packages available here; it does not validate their historical claims.

## What passing does not establish

The successful local repeat example does not validate a global repeat operator. Complete-passage fits fail or depend on exposed text and grouping assumptions. No complete plaintext or unique full key is available.

Passing verifies that these published inputs and saved rules give the recorded result. It does not certify source-image transcription, historical truth, a unique interpretation, author identity, discovery priority or external expert review. To inspect those questions, follow [the manual example and source-checking route](../READING_GUIDE.md#check-one-example-by-hand).

## If it fails

| Symptom | What to do |
| --- | --- |
| Python command not found, or version below 3.10 | Install/use Python 3.10+; confirm its version first |
| Cannot open `verification/check_all.py` | Move into the extracted repository’s top-level folder |
| Missing file | Extract the complete ZIP again; retain the directory structure |
| `Hash mismatch: ...` | Compare with an untouched download of the same version; edits change the fingerprint |
| Optimization warning | Run without `-O`/`-OO` and disable any `PYTHONOPTIMIZE` setting |
| Assertion, replay mismatch or another error on an untouched package | Save the complete error, Python version and repository commit/download reference; report it in a [research issue](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635/issues/new?template=research.yml) |

Do not change the evidence, expected results or fingerprints just to make a failing check pass. If reporting reproduction, record the commit SHA shown on GitHub; a later `main` download may contain documentation updates. A [commit-specific archive](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#source-code-archive-urls) pins the file version.

## Preserved publication scope

Local conditional repeat and N2-width dependency hypothesis. Replay covers 6,144 dependent alignment conditions and 24 width conditions, not a recovered full key or independent confirmations.

Conditional mappings and N2-width dependency; no uniquely validated full key. 6,144 conditions are dependent variants, not independent confirmations. Local repeat behavior does not establish a global rule.

From the repository root run `python3 verification/check_all.py` with Python 3.10 or later, without optimization. It verifies the repository checksum inventory and invokes only [experiments/verify.py](experiments/verify.py). The check uses the standard library and makes no network requests. Obtain source images separately under their provider terms for visual review. Source credit is not image redistribution permission.

See the [research record](../chatillon-1635/README.md) and [machine-readable scope](TOPIC_SCOPE_INDEX.json). Successful arithmetic or exact output replay does not prove historical truth, unique interpretation or priority.
