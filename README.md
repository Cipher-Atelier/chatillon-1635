# Châtillon’s cipher letter to Servien (3 August 1635)

Châtillon’s cipher letter to Servien from Nijmegen, dated 3 August 1635. Graphical signs and numerical groups are compared with possible clear-text counterparts.

## What has been found?

This is an unfinished reconstruction and a test of assumptions, not a complete decipherment. The current reproducible result shows how the possible reading of a crossed sign changes when the neighboring numeral N2 is allowed to emit more letters.

A small example from the recorded result:

```text
N2: one letter → {f}; up to eight letters → {e, f, n, r}
```

These sets describe outputs allowed by a declared alignment model. They do not establish the historical meaning of N2 or of the crossed sign.

## Start reading

1. [Read the plain-language guide](READING_GUIDE.md): the document, result, file meanings and one worked check. No programming is required.
2. Open [Saved assumption-test results](verification/experiments/verification_results.json) to inspect the saved text or test result itself.
3. Read the [research account](chatillon-1635/README.md) for historical context, methods, earlier work and unresolved questions.

## How can I check it?

Follow the worked example in [the reading guide](READING_GUIDE.md#check-one-example-by-hand). It connects a source record, a key or model assumption, and the saved output. For an independent source check, use the [original-source entry](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f135.item); images are linked, not redistributed here.

If you use Python, follow the [complete verification instructions](verification/README.md), including download/setup, expected results and troubleshooting. The command from this repository’s top-level folder is:

```sh
python3 verification/check_all.py
```

A successful run means the published files and declared calculation reproduce. It does not establish that every source sign or historical interpretation is correct.

### Saved exact-width diagnostic from 7 October 2026

The [width-spectrum package](verification/experiments/chatillon-width-spectrum-20261007/README.txt) preserves seven unchanged historical files, all 384 saved scenario/width/control records, provenance, a derived summary and checksums. This is the saved 7 October exposed-input sensitivity diagnostic; adding it does not report a new experiment or a decipherment.

To check its bytes and saved-record consistency without rerunning either historical experiment program, use Python 3.8 or later from the repository root:

```sh
python3 verification/experiments/chatillon-width-spectrum-20261007/verify_saved_artifacts.py
```

This separate read-only check does not regenerate alignment paths. Every saved strict full-reference count is zero because the input can consume at most 50, 57 or 65 characters, while the references contain 110 or 111. That zero is guaranteed by input length and cannot independently refute the historical text. Integrity and arithmetic consistency do not establish a decipherment; the package README and provenance retain the remaining limitations.

## New conditional check: 11 October 2026

The [slash-loop consistency diagnostic](verification/experiments/chatillon-slash-loop-consistency-20261011/README.md) binds two occurrences already labelled `S_slash_loop` to the same output, retaining the published references and other constraints. In the surviving prefix alignments, both emit `i`, N2 emits `r`, and the open/closed crossed targets emit `s`/`f`. This tests the coherence of recorded assumptions; it does not establish a historical key or solve the letter.

The package includes saved joint-output counts, two implementations, synthetic controls, and a preserved initial-run audit. One synthetic-control expected count was corrected after results were seen; the report discloses this amendment and treats the result as exploratory. Full-reference zero counts remain guaranteed by input length and provide no independent evidence against the historical text.

## Precise research scope

Local conditional repeat and N2-width dependency hypothesis. Replay covers 6,144 dependent alignment conditions and 24 width conditions, not a recovered full key or independent confirmations.

This is part of [Cipher-Atelier](https://github.com/Cipher-Atelier), founded by [Maxim Egorov](https://github.com/cayde-6). Explore the [research index](https://github.com/Cipher-Atelier/research-index), [contribution guide](https://github.com/Cipher-Atelier/.github/blob/main/CONTRIBUTING.md), and [step-by-step research workflow](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md).

Source credit and item-specific restrictions remain in the research records. Scans, crops, restricted materials and private correspondence are excluded. No new blanket licence is asserted. AI-assisted work requires evidence checking and does not constitute external human expert review.

[Publication provenance](SOURCE_PROVENANCE.json) records the source commit, retained file hashes and deliberate code/navigation adaptations. The original repository history remains intact.

## Contribute to this investigation

Read the current result and source limitations, then coordinate a bounded task in an existing issue or use [Work on existing research](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635/issues/new?template=research.yml). Fork the repository and submit a focused pull request with your evidence and checks. Independent replication and constructive alternative readings are welcome. See [Start here](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md) for the shared workflow.
