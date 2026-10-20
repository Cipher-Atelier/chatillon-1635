# Châtillon’s cipher letter to Servien (3 August 1635)

Châtillon’s cipher letter to Servien from Nijmegen, dated 3 August 1635. Graphical signs and numerical groups are compared with possible clear-text counterparts.

[Cipher Atelier](https://github.com/Cipher-Atelier) · [Research index](https://github.com/Cipher-Atelier/research-index) · [Reading guide](READING_GUIDE.md) · [Verification](verification/README.md)

## Current status — 11 October 2026

No continuous decipherment, full literal reading, complete translation or uniquely validated key is available. Published calculations test how proposed sign groupings and output lengths fit already exposed candidate text. They reveal dependencies in the assumptions; they do not identify the signs’ historical meanings.

| Evidence layer | Open this |
| --- | --- |
| Original | [Letter beginning, view135](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f135.item) · [cipher region, view139](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f139.item) |
| Recorded groups / conditional model | [Groups, reference wording and mappings](verification/experiments/chatillon-1635/config.json) |
| Saved model output | [Baseline results](verification/experiments/verification_results.json) · [7 October width package](verification/experiments/chatillon-width-spectrum-20261007/README.txt) |
| Interpretation of the calculations | [Research explanation](chatillon-1635/README.md) |

In the baseline, N2 maximum width 1 permits crossed-sign output `{f}`; maximum width 8 permits `{e,f,n,r}`. [Check this dependency](READING_GUIDE.md#check-one-example-by-hand). The baseline covers 6,144 dependent alignment conditions and 24 width conditions; the separate saved-width package checks 384 stored records and arithmetic. Full-reference zero counts are predetermined by input-length limits and cannot independently refute historical wording.

The published [equality diagnostic](verification/experiments/chatillon-slash-loop-consistency-20261011/README.md) has 24 dependent exploratory records; its protocol was corrected after production results. The [source audit](verification/experiments/chatillon-source-glyph-audit-20261011/README.md) leaves the named pair unresolved, with 3/4 passed controls and conditional historical-ID binding. All three later packages are on main. The [verification guide](verification/README.md#separate-package-scopes) gives each a separate command; the default check runs only the older baseline.

**Missing evidence:** secure source-ID coordinates, resolved grouping and physical classes, a coherent key explaining all occurrences, and independent same-key material or a contemporary key. The source-audit findings are unresolved even before considering its failed control gate.

## Start here

1. [Read the plain-language guide](READING_GUIDE.md): the document, result, file meanings and one worked check. No programming is required.
2. Open [Saved assumption-test results](verification/experiments/verification_results.json) to inspect the saved text or test result itself.
3. Read the [research account](chatillon-1635/README.md) for historical context, methods, earlier work and unresolved questions.

## Reproduce the checks

Follow the worked example in [the reading guide](READING_GUIDE.md#check-one-example-by-hand). It connects a source record, a key or model assumption, and the saved output. For an independent source check, use the [original-source entry](https://gallica.bnf.fr/ark:/12148/btv1b9058223v/f135.item); images are linked, not redistributed here.

If you use Python, follow the [complete verification instructions](verification/README.md), including download/setup, expected results and troubleshooting. The command from this repository’s top-level folder is:

```sh
python3 verification/check_all.py
```

A successful run means the published files and declared calculation reproduce. It does not establish that every source sign or historical interpretation is correct.

The [Evidence checks workflow](.github/workflows/verify.yml) runs this offline baseline on Python 3.10 and 3.13, without installing dependencies, and checks changed-file whitespace.

### Saved exact-width diagnostic from 7 October 2026

The [width-spectrum package](verification/experiments/chatillon-width-spectrum-20261007/README.txt) preserves seven unchanged historical files, all 384 saved scenario/width/control records, provenance, a derived summary and checksums. This is the saved 7 October exposed-input sensitivity diagnostic; adding it does not report a new experiment or a decipherment.

To check its bytes and saved-record consistency without rerunning either historical experiment program, use Python 3.8 or later from the repository root:

```sh
python3 verification/experiments/chatillon-width-spectrum-20261007/verify_saved_artifacts.py
```

This separate read-only check does not regenerate alignment paths. Every saved strict full-reference count is zero because the input can consume at most 50, 57 or 65 characters, while the references contain 110 or 111. That zero is guaranteed by input length and cannot independently refute the historical text. Integrity and arithmetic consistency do not establish a decipherment; the package README and provenance retain the remaining limitations.

### New conditional check: 11 October 2026

The [slash-loop consistency diagnostic](verification/experiments/chatillon-slash-loop-consistency-20261011/README.md) binds two occurrences already labelled `S_slash_loop` to the same output, retaining the published references and other constraints. In the surviving prefix alignments, both emit `i`, N2 emits `r`, and the open/closed crossed targets emit `s`/`f`. This tests the coherence of recorded assumptions; it does not establish a historical key or solve the letter.

The package includes saved joint-output counts, two implementations, synthetic controls, and a preserved initial-run audit. One synthetic-control expected count was corrected after results were seen; the report discloses this amendment and treats the result as exploratory. Full-reference zero counts remain guaranteed by input length and provide no independent evidence against the historical text.

## Research scope and limitations

Local conditional repeat and N2-width dependency hypothesis. Replay covers 6,144 dependent alignment conditions and 24 width conditions, not a recovered full key or independent confirmations.

A separate [source glyph limitation audit](verification/experiments/chatillon-source-glyph-audit-20261011/README.md) records proposed local source correspondences. The named pair remains unresolved under its frozen source gate: full ordering and cluster grouping are not independently established, and anonymous crop ratings cannot supply that binding.

## Contribute

This is part of [Cipher Atelier](https://github.com/Cipher-Atelier), founded by [Maxim Egorov](https://github.com/cayde-6). Explore the [research index](https://github.com/Cipher-Atelier/research-index), [contribution guide](https://github.com/Cipher-Atelier/.github/blob/main/CONTRIBUTING.md), and [step-by-step research workflow](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md).

Read the current result and source limitations, then coordinate a bounded task in an existing issue or use [Work on existing research](https://github.com/Cipher-Atelier/chatillon-to-servien-cipher-letter-1635/issues/new?template=research.yml). Fork the repository and submit a focused pull request with your evidence and checks. Independent replication and constructive alternative readings are welcome. See [Start here](https://github.com/Cipher-Atelier/research-index/blob/main/START_HERE.md) for the shared workflow.

## Sources and rights

Source credit and item-specific restrictions remain in the research records. Scans, crops, restricted materials and private correspondence are excluded. No new blanket licence is asserted. AI-assisted work requires evidence checking and does not constitute external human expert review.

[Publication provenance](SOURCE_PROVENANCE.json) records the source commit, retained file hashes and deliberate code/navigation adaptations. The original repository history remains intact.
