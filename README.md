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

## Precise research scope

Local conditional repeat and N2-width dependency hypothesis. Replay covers 6,144 dependent alignment conditions and 24 width conditions, not a recovered full key or independent confirmations.

A separate [source glyph limitation audit](verification/experiments/chatillon-source-glyph-audit-20261011/README.md) records proposed local source correspondences. The named pair remains unresolved under its frozen source gate: full ordering and cluster grouping are not independently established, and anonymous crop ratings cannot supply that binding.

This is part of [Cipher-Atelier](https://github.com/Cipher-Atelier), founded by [Maxim Egorov](https://github.com/cayde-6). Explore the [research index](https://github.com/Cipher-Atelier/research-index), [contribution guide](https://github.com/Cipher-Atelier/.github/blob/main/CONTRIBUTING.md), and [step-by-step research workflow](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md).

Source credit and item-specific restrictions remain in the research records. Scans, crops, restricted materials and private correspondence are excluded. No new blanket licence is asserted. AI-assisted work requires evidence checking and does not constitute external human expert review.

[Publication provenance](SOURCE_PROVENANCE.json) records the source commit, retained file hashes and deliberate code/navigation adaptations. The original repository history remains intact.

## Contribute to this investigation

Read the current result and source limitations, then coordinate a bounded task in an existing issue or use [Work on existing research](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635/issues/new?template=research.yml). Fork the repository and submit a focused pull request with your evidence and checks. Independent replication and constructive alternative readings are welcome. See [Start here](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md) for the shared workflow.
